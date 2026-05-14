#!/usr/bin/env python3
"""文本词频统计：字典存储、按次数降序、忽略大小写、单词查询。"""
import os

# macOS 自带 Tcl/Tk 弃用提示；须在 import tkinter 之前设置
os.environ.setdefault("TK_SILENCE_DEPRECATION", "1")

import re
import tkinter as tk
from collections import Counter
from tkinter import messagebox, scrolledtext

# 连续字母数字与撇号视为同一单词（已 lower，大小写不区分）
WORD_RE = re.compile(r"[a-z0-9']+")

# 调试用彩色外框：绿=正文输入，橙=单词查询，蓝=词频结果
_BORDER_PAD = 3
_BORDER_MAIN = "#2ecc71"
_BORDER_QUERY = "#e67e22"
_BORDER_OUT = "#3498db"


def word_freq_dict(text: str) -> dict[str, int]:
    words = WORD_RE.findall(text.lower())
    return dict(Counter(words))


def sort_by_count(d: dict[str, int]) -> list[tuple[str, int]]:
    return sorted(d.items(), key=lambda x: (-x[1], x[0]))


class App(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("词频统计器")
        self.minsize(560, 480)
        self.geometry("720x620")
        self._freq: dict[str, int] = {}
        self._build()

    def _build(self) -> None:
        # macOS 系统 Tk：LabelFrame + grid + Text(width=…) 易出现输入区被挤到右侧一条线。
        # 用单层垂直 pack，Text 不设 width，由窗口横向拉伸分配宽度。
        main = tk.Frame(self)
        main.pack(fill=tk.BOTH, expand=True)

        tk.Label(main, text="在此输入或粘贴文字：").pack(anchor=tk.W, padx=10, pady=(10, 2))
        tk.Label(
            main,
            text="调试边框：绿色=正文 ｜ 橙色=查询 ｜ 蓝色=结果",
            fg="#555555",
            font=("TkDefaultFont", 10),
        ).pack(anchor=tk.W, padx=10, pady=(0, 2))

        box_txt = tk.Frame(main, bg=_BORDER_MAIN, padx=_BORDER_PAD, pady=_BORDER_PAD)
        box_txt.pack(fill=tk.BOTH, expand=True, padx=10, pady=2)
        self.txt = scrolledtext.ScrolledText(box_txt, height=10, wrap=tk.WORD, highlightthickness=0)
        self.txt.pack(fill=tk.BOTH, expand=True)

        qrow = tk.Frame(main)
        qrow.pack(fill=tk.X, padx=10, pady=8)
        tk.Label(qrow, text="要查的单词：").pack(side=tk.LEFT)
        box_ent = tk.Frame(qrow, bg=_BORDER_QUERY, padx=_BORDER_PAD, pady=_BORDER_PAD)
        box_ent.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(4, 8))
        self.query_ent = tk.Entry(box_ent, highlightthickness=0)
        self.query_ent.pack(fill=tk.BOTH, expand=True)
        tk.Button(qrow, text="查询", command=self._on_query).pack(side=tk.LEFT)

        brow = tk.Frame(main)
        brow.pack(fill=tk.X, padx=10, pady=(0, 6))
        tk.Button(brow, text="统计词频", command=self._on_stat).pack(side=tk.LEFT)
        tk.Button(brow, text="清空", command=self._clear).pack(side=tk.LEFT, padx=(8, 0))

        tk.Label(main, text="词频结果（次数从高到低）：").pack(anchor=tk.W, padx=10, pady=(4, 2))
        box_out = tk.Frame(main, bg=_BORDER_OUT, padx=_BORDER_PAD, pady=_BORDER_PAD)
        box_out.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        self.out = scrolledtext.ScrolledText(box_out, height=12, wrap=tk.NONE, state=tk.DISABLED, highlightthickness=0)
        self.out.pack(fill=tk.BOTH, expand=True)

        self.txt.focus_set()

    def _set_out(self, s: str) -> None:
        self.out.configure(state="normal")
        self.out.delete("1.0", "end")
        self.out.insert("end", s)
        self.out.configure(state="disabled")

    def _on_stat(self) -> None:
        try:
            raw = self.txt.get("1.0", "end")
            self._freq = word_freq_dict(raw)
            lines = [f"{w}\t{c}" for w, c in sort_by_count(self._freq)]
            self._set_out("\n".join(lines) if lines else "（无单词可统计）")
        except Exception as e:
            messagebox.showerror("统计异常", f"请检查输入或稍后重试。\n详情：{e}")

    def _on_query(self) -> None:
        try:
            if not self._freq:
                self._freq = word_freq_dict(self.txt.get("1.0", "end"))
            q = self.query_ent.get().strip().lower()
            if not q:
                messagebox.showwarning("提示", "请在输入框中填写要查询的单词。")
                return
            key = WORD_RE.findall(q)
            key = key[0] if key else q
            n = self._freq.get(key, 0)
            if n:
                messagebox.showinfo("查询结果", f"包含单词 “{key}”，出现 {n} 次。")
            else:
                messagebox.showinfo("查询结果", f"未找到单词 “{key}”（按词匹配，忽略大小写）。")
        except Exception as e:
            messagebox.showerror("查询异常", f"查询失败。\n详情：{e}")

    def _clear(self) -> None:
        self.txt.delete("1.0", "end")
        self._freq = {}
        self._set_out("")


if __name__ == "__main__":
    App().mainloop()
