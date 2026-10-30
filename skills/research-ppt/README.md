# research-ppt · 科研汇报 PPT

为日常组会、导师讨论、自己的研究与阶段进展，以及独立的文献汇报模式，制作可编辑 PowerPoint。先询问是否检索文献补充背景，结合证据用 `grill-me` 共同梳理背景与科学问题，确定逐页安排后再制作文件。

## 工作方式

- 开始先询问是否联网补充研究背景。同意后检索可用本地知识库和网络原始文献，围绕本次研究组织背景，找到对应文章及合适原图。
- 将页面论点与原文结论、图号/面板及适用条件绑定。没有原图或证据不足时明确缺口，不以装饰图或未核验引文替代。
- 无论是否联网，均在制作前使用 `grill-me`／`grilling` 逐轮梳理背景逻辑、科学问题、候选解释与证据边界；已认可的安排可以复用。
- 根据怎样更好理解问题、怎样更合逻辑展开论述来组织页面，不固定章节和页数。
- 正文保留必要的方法、数据、关键推理及深入讨论，主动指出证据缺口与替代解释。
- 文献汇报覆盖问题、证明方式、方法、数据、局限、对自身研究的用途和领域价值。
- 使用真实图件与结果说明。可以裁去空白、放大和添加独立可编辑标注；重绘必须有原始数据。
- 默认白底、深色正文、轻页眉，少量蓝/红强调；中文微软雅黑、英文 Times New Roman，数学字体可单独设置。具体用户要求优先。
- 默认交付可编辑 PPTX，内嵌简短逐页备注；页面简引图源，备注保留完整来源。

项目、验收、大会与正式成果汇报应使用相应的报告或模板工作流。本技能重点服务科研理解与讨论。

## 安装

在配置好 Codex skill-installer 的环境中执行：

```bash
python ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py --repo GuangyaoYin/skills --path skills/research-ppt
```

`grilling` 是访谈实现；使用 `$grill-me` 入口时还需其别名。尚未安装二者时执行：

```bash
python ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py --repo mattpocock/skills --path skills/productivity/grilling skills/productivity/grill-me
```

已经安装其中一项时，仅在 `--path` 后列出缺少项；仅安装 `grill-me` 别名不足以执行访谈。依赖位置：[mattpocock/skills](https://github.com/mattpocock/skills/tree/main/skills/productivity)。安装后重启 Codex。

## 使用

```text
用 $research-ppt 根据这些研究笔记、结果图和已有PPT，
先问我是否需要结合本地知识库和联网文献补充背景及论文原图，
再用 $grill-me 与我梳理背景逻辑、科学问题和逐页安排，最后制作组会PPT。
保留必要的方法细节，并展开结果解释与深入讨论。
```

```text
Use $research-ppt to plan and create a paper-reading presentation from this PDF.
Explain the research question, methods, data, evidence, limitations,
relevance to my work, and the value of the questions it resolves or raises.
```

## 依赖与验证边界

宿主环境需要提供可用的演示文稿制作、渲染和编辑工具；技能入口配合环境中的 Presentations 工作流。检查助手使用 Python 标准库，建议 Python 3.10+，已用 Python 3.11.16 测试。

公式要求为 PowerPoint 原生可编辑数学对象。**原生公式生成及 PowerPoint 内实际编辑性尚未端到端实测**，具体制稿前须验证作者路径。导出 PPTX 或检测到数学 XML 均不等于已经通过应用内编辑验证。

包结构检查：

```bash
python skills/research-ppt/scripts/inspect_research_pptx.py /path/to/deck.pptx --require-notes
```

可按实际计划增加 `--expected-slides N` 和 `--expected-equations N`。检查器不会制作 PPT，也不能替代视觉检查、来源核查或公式编辑验证。

可复现的合成包测试：

```bash
python -m unittest discover -s skills/research-ppt/tests -v
```

初版开发通过技能结构验证、7 项检查器测试及 3 个场景的只读行为审查。本次背景与访谈流程另经 2 个场景的只读演练；这些检查不等于用真实科研材料完成了 PPT 制作与应用内编辑验证。

## 文件

- `SKILL.md`：触发边界、共同规划流程和交付要求。
- `agents/openai.yaml`：技能显示信息与调用提示。
- `references/story-and-evidence.md`：研究进展与文献汇报的论证组织。
- `references/background-literature-and-figures.md`：本地与网络文献检索、原图提取及图文证据对应。
- `references/background-grilling.md`：用 grill-me 梳理背景逻辑与科学问题。
- `references/slide-design.md`：页面、字体、图件、来源和备注规范。
- `references/native-equations-and-qa.md`：原生公式要求与验证边界。
- `scripts/inspect_research_pptx.py`：只读 PPTX 包结构检查。
- `tests/test_inspect_research_pptx.py`：合成 OOXML 包测试。

本目录只包含技能规则、代码和合成测试；研究资料由使用者在具体任务中提供，公开示例不包含真实未发表研究或私人材料。
