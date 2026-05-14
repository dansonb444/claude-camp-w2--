#!/usr/bin/env python3
"""待办清单：添加、完成、查看；持久化到 todos.json；重启后自动加载。"""
import json
import sys
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parent / "todos.json"

# 终端图标：未完成 / 已完成（绿色对勾）
ICON_PENDING = "\033[33m○\033[0m"  # 黄色空心圆
ICON_DONE = "\033[92m✓\033[0m"  # 绿色对勾


def load_todos() -> list[dict]:
    if not DATA_FILE.is_file():
        print(f"【错误】未找到数据文件：{DATA_FILE}", file=sys.stderr)
        print("请在该路径创建 todos.json（例如内容写 [] 表示空清单），或先添加一条待办以自动创建。", file=sys.stderr)
        sys.exit(1)
    try:
        raw = DATA_FILE.read_text(encoding="utf-8")
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"【错误】todos.json 不是合法 JSON：{e}", file=sys.stderr)
        sys.exit(1)
    except OSError as e:
        print(f"【错误】无法读取文件：{e}", file=sys.stderr)
        sys.exit(1)
    if not isinstance(data, list):
        print("【错误】todos.json 根节点必须是数组 []。", file=sys.stderr)
        sys.exit(1)
    out: list[dict] = []
    for i, item in enumerate(data):
        if not isinstance(item, dict):
            print(f"【错误】第 {i + 1} 条记录不是对象，已中止加载。", file=sys.stderr)
            sys.exit(1)
        title = item.get("title", "")
        done = bool(item.get("done", False))
        if not isinstance(title, str):
            title = str(title)
        out.append({"title": title.strip(), "done": done})
    return out


def save_todos(todos: list[dict]) -> None:
    try:
        DATA_FILE.write_text(
            json.dumps(todos, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
    except OSError as e:
        print(f"【错误】无法写入 {DATA_FILE}：{e}", file=sys.stderr)


def show_list(todos: list[dict]) -> None:
    if not todos:
        print("（暂无待办）")
        return
    print("当前清单：")
    for idx, t in enumerate(todos, start=1):
        icon = ICON_DONE if t["done"] else ICON_PENDING
        status = "已完成" if t["done"] else "未完成"
        print(f"  {icon}  [{idx}] {t['title']}  — {status}")


def add_todo(todos: list[dict]) -> None:
    title = input("请输入待办内容：").strip()
    if not title:
        print("提示：内容不能为空。")
        return
    todos.append({"title": title, "done": False})
    save_todos(todos)
    print("已添加并保存。")


def complete_todo(todos: list[dict]) -> None:
    if not todos:
        print("提示：清单为空，无需完成。")
        return
    show_list(todos)
    s = input("请输入要完成的项目编号：").strip()
    try:
        n = int(s)
    except ValueError:
        print("提示：请输入有效整数编号。")
        return
    if n < 1 or n > len(todos):
        print("提示：编号超出范围。")
        return
    if todos[n - 1]["done"]:
        print("提示：该项已经是已完成状态。")
        return
    todos[n - 1]["done"] = True
    save_todos(todos)
    print("已标记为完成并保存。")


def main() -> None:
    print("待办事项清单（数据文件 todos.json）")
    todos = load_todos()
    while True:
        print()
        print("请选择：")
        print("  1 — 添加待办")
        print("  2 — 完成待办（按编号）")
        print("  3 — 查看清单")
        print("  0 — 退出")
        choice = input("请输入选项：").strip()
        try:
            if choice == "0":
                print("再见。")
                return
            if choice == "1":
                add_todo(todos)
            elif choice == "2":
                complete_todo(todos)
            elif choice == "3":
                show_list(todos)
            else:
                print("提示：请输入 0～3。")
        except (EOFError, KeyboardInterrupt):
            print("\n已中断，退出。")
            return
        except Exception as e:
            print(f"发生意外错误：{e}，请重试。")


if __name__ == "__main__":
    main()
