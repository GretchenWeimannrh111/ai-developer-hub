#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
三级分层级联路由器 (Tiered Cascade Router)
- 0.03 倍率福利层：处理轻量分类、格式校验与摘要
- 0.15 倍率均衡层：处理常规问答与中长文本
- 0.30 倍率旗舰层：处理核心编码与复杂决策
"""

import asyncio
import httpx
import logging
import os
from typing import Dict, Any, List

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("CascadeRouter")

API_BASE_URL = os.getenv("API_BASE_URL", "https://api.20020723.xyz/v1/chat/completions")
API_KEY = os.getenv("API_KEY", "sk-your-superfast-token")

MODEL_TIERS = {
    "tier_economy": "deepseek-v4.1-flash",  # 0.03 极低倍率福利模型
    "tier_standard": "grok-4.6",            # 0.15 均衡推理模型
    "tier_premium": "claude-sonnet-4-6"     # 0.3 顶配核心模型
}

class CascadeRouter:
    def __init__(self, api_key: str, base_url: str):
        self.api_key = api_key
        self.base_url = base_url
        self.client = httpx.AsyncClient(timeout=60.0)

    def evaluate_task_complexity(self, messages: List[Dict[str, str]]) -> str:
        total_chars = sum(len(m.get("content", "")) for m in messages)
        last_prompt = messages[-1].get("content", "").lower() if messages else ""

        if any(keyword in last_prompt for keyword in ["refactor architecture", "重构核心模块", "证明该定理", "security audit"]):
            return "tier_premium"

        if total_chars > 3000 or any(keyword in last_prompt for keyword in ["总结文档", "对比分析", "提取大纲"]):
            return "tier_standard"

        return "tier_economy"

    async def execute_request(self, messages: List[Dict[str, str]], fallback: bool = True) -> Dict[str, Any]:
        tier = self.evaluate_task_complexity(messages)
        target_model = MODEL_TIERS[tier]
        logger.info(f"Task dispatched to [{tier}] using model: {target_model}")

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": target_model,
            "messages": messages,
            "temperature": 0.3
        }

        try:
            resp = await self.client.post(self.base_url, headers=headers, json=payload)
            if resp.status_code == 200:
                return resp.json()
            else:
                logger.warning(f"Model {target_model} returned {resp.status_code}: {resp.text}")
        except Exception as e:
            logger.error(f"Error calling {target_model}: {str(e)}")

        if fallback and tier != "tier_premium":
            logger.info("Triggering fallback promotion to tier_premium...")
            payload["model"] = MODEL_TIERS["tier_premium"]
            resp = await self.client.post(self.base_url, headers=headers, json=payload)
            return resp.json()

        raise RuntimeError("All routing tiers exhausted.")

async def main():
    router = CascadeRouter(api_key=API_KEY, base_url=API_BASE_URL)
    task_extract = [{"role": "user", "content": "请从以下文本提取公司名称与金额：张三向北京某科技有限公司投资了500万元。"}]
    res1 = await router.execute_request(task_extract)
    print("Task 1 Result:", res1["choices"][0]["message"]["content"])

if __name__ == "__main__":
    asyncio.run(main())
