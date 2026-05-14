#!/usr/bin/env python3
"""安全计算器：+-×÷；除零与非数字不崩溃；输入 quit 退出。"""
import re

# 匹配：可选空白 + 左操作数 + 运算符 + 右操作数 + 可选空白
EXPR = re.compile(
    r"^\s*"
    r"(-?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?)"
    r"\s*"
    r"([+\-*/×÷xX])"
    r"\s*"
    r"(-?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?)"
    r"\s*$"
)

OP_MAP = {"+": "+", "-": "-", "*": "*", "x": "*", "X": "*", "×": "*", "/": "/", "÷": "/"}


def calc(left: float, op: str, right: float):
    sym = OP_MAP[op]
    if sym == "/" and right == 0:
        return None
    if sym == "+":
        return left + right
    if sym == "-":
        return left - right
    if sym == "*":
        return left * right
    return left / right


def main() -> None:
    print("安全计算器：支持 + - × ÷（也可用 * / x X）")
    print("格式示例：3 + 4  或  10 ÷ 2 ；输入 quit 退出。")
    while True:
        try:
            line = input("\n> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n再见。")
            return
        if not line:
            continue
        if line.lower() == "quit":
            print("再见。")
            return
        m = EXPR.match(line)
        if not m:
            print("提示：请输入「数字 运算符 数字」，运算符两侧建议加空格；例如 1.5 * 2")
            continue
        a_s, op, b_s = m.group(1), m.group(2), m.group(3)
        try:
            a = float(a_s)
            b = float(b_s)
        except ValueError:
            print("提示：左右两侧需要为合法数字。")
            continue
        try:
            result = calc(a, op, b)
        except Exception as e:
            print(f"提示：运算出错（{e}），请换一道题。")
            continue
        if result is None:
            print("提示：除数不能为 0，请更换除数。")
            continue
        print(f"= {result}")


if __name__ == "__main__":
    main()
