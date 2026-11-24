# 烟台地区小学数学四年级上册口算题卡

**Yantai Grade 4 Math: Mental Arithmetic Cards, Volume 1**

本工程按原书第 1–100 页编排。学生可直接打印题目册；核对单题可用速查册，需要看步骤或不同解法时请用详解册。PDF 的页眉和书签标有原书页码，便于在各册之间查找。

| PDF | 页数 | 用途 |
| --- | ---: | --- |
| [口算题目](release/口算题目.pdf) | 100 | 练习用，留有填答和作图空间 |
| [口算题卡四上答案](release/口算题卡四上答案.pdf) | 403 | 红字答案、计算步骤和多种解法 |
| [口算速查](release/口算速查.pdf) | 100 | 逐页快速核对 |
| [口算合订](release/口算合订.pdf) | 603 | 题目、详解、速查，依次合订 |

## 在哪里编辑

- [LaTeX/TikZ 源码](source/)含原题、详解、速查、重绘题图、公共版式和编译脚本。[源码清单和编译说明](docs/source-inventory.md)注明依赖和历史文件的范围。
- 历史 LaTeX 源码早于最终的 PDF 排版。仅运行 XeLaTeX 不会得到这里的最新版。基线成品保存在 [archive/baseline/](archive/baseline/)。
- 要精确恢复四份定稿，请使用[二进制补丁和说明](patches/README.md)。这是按保留的 PDF 新制作的恢复方式，不是最后几轮排版修改的原脚本。

## 验证与恢复

在仓库根目录运行（校验只需 Python 3；恢复还需可执行的 zstd）：

~~~sh
python3 tools/pdf_revision.py verify
python3 tools/pdf_revision.py restore --out reconstructed
~~~

恢复后会校验每个文件的 SHA-256。此工程的最终版包括原书第 95 页第 4 题的克数订正、后期表格方向与圈框调整、答案与解析位置及空行整理。原书扫描件不在历史源码包内。
