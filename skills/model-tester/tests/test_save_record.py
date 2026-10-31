"""save_record.py CLI 回归测试。

契约：--type test/observation/profile 三种记录类型都必须真正写入
test_records.db / observations 表，并打印确认信息。
--type test 曾被静默忽略（退出码 0、无输出、不落库），导致测试记录丢失。
"""

import shutil
import sqlite3
import subprocess
import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent.parent / "scripts"


def _prepare(tmp_path):
    # 复制脚本到临时目录运行，使 test_records.db 落在 tmp_path 而非仓库内
    dst = tmp_path / "scripts"
    dst.mkdir(exist_ok=True)
    for name in ("init_db.py", "save_record.py"):
        shutil.copy(SCRIPTS / name, dst / name)
    return dst


def _run_cli(tmp_path, *argv):
    dst = _prepare(tmp_path)
    return subprocess.run(
        [sys.executable, str(dst / "save_record.py"), *argv],
        capture_output=True,
        text=True,
        encoding="utf-8",
    )


def _init_db(tmp_path):
    dst = _prepare(tmp_path)
    subprocess.run(
        [sys.executable, str(dst / "init_db.py")],
        check=True, capture_output=True, text=True, encoding="utf-8",
    )


def test_type_test_persists_record(tmp_path):
    _init_db(tmp_path)
    proc = _run_cli(
        tmp_path,
        "--type", "test",
        "--model-a", "model-x",
        "--model-b", "model-y",
        "--task", "统计任务",
        "--prompt", "分析这份数据",
        "--result", "A 更稳",
        "--insight", "B 在边界条件下幻觉",
        "--score-a", "5",
        "--score-b", "3",
    )

    assert proc.returncode == 0, proc.stderr
    assert "测试记录已保存" in proc.stdout, f"无确认输出: stdout={proc.stdout!r}"

    conn = sqlite3.connect(tmp_path / "test_records.db")
    rows = conn.execute(
        "SELECT test_type, model_a, model_b, task_name, task_prompt,"
        " result_summary, insights, model_a_score, model_b_score"
        " FROM test_records"
    ).fetchall()
    conn.close()

    assert rows == [(
        "comprehensive_task", "model-x", "model-y", "统计任务", "分析这份数据",
        "A 更稳", "B 在边界条件下幻觉", 5, 3,
    )]


def test_type_observation_still_persists(tmp_path):
    _init_db(tmp_path)
    proc = _run_cli(
        tmp_path,
        "--type", "observation",
        "--model", "m1",
        "--task", "t1",
        "--result", "r1",
        "--insight", "i1",
    )

    assert proc.returncode == 0, proc.stderr
    assert "观察记录已保存" in proc.stdout

    conn = sqlite3.connect(tmp_path / "test_records.db")
    rows = conn.execute(
        "SELECT model_name, task, result, insight FROM observations"
    ).fetchall()
    conn.close()
    assert rows == [("m1", "t1", "r1", "i1")]
