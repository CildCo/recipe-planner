import argparse
import os
import sys
import webbrowser
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR / "backend"))


def main() -> None:
    parser = argparse.ArgumentParser(description="启动饭桌后端")
    parser.add_argument("--host", default=os.getenv("HOST", "127.0.0.1"))
    parser.add_argument("--port", type=int, default=int(os.getenv("PORT", "8020")))
    parser.add_argument("--open", action="store_true", help="启动后打开管理后台")
    args = parser.parse_args()

    import uvicorn

    if args.open:
        webbrowser.open(f"http://{args.host}:{args.port}/admin")

    print(f"管理后台：http://{args.host}:{args.port}/admin")
    print(f"小程序接口：http://{args.host}:{args.port}/api")
    password_file = BASE_DIR / "backend" / "runtime" / "admin-password.txt"
    if password_file.exists() and not os.getenv("ADMIN_PASSWORD"):
        print(f"首次登录密码：{password_file}")
    else:
        print("管理员密码：读取环境变量 ADMIN_PASSWORD")
    uvicorn.run("app.main:app", host=args.host, port=args.port, app_dir=str(BASE_DIR / "backend"))


if __name__ == "__main__":
    main()
