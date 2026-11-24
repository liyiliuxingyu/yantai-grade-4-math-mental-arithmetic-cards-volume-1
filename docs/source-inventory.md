# 工程源文件与版本对照

本仓库同时保留可编辑的历史 LaTeX/TikZ 源码和较晚定稿的 PDF。阅读、打印请使用 `release/`；从原题和解法继续编辑，请先看 `source/`。原归档内部的“最终”均指该归档形成时的版本。

| 目录或文件 | 内容 |
| --- | --- |
| `source/questions/题目.tex` | 题目册主文档，引用 `questions/p001.tex` 至 `p100.tex`，以及本册图形 |
| `source/answers/答案.tex` | 详解册主文档，按原书页码引用 `integrated/p001.tex` 至 `p100.tex` |
| `source/answers/速查.tex` | 速查册主文档，含逐页答案及必要图形 |
| `source/common_book.tex`、`source/p77_tikz.tex` | 公共版式、宏和原书第 77 页的图形 |
| `source/核对记录/` | 8 份历史记录，包括覆盖情况、整合校对和第 68、77 页核对结果；不是对后来 PDF 的逐题证明 |
| `source/页码对照.csv` | 100 个原书页码与分册、合订本页码的对照 |
| `archive/baseline/` | 原全套包中的四份历史 PDF、使用说明及页码对照，供历史版本对照 |
| `release/` | 后续定稿的题目册、答案详解、速查、合订成品 |

## 构建归档版本

安装 Python 3，以及含 XeLaTeX、ctex、PGF/TikZ、Fandol 字体和其余排版宏包的完整 TeX Live 或 MiKTeX。附加宏包列表以 `source/common_book.tex` 为准。仓库未内置字体和 TeX 工具链。在仓库根目录执行：

```bash
python3 source/编译.py
```

此脚本给三个 `ctexbook` 入口各运行两次 XeLaTeX，将分册放到 `source/PDF/`。它不会生成合订本，也不会把历史分册覆盖到 `release/`。若在 Windows 环境使用 Python 启动器，可用 `py -3 source/编译.py`。

## 归档对照和验证边界

- `口算源码.zip` 共含 650 个文件：639 个 TeX 文件、7 个 JSON、2 个 TXT、1 个 Python 脚本、1 个 CSV。`口算全套.zip` 内嵌的源码压缩包与独立源码压缩包逐字节相同，故这里将它展开一次。两份 CSV 在对应原目录中保留。
- 两个压缩包均通过 ZIP 成员 CRC 检查。已将展开后的 650 个源码文件和 6 个全套附件逐件与原包比对。唯一面向公开仓库的处理，是将 `cleanup_manifest.txt` 中的 62 个私人文件存储标识删除；历史文件名均保留。其余文件原样保留。
- 检查了 523 处显式 TeX 文件/图形引用，在各入口或源码目录下均找到了相应文件。原编译脚本和依赖记录一并保留。本次发布环境未安装完整的 ctexbook 和 XeLaTeX 格式文件，未在此环境重新排版编译。
- 全套历史 PDF 与单独恢复的现行 PDF 为不同版本。历史 TeX 包不含后来的表格行列调整、原书第 95 页的克数订正、答案后紧接解析、填空圈框及留白修订。现行 PDF 保存了这些后续排版结果；历史归档没有包含对应的后处理脚本，因此直接重新编译这些 TeX 不能逐字节重现 `release/`。
- 原始扫描图片、字体文件及 Lean 源码不在上述归档中。题图以 TeX/TikZ 源码归档。

原始归档 SHA-256（用于与持有的原包核对）：

```text
f4073bb7e84e60fbd3f4260058549121d1dbf6d48cad9a35a9a9dbb42454353f  口算源码.zip
6b2cb951a08addd22356b91b26a1f949d1fa8f0016319f12eef9273e4f148258  口算全套.zip
```
