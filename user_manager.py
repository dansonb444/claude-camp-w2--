#!/usr/bin/env python3
"""命令行用户管理器：字典存储姓名、邮箱、加入日期；支持添加、查询、删除。"""
import re
import sys
from datetime import date

# 邮箱作为唯一键；值为 {姓名, 邮箱, 加入日期}
EMAIL_RE = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")


def _initial_users() -> dict[str, dict[str, str]]:
    rows = [
        ("陈思远", "chen.siyuan@example.com", "2024-03-12"),
        ("李雨桐", "li.yutong@example.com", "2024-05-01"),
        ("王浩然", "wang.haoran@example.com", "2024-06-18"),
        ("张梓萱", "zhang.zixuan@example.com", "2024-07-22"),
        ("刘子墨", "liu.zimo@example.com", "2024-08-30"),
        ("赵欣怡", "zhao.xinyi@example.com", "2024-09-05"),
        ("周宇航", "zhou.yuhang@example.com", "2024-10-11"),
        ("吴若曦", "wu.ruoxi@example.com", "2024-11-03"),
        ("孙嘉树", "sun.jiashu@example.com", "2025-01-09"),
        ("郑清妍", "zheng.qingyan@example.com", "2025-02-14"),
    ]
    out: dict[str, dict[str, str]] = {}
    for name, email, join_date in rows:
        out[email] = {"姓名": name, "邮箱": email, "加入日期": join_date}
    return out


def _prompt_nonempty(label: str) -> str:
    s = input(label).strip()
    return s


def _parse_date(s: str) -> str:
    s = s.strip()
    if not s:
        return date.today().isoformat()
    try:
        y, m, d = (int(x) for x in s.split("-", 2))
        return date(y, m, d).isoformat()
    except (ValueError, TypeError):
        raise ValueError("加入日期格式应为 YYYY-MM-DD，例如 2024-06-01；留空则使用今天。")


def _print_user(u: dict[str, str]) -> None:
    print(f"  姓名：{u['姓名']}")
    print(f"  邮箱：{u['邮箱']}")
    print(f"  加入日期：{u['加入日期']}")


def add_user(users: dict[str, dict[str, str]]) -> None:
    name = _prompt_nonempty("请输入姓名：")
    if not name:
        print("提示：姓名不能为空。")
        return
    email = _prompt_nonempty("请输入邮箱：").lower()
    if not EMAIL_RE.match(email):
        print("提示：邮箱格式不正确，需包含 @ 与域名，例如 user@example.com。")
        return
    if email in users:
        print("提示：该邮箱已存在，请使用其他邮箱或先删除再添加。")
        return
    raw_date = input("请输入加入日期（YYYY-MM-DD，直接回车为今天）：")
    try:
        join_date = _parse_date(raw_date)
    except ValueError as e:
        print(f"提示：{e}")
        return
    users[email] = {"姓名": name, "邮箱": email, "加入日期": join_date}
    print(f"已添加用户：{name}（{email}）")


def query_user(users: dict[str, dict[str, str]]) -> None:
    if not users:
        print("当前没有任何用户记录。")
        return
    hint = input("请输入要查询的邮箱（输入 all 列出全部）：").strip()
    if not hint:
        print("提示：请输入邮箱，或输入 all 查看全部。")
        return
    if hint.lower() == "all":
        list_all(users)
        return
    email = hint.lower()
    u = users.get(email)
    if not u:
        print("未找到该邮箱对应的用户。")
        return
    print("查询结果：")
    _print_user(u)


def delete_user(users: dict[str, dict[str, str]]) -> None:
    email = _prompt_nonempty("请输入要删除的用户邮箱：").lower()
    if not email:
        print("提示：邮箱不能为空。")
        return
    if email not in users:
        print("未找到该邮箱，无法删除。")
        return
    name = users[email]["姓名"]
    confirm = _prompt_nonempty(f"确认删除「{name}」({email})？输入 yes 确认，其它取消：")
    if confirm.lower() != "yes":
        print("已取消删除。")
        return
    del users[email]
    print("已删除该用户。")


def list_all(users: dict[str, dict[str, str]]) -> None:
    if not users:
        print("当前没有任何用户记录。")
        return
    print(f"共 {len(users)} 条记录：")
    for i, u in enumerate(users.values(), 1):
        print(f"--- [{i}] ---")
        _print_user(u)


def main() -> None:
    users = _initial_users()
    print("用户管理器（预置 10 条示例数据）")
    while True:
        print()
        print("请选择操作：")
        print("  1 — 添加用户")
        print("  2 — 查询用户（按邮箱；输入 all 可列出全部）")
        print("  3 — 删除用户（按邮箱）")
        print("  0 — 退出")
        choice = input("请输入选项编号：").strip()
        try:
            if choice == "0":
                print("再见。")
                sys.exit(0)
            if choice == "1":
                add_user(users)
            elif choice == "2":
                query_user(users)
            elif choice == "3":
                delete_user(users)
            else:
                print("提示：请输入 0～3 之间的数字。")
        except (EOFError, KeyboardInterrupt):
            print("\n已中断，退出程序。")
            sys.exit(0)
        except Exception as e:
            print(f"发生意外错误：{e}")
            print("请重试或更换输入；程序将继续运行。")


if __name__ == "__main__":
    main()
