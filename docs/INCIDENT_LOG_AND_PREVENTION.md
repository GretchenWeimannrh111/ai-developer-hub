# 生产环境运维复盘与故障预防白皮书
## Production Incident Post-Mortem & Architecture Prevention Runbook

> **适用范围**：`20020723.xyz` 聚合平台、`api.20020723.xyz` (Sub2API)、`image.20020723.xyz` (绘图工作台)、`videogen.20020723.xyz` (视频工坊) 及全站反向代理架构。  
> **制定目的**：记录过往真实生产故障根因，建立可落地的工程防范机制，严禁二次踩坑。

---

## 目录
1. [故障一：Cloudflare 301 无限重定向死循环 (ERR_TOO_MANY_REDIRECTS)](#1-cloudflare-301-无限重定向死循环)
2. [故障二：Cloudflare 522 握手超时与 Linux TCP 队列溢出](#2-cloudflare-522-握手超时与-linux-tcp-队列溢出)
3. [故障三：大模型 API 响应头溢出 (upstream sent too big header)](#3-大模型-api-响应头溢出)
4. [故障四：聚合平台 Iframe 沙箱限制导致登录/下载失效](#4-聚合平台-iframe-沙箱限制导致登录下载失效)
5. [故障五：移动端视口溢出与选项卡竖向折行穿透](#5-移动端视口溢出与选项卡竖向折行穿透)
6. [故障六：Edge / Windows 系统无障碍导致 Canvas 粒子球静止或白屏](#6-edge--windows-系统无障碍导致-canvas-粒子球静止或白屏)
7. [生产标准 Nginx 模版与系统参数配置速查](#7-生产标准-nginx-模版与系统参数配置速查)

---

### 1. Cloudflare 301 无限重定向死循环

#### 故障现象
用户在访问 `https://image.20020723.xyz/` 时，浏览器报错 `ERR_TOO_MANY_REDIRECTS`，网络请求瀑布流显示该域名在循环返回 `301 Moved Permanently`。

#### 底层根因剖析
1. **Cloudflare 与源站 SSL 握手协议失配**：  
   当 Cloudflare 域名的 SSL/TLS 加密模式设置为 **Flexible（灵活）** 时，Cloudflare 边缘节点向源服务器请求时**强制使用 HTTP (端口 80)**。
2. **源站 Nginx 80 端口自循环**：  
   源站 Nginx 在 80 端口配置了无条件的跳转指令：
   ```nginx
   server {
       listen 80;
       server_name image.20020723.xyz;
       return 301 https://$host$request_uri; # 致命死循环触发点
   }
   ```
3. **死循环发生路径**：  
   `客户端浏览器 (HTTPS)` $\to$ `Cloudflare 边缘 (443)` $\to$ `Cloudflare 回源请求 (HTTP 80)` $\to$ `源站 Nginx (80 返回 301)` $\to$ `Cloudflare 将 301 透传给浏览器` $\to$ `浏览器重定向到 HTTPS` $\to$ `无限循环`。

#### 预防与工程标准
1. **Cloudflare 端设置**：  
   所有域名 SSL 模式必须统一配置为 **Full** 或 **Full (Strict)**。
2. **源站 Nginx 双端口直通准则**：  
   对于作为反向代理转发至内部服务（如 Docker 端口 21789）的站点，Nginx 的 80 端口与 443 端口应一并直接转发，禁止随意配置全局无条件 301：
   ```nginx
   server {
       listen 80;
       listen 443 ssl http2;
       server_name image.20020723.xyz;

       # 证书配置（443 时生效）
       ssl_certificate /etc/letsencrypt/live/20020723.xyz/fullchain.pem;
       ssl_certificate_key /etc/letsencrypt/live/20020723.xyz/privkey.pem;

       location / {
           proxy_pass http://127.0.0.1:21789;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
   }
   ```
3. **若需强制 HTTPS**：  
   应在 Cloudflare 后台开启「Always Use HTTPS」，而非在源站 80 端口写粗暴的跳转规则。

---

### 2. Cloudflare 522 握手超时与 Linux TCP 队列溢出

#### 故障现象
在访问 `api.20020723.xyz` 或主站聚合时，Cloudflare 偶发报错 `Error 522: Connection timed out`。

#### 底层根因剖析
1. **TCP 半连接与全连接队列耗尽**：  
   Linux 系统内核默认的 `net.core.somaxconn` 仅为 128 或 1024，`tcp_max_syn_backlog` 较低。在高并发大模型请求、健康探测与浏览器并发连接时，SYN 握手队列瞬间被占满，内核直接丢弃新的 TCP SYN 请求包。
2. **Cloudflare 边缘超时判定**：  
   Cloudflare 边缘节点向源站 IP 发送 SYN 包后，因源站内核队列已满被丢弃，在超时时间内未收到 SYN-ACK，Cloudflare 立即判定源站连接失败并返回 522。
3. **Nginx Worker 连接数不足**：  
   默认 `worker_connections 768;` 极易在高并发持久连接（SSE 流式）下耗尽。

#### 预防与工程标准
所有生产机初始化与运维时，必须持久化应用以下 Linux 内核参数（写入 `/etc/sysctl.conf` 并 `sysctl -p`）：
```ini
net.core.somaxconn = 16384
net.ipv4.tcp_max_syn_backlog = 16384
net.core.netdev_max_backlog = 16384
net.ipv4.tcp_tw_reuse = 1
net.ipv4.ip_local_port_range = 1024 65535
net.ipv4.tcp_fin_timeout = 15
```
同时在 `/etc/nginx/nginx.conf` 中优化连接池：
```nginx
events {
    worker_connections 16384;
    multi_accept on;
    use epoll;
}
```

---

### 3. 大模型 API 响应头溢出

#### 故障现象
前端聊天流式或 API 网关请求返回 502 Bad Gateway，Nginx 错误日志显示：
`upstream sent too big header while reading response header from upstream`

#### 底层根因剖析
Nginx 默认分配给反向代理上游响应头的缓冲区大小仅为 4KB 或 8KB。在接入带有长 JWT Token、复杂安全 Cookie、大模型元数据或长报错信息的响应时，头信息尺寸超过 8KB，Nginx 自动中断请求并返回 502。

#### 预防与工程标准
所有反向代理 `location` 必须声明大缓冲区容纳策略：
```nginx
proxy_buffer_size 128k;
proxy_buffers 4 256k;
proxy_busy_buffers_size 256k;
```

---

### 4. 聚合平台 Iframe 沙箱限制导致登录/下载失效

#### 故障现象
在 `20020723.xyz` 聚合平台内通过 iframe 嵌入 `image.20020723.xyz` 或 `videogen.20020723.xyz` 时，出现：
- LocalStorage 写入受阻，登录状态每次刷新丢失；
- 点击「下载图片」或「下载视频」无响应或控制台报错；
- 无法进入全屏。

#### 底层根因剖析
给 iframe 误加了过度严格的 `sandbox="allow-scripts allow-same-origin"` 限制，浏览器默认禁止了 `downloads`、`modals`、`popups` 以及跨文档通信权限。

#### 预防与工程标准
聚合主站与子应用同属于第一方产品矩阵（`*.20020723.xyz`），完全受信任。
1. **原则**：直接使用完全开放的 iframe 嵌入，或者声明完整宽容沙箱属性：
   ```html
   <iframe src="https://image.20020723.xyz/"
           allow="clipboard-write; fullscreen; camera; microphone"
           loading="lazy"></iframe>
   ```
2. **跨域存储互通**：使用标准 `window.postMessage` API 实现主应用与子 iframe 的凭证同步与状态联动。

---

### 5. 移动端视口溢出与选项卡竖向折行穿透

#### 故障现象
在 iPhone 或 Android 竖屏访问聚合平台时：
- 顶部导航栏被 Logo 标题与 4 个功能选项卡挤爆，文字竖向换行（如“网\n页\n对\n话”）；
- 选项卡覆盖下方的对话模型选择栏；
- “底色”和“登录”按钮被挤出屏幕右边缘。

#### 底层根因剖析
PC 端默认采用 `flex-wrap: nowrap` 且各项有大横向外边距。在屏幕宽度小于 480px 时未针对 Logo 文本、选项卡内边距进行缩减与横向滚动隔离。

#### 预防与工程标准
1. **移动端 Logo 精简**：屏幕宽度 `< 768px` 时，隐藏 Logo 冗余文字（`brand-title`, `brand-badge`），只保留 28px 高清纯图标。
2. **选项卡胶囊滚动**：导航栏选项卡采用横向弹性胶囊滑动，禁止文字折行：
   ```css
   .hub-tabs {
     overflow-x: auto;
     white-space: nowrap;
     scrollbar-width: none;
   }
   .hub-tab {
     white-space: nowrap;
     flex-shrink: 0;
   }
   ```
3. **双重断点适配**：移动端单独定义紧凑型 Header（52px 高度），对话输入区域适配软键盘安全距离。

---

### 6. Edge / Windows 系统无障碍导致 Canvas 粒子球静止或白屏

#### 故障现象
部分用户使用 Microsoft Edge 或 Windows 笔记本访问时，首页没有出现流动的粒子地球，或者显示为空白区域。

#### 底层根因剖析
1. **系统减弱动态效果设置**：Windows 系统设置若勾选了“关闭动画效果”，Edge 会向页面抛出 `(prefers-reduced-motion: reduce)` 为 `true`。原粒子引擎检测到该标志后直接取消了 `requestAnimationFrame` 循环。
2. **隐藏标签页初始尺寸为 0**：聚合平台默认展示对话框，官网主页处于 `display: none`。在页面加载时 `getBoundingClientRect()` 计算出 `width: 0, height: 0`，粒子引擎初始化退化为 1x1 画布后挂起，标签页切换时未主动唤醒。

#### 预防与工程标准
1. **画布托底容错**：在粒子引擎内部计算尺寸时，若测得宽度小于 10px，自动以 `window.innerWidth * 0.92` 与 `210px` 作为安全保底，严禁画布塌陷为 1x1。
2. **显式传入 `ignoreReducedMotion: true`**：对于地球自转等环境装饰性背景，不受无障碍系统强制冻结限制。
3. **标签页切换主动唤醒**：在 `switchView('portal')` 时调用暴露的 `pgsHandle.resize()` 与 `pgsHandle.wake()`，确保在任何浏览器切换可见时立即恢复 60fps 渲染。

---

### 7. 生产标准 Nginx 模版与系统参数配置速查

#### `/etc/nginx/sites-available/default` 核心配置标准
```nginx
# 1. 聚合主站 (20020723.xyz)
server {
    listen 80;
    listen 443 ssl http2;
    server_name 20020723.xyz www.20020723.xyz;

    ssl_certificate /etc/letsencrypt/live/20020723.xyz/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/20020723.xyz/privkey.pem;

    root /var/www/geo/20020723.xyz;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
        add_header Cache-Control "no-cache, must-revalidate";
    }

    location ~* \.(jpg|jpeg|png|gif|ico|css|js|svg)$ {
        expires 7d;
        add_header Cache-Control "public, max-age=604800";
    }
}

# 2. 图像工作台反向代理 (image.20020723.xyz)
server {
    listen 80;
    listen 443 ssl http2;
    server_name image.20020723.xyz;

    ssl_certificate /etc/letsencrypt/live/20020723.xyz/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/20020723.xyz/privkey.pem;

    location / {
        proxy_pass http://127.0.0.1:21789;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        proxy_buffer_size 128k;
        proxy_buffers 4 256k;
        proxy_busy_buffers_size 256k;
    }
}
```

---
*本文档为生产最高准则，后续所有改动均须遵循上述规约。*
