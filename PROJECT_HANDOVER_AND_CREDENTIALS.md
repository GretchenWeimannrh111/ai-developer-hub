# SuperFast 生态站与 GEO 建设工程交接文档

> **归档日期**：2026-09-24  
> **项目范围**：SuperFast 生态门户建设、大模型表述校准、动效 1:1 复刻、GEO/SEO 矩阵搭建、服务器部署与多平台自动化发布  
> **代码仓库目录**：`/Users/luyuan/1workshop/antigravity/GEO/`

---

## 一、目前已完成的工作总结

### 1. 门户主站重构与视觉体验升级（`https://20020723.xyz/`）
- **现代化双色响应式架构**：重构深浅（Twilight / Cream）双主题设计，支持中英文即时切换，移动端/桌面端弹性适配。
- **大模型表述全面校准与时效修复**：
  - 修正了关于 SuperFast 绘图工作台的过时表述，明确标注接入前沿模型矩阵：**GPT-Image-2.5**、**Grok 生图引擎**、DALL-E 3、Midjourney 等；
  - 核心 API 网关聚焦毫秒级低延迟、高并发弹性集群，全兼容 OpenAI 格式；
  - 视频工坊突出首尾关键帧过渡锁死、4~12s 超长运镜、角色原图一致性等核心卖点；
  - 梦言（DreamTalk）突出超长记忆链与多模态情感陪伴；
  - 开发者知识库聚焦工程落地最佳实践与长尾深度专栏。
- **界面降噪与极简排布**：
  - 去除底部复杂的 Sitemap 和冗余外部友链，保持极简大气与高级质感；
  - 调整文字层级，优化 Banner 排版与留白；
  - **HOT MODELS 跑马灯与滚动条优化**：将原本挤在左侧的 "HOT MODELS" 标签独立提取并上移居中，设计为带动态呼吸脉冲点的胶囊小标题，跑马灯采用双轨无缝平滑滚动与两端柔和渐变渐隐（mask-fade）；全局适配现代平滑超窄滚动条（支持深浅色自适应）。
