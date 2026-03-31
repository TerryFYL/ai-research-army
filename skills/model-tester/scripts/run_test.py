#!/usr/bin/env python3
"""
模型测试自动化脚本
支持调用不同模型API执行综合性任务测试
"""

import os
import json
import yaml
import time
import argparse
import sqlite3
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any

# API 客户端（需要安装对应的SDK）
try:
    import openai
except ImportError:
    openai = None

try:
    import anthropic
except ImportError:
    anthropic = None

try:
    import google.generativeai as genai
except ImportError:
    genai = None

SKILL_DIR = Path(__file__).parent.parent
CONFIG_PATH = SKILL_DIR / "config" / "models.yaml"
DB_PATH = SKILL_DIR / "test_records.db"
OUTPUT_DIR = SKILL_DIR / "test_outputs"


def load_config() -> dict:
    """加载配置文件"""
    with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)

    # 替换环境变量
    for model_name, model_config in config.get('models', {}).items():
        api_key = model_config.get('api_key', '')
        if api_key.startswith('${') and api_key.endswith('}'):
            env_var = api_key[2:-1]
            model_config['api_key'] = os.environ.get(env_var, '')

    return config


def load_prompt(task_name: str, config: dict) -> str:
    """加载任务Prompt"""
    task_config = config.get('tasks', {}).get(task_name)
    if not task_config:
        raise ValueError(f"未找到任务配置: {task_name}")

    prompt_file = SKILL_DIR / task_config['prompt_file']
    with open(prompt_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # 提取 ``` 之间的prompt内容
    import re
    match = re.search(r'## 完整 Prompt\s*```\s*(.*?)\s*```', content, re.DOTALL)
    if match:
        return match.group(1).strip()

    # 如果没有找到特定格式，返回整个内容
    return content


def call_openai(model_config: dict, prompt: str) -> tuple[str, float]:
    """调用 OpenAI API"""
    if not openai:
        raise ImportError("请安装 openai: pip install openai")

    client = openai.OpenAI(
        api_key=model_config['api_key'],
        base_url=model_config.get('base_url')
    )

    start_time = time.time()
    response = client.chat.completions.create(
        model=model_config['model_id'],
        messages=[{"role": "user", "content": prompt}],
        max_tokens=model_config.get('max_tokens', 8000),
        temperature=model_config.get('temperature', 0.7)
    )
    elapsed_time = time.time() - start_time

    return response.choices[0].message.content, elapsed_time


def call_anthropic(model_config: dict, prompt: str) -> tuple[str, float]:
    """调用 Anthropic API"""
    if not anthropic:
        raise ImportError("请安装 anthropic: pip install anthropic")

    client = anthropic.Anthropic(api_key=model_config['api_key'])

    start_time = time.time()
    response = client.messages.create(
        model=model_config['model_id'],
        max_tokens=model_config.get('max_tokens', 8000),
        messages=[{"role": "user", "content": prompt}]
    )
    elapsed_time = time.time() - start_time

    return response.content[0].text, elapsed_time


def call_google(model_config: dict, prompt: str) -> tuple[str, float]:
    """调用 Google Gemini API"""
    if not genai:
        raise ImportError("请安装 google-generativeai: pip install google-generativeai")

    genai.configure(api_key=model_config['api_key'])
    model = genai.GenerativeModel(model_config['model_id'])

    start_time = time.time()
    response = model.generate_content(prompt)
    elapsed_time = time.time() - start_time

    return response.text, elapsed_time


def call_model(model_name: str, model_config: dict, prompt: str) -> tuple[str, float]:
    """根据provider调用对应的API"""
    provider = model_config.get('provider', '').lower()

    if provider == 'openai':
        return call_openai(model_config, prompt)
    elif provider == 'anthropic':
        return call_anthropic(model_config, prompt)
    elif provider == 'google':
        return call_google(model_config, prompt)
    elif provider in ['zhipu', 'deepseek']:
        # 智谱和DeepSeek兼容OpenAI格式
        return call_openai(model_config, prompt)
    else:
        raise ValueError(f"不支持的provider: {provider}")


def save_output(model_name: str, task_name: str, response: str, elapsed_time: float):
    """保存测试输出"""
    OUTPUT_DIR.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{task_name}_{model_name}_{timestamp}.md"
    output_path = OUTPUT_DIR / filename

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(f"# 测试结果: {task_name}\n\n")
        f.write(f"**模型**: {model_name}\n")
        f.write(f"**时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"**耗时**: {elapsed_time:.2f}秒\n\n")
        f.write("---\n\n")
        f.write("## 模型输出\n\n")
        f.write(response)

    print(f"输出已保存: {output_path}")
    return output_path


def save_to_db(model_name: str, task_name: str, elapsed_time: float,
               output_path: str, config: dict):
    """保存测试记录到数据库"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    model_config = config.get('models', {}).get(model_name, {})
    nickname = model_config.get('nickname', '')

    cursor.execute("""
    INSERT INTO test_records
    (test_date, test_type, model_a, task_name, result_summary, insights)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (
        datetime.now().strftime("%Y-%m-%d"),
        "comprehensive_task",
        model_name,
        task_name,
        f"耗时: {elapsed_time:.2f}秒, 输出: {output_path}",
        f"模型昵称: {nickname}"
    ))

    conn.commit()
    conn.close()
    print(f"记录已保存到数据库")


def run_test(model_name: str, task_name: str, save: bool = True):
    """执行单个测试"""
    config = load_config()

    # 检查模型配置
    model_config = config.get('models', {}).get(model_name)
    if not model_config:
        print(f"错误: 未找到模型配置 '{model_name}'")
        print(f"可用模型: {list(config.get('models', {}).keys())}")
        return

    if not model_config.get('api_key'):
        print(f"错误: 模型 '{model_name}' 的 API Key 未设置")
        print(f"请设置环境变量或在 config/models.yaml 中配置")
        return

    # 加载Prompt
    try:
        prompt = load_prompt(task_name, config)
    except Exception as e:
        print(f"错误: 加载任务Prompt失败 - {e}")
        return

    print(f"\n{'='*60}")
    print(f"开始测试: {task_name}")
    print(f"模型: {model_name} ({model_config.get('nickname', '')})")
    print(f"{'='*60}\n")

    # 调用模型
    try:
        response, elapsed_time = call_model(model_name, model_config, prompt)
        print(f"✅ 调用成功，耗时: {elapsed_time:.2f}秒")

        if save:
            output_path = save_output(model_name, task_name, response, elapsed_time)
            save_to_db(model_name, task_name, elapsed_time, str(output_path), config)

        # 打印响应预览
        print(f"\n--- 响应预览 (前500字) ---\n")
        print(response[:500])
        if len(response) > 500:
            print(f"\n... (共 {len(response)} 字)")

    except Exception as e:
        print(f"❌ 调用失败: {e}")


def run_cross_validation(model_a: str, model_b: str, task_name: str):
    """执行交叉验证测试"""
    config = load_config()
    prompt = load_prompt(task_name, config)

    print(f"\n{'='*60}")
    print(f"交叉验证测试: {task_name}")
    print(f"模型A: {model_a}")
    print(f"模型B: {model_b}")
    print(f"{'='*60}\n")

    # Step 1: 模型A完成任务
    print(f"\n[Step 1] {model_a} 执行任务...")
    model_a_config = config.get('models', {}).get(model_a)
    response_a, time_a = call_model(model_a, model_a_config, prompt)
    save_output(model_a, task_name, response_a, time_a)

    # Step 2: 模型B评审
    print(f"\n[Step 2] {model_b} 评审代码...")
    review_prompt = f"""请评审以下代码，从以下维度进行分析：
1. 逻辑正确性（是否有bug、边界条件处理、内存泄漏等）
2. 代码质量（可读性、模块化、命名规范）
3. 性能问题（潜在的性能瓶颈）
4. 安全问题（是否有安全隐患）
5. 改进建议

被评审的代码：
```
{response_a}
```
"""
    model_b_config = config.get('models', {}).get(model_b)
    review_b, time_b = call_model(model_b, model_b_config, review_prompt)
    save_output(model_b, f"{task_name}_review_of_{model_a}", review_b, time_b)

    # Step 3: 模型A回应评审
    print(f"\n[Step 3] {model_a} 回应评审...")
    response_prompt = f"""以下是对你代码的评审意见，请逐条回应：
1. 如果你认同，说明如何修正
2. 如果你不认同，说明理由

评审意见：
{review_b}
"""
    response_to_review, time_r = call_model(model_a, model_a_config, response_prompt)
    save_output(model_a, f"{task_name}_response_to_review", response_to_review, time_r)

    print(f"\n✅ 交叉验证完成")
    print(f"输出目录: {OUTPUT_DIR}")


def list_models():
    """列出可用模型"""
    config = load_config()
    print("\n可用模型:")
    print("-" * 60)
    for name, cfg in config.get('models', {}).items():
        has_key = "✅" if cfg.get('api_key') else "❌"
        print(f"  {has_key} {name:<20} {cfg.get('nickname', '')}")
    print("-" * 60)


def list_tasks():
    """列出可用任务"""
    config = load_config()
    print("\n可用任务:")
    print("-" * 60)
    for name, cfg in config.get('tasks', {}).items():
        print(f"  • {name}: {cfg.get('name', '')}")
    print("-" * 60)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="模型测试自动化脚本")
    subparsers = parser.add_subparsers(dest="command")

    # 单模型测试
    test_parser = subparsers.add_parser("test", help="执行单模型测试")
    test_parser.add_argument("--model", "-m", required=True, help="模型名称")
    test_parser.add_argument("--task", "-t", required=True, help="任务名称")
    test_parser.add_argument("--no-save", action="store_true", help="不保存结果")

    # 交叉验证
    cross_parser = subparsers.add_parser("cross", help="执行交叉验证")
    cross_parser.add_argument("--model-a", "-a", required=True, help="模型A")
    cross_parser.add_argument("--model-b", "-b", required=True, help="模型B")
    cross_parser.add_argument("--task", "-t", required=True, help="任务名称")

    # 列出可用资源
    subparsers.add_parser("models", help="列出可用模型")
    subparsers.add_parser("tasks", help="列出可用任务")

    args = parser.parse_args()

    if args.command == "test":
        run_test(args.model, args.task, save=not args.no_save)
    elif args.command == "cross":
        run_cross_validation(args.model_a, args.model_b, args.task)
    elif args.command == "models":
        list_models()
    elif args.command == "tasks":
        list_tasks()
    else:
        parser.print_help()
