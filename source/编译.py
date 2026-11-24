#!/usr/bin/env python3
"""在本目录运行：python 编译.py。需要安装 XeLaTeX、ctex 和 TikZ。"""
from pathlib import Path
import subprocess, shutil
ROOT=Path(__file__).resolve().parent
jobs=[('answers','答案','口算答案.pdf'),('questions','题目','口算题目.pdf'),('answers','速查','口算速查.pdf')]
if not shutil.which('xelatex'):
    raise SystemExit('未找到 xelatex，请安装含 ctex/TikZ 的 TeX Live 或 MiKTeX。')
out=ROOT/'PDF'; out.mkdir(exist_ok=True)
for folder, name, output in jobs:
    for _ in range(2):
        subprocess.run(['xelatex','-interaction=nonstopmode','-halt-on-error',name+'.tex'],cwd=ROOT/folder,check=True)
    shutil.copy2(ROOT/folder/(name+'.pdf'),out/output)
print('完成：',out)
