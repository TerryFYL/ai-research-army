#!/usr/bin/env python3
"""
初始化 model-tester 数据库
"""

import sqlite3
import os
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "test_records.db"

def init_database():
    """创建数据库表结构"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 测试记录表
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS test_records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        test_date TEXT NOT NULL,
        test_type TEXT NOT NULL,  -- cross_validation / comprehensive_task / observation
        model_a TEXT,
        model_b TEXT,
        task_name TEXT,
        task_prompt TEXT,
        result_summary TEXT,
        insights TEXT,
        model_a_score INTEGER,
        model_b_score INTEGER,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # 模型画像表
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS model_profiles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        model_name TEXT UNIQUE NOT NULL,
        nickname TEXT,
        strengths TEXT,  -- JSON array
        weaknesses TEXT,  -- JSON array
        best_for TEXT,  -- JSON array
        avoid_for TEXT,  -- JSON array
        last_updated TEXT DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # 观察记录表
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS observations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        model_name TEXT NOT NULL,
        observation_date TEXT NOT NULL,
        task TEXT,
        result TEXT,
        insight TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()
    print(f"数据库初始化完成: {DB_PATH}")

if __name__ == "__main__":
    init_database()
