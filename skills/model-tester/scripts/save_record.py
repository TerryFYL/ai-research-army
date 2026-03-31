#!/usr/bin/env python3
"""
保存测试记录到数据库
"""

import sqlite3
import json
import argparse
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "test_records.db"

def save_test_record(test_type: str, model_a: str, model_b: str,
                     task_name: str, task_prompt: str,
                     result_summary: str, insights: str,
                     model_a_score: int = None, model_b_score: int = None):
    """保存测试记录"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO test_records
    (test_date, test_type, model_a, model_b, task_name, task_prompt,
     result_summary, insights, model_a_score, model_b_score)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        datetime.now().strftime("%Y-%m-%d"),
        test_type,
        model_a,
        model_b,
        task_name,
        task_prompt,
        result_summary,
        insights,
        model_a_score,
        model_b_score
    ))

    conn.commit()
    record_id = cursor.lastrowid
    conn.close()

    print(f"测试记录已保存，ID: {record_id}")
    return record_id

def save_observation(model_name: str, task: str, result: str, insight: str):
    """保存观察记录"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO observations (model_name, observation_date, task, result, insight)
    VALUES (?, ?, ?, ?, ?)
    """, (
        model_name,
        datetime.now().strftime("%Y-%m-%d"),
        task,
        result,
        insight
    ))

    conn.commit()
    conn.close()
    print(f"观察记录已保存: {model_name}")

def update_model_profile(model_name: str, nickname: str = None,
                         strengths: list = None, weaknesses: list = None,
                         best_for: list = None, avoid_for: list = None):
    """更新模型画像"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 检查是否存在
    cursor.execute("SELECT id FROM model_profiles WHERE model_name = ?", (model_name,))
    existing = cursor.fetchone()

    if existing:
        # 更新现有记录
        updates = []
        params = []

        if nickname:
            updates.append("nickname = ?")
            params.append(nickname)
        if strengths:
            updates.append("strengths = ?")
            params.append(json.dumps(strengths, ensure_ascii=False))
        if weaknesses:
            updates.append("weaknesses = ?")
            params.append(json.dumps(weaknesses, ensure_ascii=False))
        if best_for:
            updates.append("best_for = ?")
            params.append(json.dumps(best_for, ensure_ascii=False))
        if avoid_for:
            updates.append("avoid_for = ?")
            params.append(json.dumps(avoid_for, ensure_ascii=False))

        updates.append("last_updated = ?")
        params.append(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        params.append(model_name)

        cursor.execute(f"""
        UPDATE model_profiles SET {', '.join(updates)} WHERE model_name = ?
        """, params)
    else:
        # 插入新记录
        cursor.execute("""
        INSERT INTO model_profiles
        (model_name, nickname, strengths, weaknesses, best_for, avoid_for)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (
            model_name,
            nickname,
            json.dumps(strengths or [], ensure_ascii=False),
            json.dumps(weaknesses or [], ensure_ascii=False),
            json.dumps(best_for or [], ensure_ascii=False),
            json.dumps(avoid_for or [], ensure_ascii=False)
        ))

    conn.commit()
    conn.close()
    print(f"模型画像已更新: {model_name}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="保存测试记录")
    parser.add_argument("--type", choices=["test", "observation", "profile"], required=True)
    parser.add_argument("--model", help="模型名称")
    parser.add_argument("--model-a", help="模型A名称")
    parser.add_argument("--model-b", help="模型B名称")
    parser.add_argument("--task", help="任务名称")
    parser.add_argument("--result", help="结果摘要")
    parser.add_argument("--insight", help="洞察")
    parser.add_argument("--nickname", help="模型昵称")

    args = parser.parse_args()

    if args.type == "observation":
        save_observation(args.model, args.task, args.result, args.insight)
    elif args.type == "profile":
        update_model_profile(args.model, nickname=args.nickname)
