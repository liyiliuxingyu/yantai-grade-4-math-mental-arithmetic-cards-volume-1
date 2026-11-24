# 恢复最终版 PDF

这里的补丁是将历史 PDF 和最终成品按字节比较后**重新生成**的二进制差分。它们用来恢复和检验成品，不是原先调整分栏、表格、留白或圈框的排版脚本。LaTeX/TikZ 的历史源码仍然在 `source/`，对应的原始成品保存在 `archive/baseline/`。仅重编历史源码不能保证生成含后续排版修订的最终版。

直接阅读可打开 `release/`。要验证或从旧版恢复，在仓库根目录运行：

```sh
# 不用安装 LaTeX，也不联网。校验只需 Python 3.8 或以上。
python3 tools/pdf_revision.py verify

# 恢复另需安装 zstd 命令行程序，并加入 PATH。已验证版本：1.5.7。
python3 tools/pdf_revision.py restore --out reconstructed
python3 tools/pdf_revision.py verify --dir reconstructed
```

Windows 可以用 `py -3` 替代 `python3`。恢复时不读取 `release/`；输入为 `archive/baseline/` 中的四份原始 PDF 和本目录的补丁。工具将四份最终 PDF 写到指定目录，并校验文件长度与 SHA-256。已经存在且哈希不符的文件不会被覆盖。请选择有约 200 MB 可用空间的输出目录。

| 补丁 | 恢复结果 |
| --- | --- |
| `questions.zst` | 口算题目.pdf |
| `quick-key.zst` | 口算速查.pdf |
| `worked-answers.zst` | 口算题卡四上答案.pdf |
| `combined.zst` | 口算合订.pdf |

`manifest.json` 记录原版、最终版和补丁的字节数、SHA-256 以及每一步参考文件的顺序；`b` 是归档原版，`f` 是前面步骤已恢复的最终版。补丁保留内嵌字体、书签以及全部 PDF 矢量对象：最终产物须与所记录的文件逐字节相同。差分仅适用于清单所列的原始字节，不能直接套用在修改过或重新编译出来的 PDF 上。

今后手工改过 `release/` 中的 PDF 并确认无误后，可运行 `python3 tools/pdf_revision.py make-patches`。该命令会逐册做恢复测试，然后才更新补丁及哈希清单。它不会自行把新题改排到其他分册或更新合订版；如改动正文，请先生成并检查对应的新版分册和合订版。
