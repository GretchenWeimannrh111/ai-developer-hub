#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
大模型 API 自动化性能压测与防坑鉴真脚本
- 测量首字延迟（TTFT - Time to First Token）
- 测量每秒 Token 吞吐（TPS）
- 真实流式数据包检验
- 逻辑与反事实探针检验（防模型被偷换/降级）
"""

import time
import httpx
import json
import os

API_ENDPOINT = os.getenv("API_BASE_URL", "https://api.20020723.xyz/v1/chat/completions")
API_KEY = os.getenv("API_KEY", "sk-your-test-token")
TEST_MODEL = os.getenv("TEST_MODEL", "claude-sonnet-4-6")

def run_benchmark(model_name: str):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": model_name,
        "messages": [
            {"role": "system", "content": "你是一个严格的技术鉴真探针。请如实、简洁回答。"},
            {"role": "user", "content": "请用一段话解释为什么周树人与鲁迅没有在现实中见过面？并顺带输出一段快速斐波那契数列 Python 代码。"}
        ],
        "temperature": 0.1,
        "stream": True
    }

    print("\n==========================================")
    print(f"开始测试模型: {model_name}")
    print(f"测试端点: {API_ENDPOINT}")
    print("==========================================")

    start_time = time.time()
    first_token_time = None
    chunks_count = 0
    full_content = []

    try:
        with httpx.Client(timeout=30.0) as client:
            with client.stream("POST", API_ENDPOINT, headers=headers, json=payload) as response:
                if response.status_code != 200:
                    print(f"❌ 接口请求异常! HTTP 状态码: {response.status_code}")
                    print(response.read().decode('utf-8'))
                    return

                for line in response.iter_lines():
                    if line.startswith("data: ") and line != "data: [DONE]":
                        chunk_data = json.loads(line[6:])
                        delta = chunk_data["choices"][0]["delta"].get("content", "")
                        if delta:
                            if first_token_time is None:
                                first_token_time = time.time()
                            full_content.append(delta)
                            chunks_count += 1

        end_time = time.time()

        ttft = (first_token_time - start_time) if first_token_time else 0
        total_time = end_time - start_time
        total_chars = len("".join(full_content))
        approx_tokens = total_chars / 1.5
        tps = approx_tokens / (total_time - ttft) if (total_time - ttft) > 0 else 0

        print(f"✔ 首字延迟 (TTFT): {ttft:.3f} 秒 {'(优秀 < 0.8s)' if ttft < 0.8 else '(一般)'}")
        print(f"✔ 整体耗时: {total_time:.3f} 秒")
        print(f"✔ 流式推送分块数: {chunks_count} 次 {'(真实流式)' if chunks_count > 10 else '(疑似伪流式缓存)'}")
        print(f"✔ 估算生成吞吐: {tps:.1f} tokens/s")
        print("------------------------------------------")
        print("模型回答内容摘要 (前120字):")
        print("".join(full_content)[:120] + "...")
        print("==========================================\n")

    except Exception as e:
        print(f"❌ 运行测试出错: {str(e)}")

if __name__ == "__main__":
    run_benchmark(TEST_MODEL)