- **100% 官方模型广场对齐（拒绝老旧模型，真实精准映射）**：
  - 以官方系统原生模型广场（[`api.20020723.xyz/model-plaza`](https://api.20020723.xyz/model-plaza)）接口为唯一准据，全面清除 GPT-4o、Claude 3.5 Sonnet、DALL-E 3 等一切过时模型；
  - 严格映射 6 大官方专属分组：**图像生成**（最终倍率 0.3，含 `gpt-image-2`、`gpt-image-2.5-flare`、`gpt-image-2.5-sunburst` 4K）、**Grok 旗舰**（最终倍率 0.15，含 `grok-4.7`、`grok-imagine-image-2.0` 等 8 款）、**Anthropic-Claude**（最终倍率 0.3，含 `claude-opus-5`、`claude-sonnet-4-6` 等 5 款）、**OpenAI**（最终倍率 0.3，含 `gpt-6-astra`、`gpt-6-sol`、`codex-auto-review` 等 6 款）、**Gemini**（最终倍率 0.15，含 `gemini-3.7-flash` 等 4 款）、**福利分组**（最终倍率 0.03，含 `deepseek-v4.1-flash`、`glm-5.3-flash`、`gpt-oss-20b` 等 7 款），共计 33 款前沿模型；
  - 全量上线到官网首页、[`models.html`](https://20020723.xyz/models.html) 与 [`llms.txt`](https://20020723.xyz/llms.txt)。
- **Banner 核心行动按钮与「共建 Agent 生态」矩阵**：
  - **Banner 核心双 CTA 按钮**：Banner 文案下方增设高亮主行动按钮「⚡ 立刻使用」（直达 `https://api.20020723.xyz/login`）与次行动按钮「📋 查看模型」（直达 `https://20020723.xyz/models.html`），支持双色模式与双语切换；
  - **「共建 Agent 生态」矩阵**：对齐前沿开发者工具流，上线 12 款主流代码 Agent 与客户端展示胶囊（排除 MiMo Desktop，Codex 与 Claude Code 置于最前面，MiMo Code 放在最后），采用 4x3 响应式弹性网格布局，适配暗色与亮色无缝切换。
- **核心主打定价与商业优势（必须牢牢铭记）**：
  - **基础充值汇率**：**0.3 元人民币 = 1 美元额度**（即 1 USD 额度仅需 ¥0.30，相比银行常规汇率立省 95% 以上，按量透明扣除，无隐形门槛）；
  - **爆款开发者 Coding Plan 月卡**：**200 元人民币 / 月，独享 3000 美元 GPT 系列超大额度**（折合 1 USD 额度仅需 ¥0.067，专为高强度编程、Cursor、Cline、CI 门禁与自动化 Agent 打造）；
  - **超级叠加效应**：在 0.3 元充值比例与 200 元月卡基础上，各分组还享受 0.03 ~ 0.3 倍超低倍率，打造全行业断层领先的性价比优势。

### 2. 粒子动效 1:1 深度复刻（逆向工程对齐）
- **方法论裁决**：遵循 `website-rebuild-skill` 原则（“以源码为唯一裁决，不凭肉眼调效果，源站有的都要有，源站没有的不发明”）。
- **底层引擎提取**：从 `https://api.pgsgrove.com/assets/index-Cz5fgE-j.js` 逆向完整提取 Phoenix Grove Systems 粒子引擎，封装为独立的 [`portal/pgs-particle.js`](file:///Users/luyuan/1workshop/antigravity/GEO/portal/pgs-particle.js)。
- **核心算法对齐（Earth Formation）**：
  - 采用原版 3D 大陆自转球体算法（$180 \times 90$ 经纬度陆地/海洋双层粒子网格与地轴倾角公转）；
  - 陆地节点随机映射五彩调色板（橙/绿/红/紫/黄），海洋节点渲染青蓝/深蓝微光；
  - 开启鼠标物理向心吸附引力场（`gather` 模式），提供平滑的动量阻尼回弹；
  - 启用 `adaptive: true` 自动帧率补偿，在低配设备或掉帧时智能减少粒子数与流速。
- **布局防遮挡与光标修复**：
  - 粒子舞台独立置于 Banner 文字上方（高度 210px），彻底消除粒子与文本标题的视觉重叠；
  - 移除了残留的 `cursor: crosshair` 十字准星，恢复正常系统的指针交互；
  - 开启事件穿透（`pointer-events: none;`），确保在交互动效的同时不阻挡文本选中与卡片点击。

### 3. GEO / SEO 高权重矩阵建设
- 构建了静态页面生成引擎（SSG），输出涵盖架构设计、API 防伪、成本优化路由、Cline/Cursor 工具流等 13 篇长尾技术实战专栏。
- 自动化生成高密度结构化数据：
  - 完整 Sitemap 矩阵（`sitemap.xml`, `sitemap-matrix.xml`, `sitemap-pages.xml`, `sitemap-faq.xml`）；
  - 搜索引擎友好的 `robots.txt`、大模型抓取专用的 `llms-full.txt`；
  - 符合 Schema.org 规范的 JSON-LD 结构化标签。

### 4. 全球平台外链与自动化分发
- 编写并部署了面向 GitHub 和 Dev.to 的自动化发布管道，实现工程文章与 Canonical 权威源的自动绑定。
- **全网分发矩阵达成**：已累计向 Dev.to 发布 **27 篇深度中英文实战长文**（18 篇中文 + 9 篇英文），全量经过生产环境验证；
- **GitHub 开源仓库同步**：已将全套中英文文章与多模型架构指南同步推送至 [GitHub: GretchenWeimannrh111/ai-developer-hub](https://github.com/GretchenWeimannrh111/ai-developer-hub)，README 中已嵌入全部 27 篇 Dev.to 权威链接与模型目录。

---

## 二、相关网站与服务地址清单

| 服务 / 站点名称 | 访问地址 | 说明与定位 |
| :--- | :--- | :--- |
| **门户聚合主站** | [https://20020723.xyz/](https://20020723.xyz/) | 统一生态入口（当前生产上线地址） |
| **官方模型目录与定价** | [https://20020723.xyz/models.html](https://20020723.xyz/models.html) | 全量大模型实时支持清单与定价矩阵（权威白皮书） |
| **SuperFast API 平台** | [https://api.20020723.xyz/](https://api.20020723.xyz/) | 大模型中转分发与 API 接入中心 |
| **SuperFast 绘图工作台** | [https://image.20020723.xyz/](https://image.20020723.xyz/) | 文生图/图生图/智能扩图工作台 |
| **SuperFast 视频创作工坊** | [https://videogen.20020723.xyz/](https://videogen.20020723.xyz/) | 电影级首尾帧控制与视频运镜平台 |
| **梦言 DreamTalk** | [https://dreamtalk.cc.cd/](https://dreamtalk.cc.cd/) | 独立创新情感陪伴与虚拟角色对话产品 |
| **GEO 镜像/内容基站** | [https://superfast.us.ci](https://superfast.us.ci) | 静态技术专栏与 SEO/GEO 基站源站 |
| **官方卡密商城** | [https://9.plus/shop/SuperFast/rqa6n7](https://9.plus/shop/SuperFast/rqa6n7) | 自动化 24 小时充值商城兑换通道 |
| **官方腾讯文档** | [https://docs.qq.com/aio/DSVN2cG1tQmRPamZZ](https://docs.qq.com/aio/DSVN2cG1tQmRPamZZ) | 使用指南、模型列表与服务状态 |
| **参考对标源站** | [https://api.pgsgrove.com/plan](https://api.pgsgrove.com/plan) | 粒子引擎逆向对比与参考来源 |

---

## 三、服务器连接信息与凭证

### 1. 生产服务器 1（当前主站 `20020723.xyz` 部署机）
- **服务器 IP**：`85.137.246.78`
- **SSH 端口**：`22`
- **登录用户名**：`root`
- **登录密码**：`qompSOAD4292`
- **Web 根目录**：`/var/www/geo/20020723.xyz/`
- **环境服务**：Nginx、Let's Encrypt SSL
- **快捷管理脚本**：[`ssh_client_85.py`](file:///Users/luyuan/1workshop/antigravity/GEO/ssh_client_85.py)

### 2. 生产服务器 2（辅站/内容镜像机 `superfast.us.ci`）
- **服务器 IP**：`163.7.6.109`
- **SSH 端口**：`22`
- **登录用户名**：`root`
- **登录密码**：`Aa121469249`
- **Web 根目录**：`/var/www/geo/`
- **环境服务**：Nginx、Let's Encrypt SSL
- **快捷管理脚本**：[`ssh_client.py`](file:///Users/luyuan/1workshop/antigravity/GEO/ssh_client.py)

---

## 四、第三方平台凭证与账号权限

### 1. GitHub 自动化推送凭证
- **GitHub 账户**：`GretchenWeimannrh111`
- **Personal Access Token (PAT)**：`ghp_****************************`
- **远程仓库地址**：`https://github.com/GretchenWeimannrh111/superfast-ai-guide-2026`
- **自动化推送脚本**：[`push_to_github.py`](file:///Users/luyuan/1workshop/antigravity/GEO/push_to_github.py)

### 2. Dev.to 开放平台 API 凭证
- **开发者 API 密钥**：`Cz3sWPs1nguCeJdc37wZbkWD`
- **自动化发布脚本**：[`batch_publish_devto.py`](file:///Users/luyuan/1workshop/antigravity/GEO/batch_publish_devto.py)
- **用途**：用于批量分发技术专栏，建立海外高权重反向链接并附带 `canonical_url`。

### 3. 客服与商务支持渠道
- **官方技术支持 QQ**：`2796802957`
- **客服企业微信二维码图床**：`https://img.ofc.ccwu.cc/file/1776333014782_qw2.png`

---

## 五、本地项目工程目录结构

```text
/Users/luyuan/1workshop/antigravity/GEO/
├── portal/                          # 生产前端门户静态资源
│   ├── index.html                   # 官网入口主页（双语/双色/粒子/卡片）
│   └── pgs-particle.js              # 逆向复刻的 Phoenix Grove Systems 粒子引擎
├── dist/                            # SSG 自动生成的完整站点与 GEO 专栏
│   ├── articles/                    # 13 篇长尾深度技术文章 HTML
│   ├── sitemap*.xml                 # 4 套搜索引擎专用站点地图
│   ├── robots.txt                   # 爬虫指引配置
│   └── llms-full.txt                # 大语言模型与 AI 智能体检索数据源
├── external_articles/               # 针对外发平台优化的 Markdown 专栏库
├── github_repo/                     # 同步至 GitHub 的独立 Git 开源项目工程
├── generate_site.py                 # GEO 静态页面生成引擎
├── build_all.py                     # 全站编译构建流水线
├── ssh_client_85.py                 # 服务器 85.137.246.78 自动化 SSH 脚本
├── ssh_client.py                    # 服务器 163.7.6.109 自动化 SSH 脚本
├── push_to_github.py                # GitHub 一键自动化推送工具
├── batch_publish_devto.py           # Dev.to 批量自动发布脚本
└── PROJECT_HANDOVER_AND_CREDENTIALS.md # 本交接总结文档
```

---

## 六、常用运维与部署命令速查

### 1. 同步前端主站代码至生产机（85.137.246.78）
```bash
python3 -c "
import paramiko
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('85.137.246.78', port=22, username='root', password='qompSOAD4292')
sftp = ssh.open_sftp()
sftp.put('/Users/luyuan/1workshop/antigravity/GEO/portal/index.html', '/var/www/geo/20020723.xyz/index.html')
sftp.put('/Users/luyuan/1workshop/antigravity/GEO/portal/pgs-particle.js', '/var/www/geo/20020723.xyz/pgs-particle.js')
sftp.close()
ssh.close()
print('Deploy complete!')
"
```

### 2. 检查线上主站 HTTP 响应与证书
```bash
curl -I -k https://20020723.xyz/
```

### 3. 一键编译并生成全套 GEO 专栏
```bash
python3 /Users/luyuan/1workshop/antigravity/GEO/build_all.py
```

### 4. 聚合平台与全矩阵一键构建部署
```bash
python3 /Users/luyuan/1workshop/antigravity/GEO/build_aggregator.py
python3 /Users/luyuan/1workshop/antigravity/GEO/deploy_all_85.py
```

---

## 七、生产环境运维复盘与故障预防白皮书 (必须严格遵守)

> 详见权威工程白皮书：[`docs/INCIDENT_LOG_AND_PREVENTION.md`](file:///Users/luyuan/1workshop/antigravity/GEO/docs/INCIDENT_LOG_AND_PREVENTION.md)

1. **Cloudflare 301 重定向死循环**：所有代理到本地容器/内部端口的子域名（如 `image.20020723.xyz`），Nginx 80 端口与 443 端口必须同时配置 `proxy_pass`，严禁在 80 端口配置全局无条件 301 重定向。
2. **Cloudflare 522 超时与 SYN 丢包**：Linux 内核必须持久化配置 `net.core.somaxconn = 16384`、`net.ipv4.tcp_max_syn_backlog = 16384`、`net.ipv4.tcp_tw_reuse = 1`，Nginx `worker_connections 16384`。
3. **大模型 API 502 响应头溢出**：反向代理必须声明 `proxy_buffer_size 128k; proxy_buffers 4 256k; proxy_busy_buffers_size 256k;`。
4. **聚合 Iframe 沙箱权限陷阱**：自家第一方子域名必须使用开放 iframe 嵌入或宽容沙箱，禁止阻断本地存储与图片/视频下载。
5. **移动端 Viewport 溢出防线**：导航栏在宽度 `< 768px` 时必须隐藏 Logo 文本只留 28px 图标，选项卡必须使用横向滚动胶囊，禁止文字折行。
6. **Edge / Windows 无障碍粒子球兼容**：底层粒子引擎必须设置 `ignoreReducedMotion: true` 与视口保底尺寸，并在切换标签页时主动调用 `forceWake()`。

