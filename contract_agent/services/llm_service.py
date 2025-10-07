import os
from zhipuai import ZhipuAI

client = ZhipuAI(api_key="39d0b16bd58f44fa85915d7a84d9b691.5AY5yC4qLrrKTaOE")

def run_contract_review(contract_text: str) -> str:
    # 读取Prompt模板
    with open("prompts/contract_review.txt", "r", encoding="utf-8") as f:
        prompt_template = f.read()

    prompt = f"{prompt_template}\n\n【合同文本开始】\n<<<\n{contract_text}\n>>>\n"

    # 方案1：调用本地Ollama / LM Studio / GPT部署
    # response = requests.post("http://localhost:11434/api/generate", json={"model": "llama3", "prompt": prompt})

    # 方案2：调用 API

    response = client.chat.completions.create(
        model="glm-4.5", # 可换为 glm-4-flash / glm-4-air 视速度成本选择
        messages=[
            {"role": "system", "content": "你是一名资深企业法务顾问，负责合同风险审查与优化。"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
        max_tokens=4096,
    )

    return response.choices[0].message.content

