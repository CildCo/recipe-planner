"""跑通饭桌的全部检查。

用法：
    python run_all.py

会依次：
1. 生成封面和 tabBar 图标（缺失时）
2. 导出小程序本地数据
3. 检查菜谱、封面、小程序页面、JS 语法
4. 跑后端测试
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PYTHON = sys.executable

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")


def run(name: str, args: list[str], cwd: Path = ROOT) -> None:
    print(f"\n>>> {name}")
    result = subprocess.run(args, cwd=str(cwd))
    if result.returncode != 0:
        print(f"失败：{name}")
        sys.exit(result.returncode)


def main() -> None:
    if not (ROOT / "backend" / "app" / "static" / "covers" / "tomato-egg.jpg").exists():
        run("生成封面", [PYTHON, "tools/make-assets.py"])
    run("导出小程序数据", [PYTHON, "tools/export-mini-data.py"])
    run("内容检查", [PYTHON, "tools/check-content.py"])
    run("后端测试", [PYTHON, "-m", "pytest", "tests", "-q"], ROOT / "backend")
    print("\n全部通过。启动：python start.py")


if __name__ == "__main__":
    main()
