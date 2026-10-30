# Guangyao Yin's Codex Skills

这里是我维护的 Codex skills 总索引，参考 `lovstudio/skills` 的组织方式整理。每个 skill 通常放在独立 GitHub 仓库中，也可以放在本仓库的 `skills/` 目录下；本仓库提供统一目录、安装命令、适用场景和机器可读清单。

## 快速安装

选择需要的 skill 后，运行对应命令：

```bash
python ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo GuangyaoYin/<repo-name> \
  --path <skill-path>
```

安装后重启 Codex，使新 skill 进入可用列表。

## Skills

| Skill | 用途 | 仓库 | 安装路径 |
| --- | --- | --- | --- |
| `data-locflow` | 通用 LOC-FLOW 地震目录流程、项目配置、输入/目录检查、震级与定位误差及绘图规范；科学后端需另行接入。 | [`skills`](https://github.com/GuangyaoYin/skills/tree/main/skills/data-locflow) | `skills/data-locflow` |
| `research-ppt` | 制作组会、导师讨论与研究进展 PPT；按选择检索本地与网络背景文献和原图，用 grill-me 梳理科学问题，再规划并制作可编辑 PPTX。 | [`skills`](https://github.com/GuangyaoYin/skills/tree/main/skills/research-ppt) | `skills/research-ppt` |
| `nsfc-project-review` | 批量评审国家自然科学基金项目申请书 PDF，生成中文通讯评审意见、评分/资助建议和横向比较。 | [`skill-nsfc-project-review`](https://github.com/GuangyaoYin/skill-nsfc-project-review) | `.` |
| `paper2pdf` | 将学术论文按期刊模板、出版社指南、样例 PDF 或 SciSpace 链接排版为 DOCX/PDF 风格稿。 | [`skill-paper2pdf`](https://github.com/GuangyaoYin/skill-paper2pdf) | `paper2pdf` |
| `review-response-docx` | 根据审稿意见和论文原文逐条撰写 Response to Reviewers，并生成返修分析、回复信、标红修订稿和 clean version。 | [`skill-review-response-docx`](https://github.com/GuangyaoYin/skill-review-response-docx) | `review-response-docx` |
| `skill-endnote-research` | 根据研究想法检索本地 EndNote 文献库，生成文献清单、复制 PDF 并整理综述文件夹。 | [`skill-endnote-research`](https://github.com/GuangyaoYin/skill-endnote-research) | `.` |
| `earthquake-mc` | 使用归一化累积地震发生曲线估计地震目录完备震级 Mc，并生成候选阈值曲线、分离度表和方法说明。 | [`skills`](https://github.com/GuangyaoYin/skills) | `skills/earthquake-mc` |
| `improve-journal-acceptance` | 按编辑视角检查投稿包，优化标题摘要、cover letter、前人工作比较、图件信息、审稿人建议和重投/转投策略。 | [`skills`](https://github.com/GuangyaoYin/skills) | `skills/improve-journal-acceptance` |
| `academic-introduction-polisher` | 润色、翻译和梳理论文 Introduction 的论证结构与英文表达。 | [`skills`](https://github.com/GuangyaoYin/skills/tree/main/skills/academic-introduction-polisher) | `skills/academic-introduction-polisher` |
| `academic-discussion-polisher` | 润色、翻译和梳理论文 Discussion 的证据、机制、替代解释及局限性。 | [`skills`](https://github.com/GuangyaoYin/skills/tree/main/skills/academic-discussion-polisher) | `skills/academic-discussion-polisher` |
| `skillscreator` | 将模糊任务想法、示例材料、工作流或已有仓库转化为可安装、可复用、可上架 GitHub 的 Codex skill。 | [`skill-skillscreator`](https://github.com/GuangyaoYin/skill-skillscreator) | `skillscreator` |

## 安装命令

### data-locflow

```bash
python ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py --repo GuangyaoYin/skills --path skills/data-locflow
```

包含通用流程参考、配置模板和管理检查工具，适用于不同研究区；完整科学后端仍需接入和验证。[下载 ZIP 分发包](dist/data-locflow-skill.zip)。

### nsfc-project-review

```bash
python ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo GuangyaoYin/skill-nsfc-project-review \
  --path .
```

### paper2pdf

```bash
python ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo GuangyaoYin/skill-paper2pdf \
  --path paper2pdf
```

### review-response-docx

```bash
python ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo GuangyaoYin/skill-review-response-docx \
  --path review-response-docx
```

### skill-endnote-research

```bash
python ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo GuangyaoYin/skill-endnote-research \
  --path .
```

### earthquake-mc

```bash
python ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo GuangyaoYin/skills \
  --path skills/earthquake-mc
```

### improve-journal-acceptance

```bash
python ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo GuangyaoYin/skills \
  --path skills/improve-journal-acceptance
```

### skillscreator

```bash
python ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo GuangyaoYin/skill-skillscreator \
  --path skillscreator
```

### academic-introduction-polisher

```bash
python ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo GuangyaoYin/skills \
  --path skills/academic-introduction-polisher
```

### academic-discussion-polisher

```bash
python ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo GuangyaoYin/skills \
  --path skills/academic-discussion-polisher
```

### research-ppt

```bash
python ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py --repo GuangyaoYin/skills --path skills/research-ppt
```

新增背景检索与 `grill-me` 访谈流程；访谈依赖安装及使用方式见 [research-ppt 说明](skills/research-ppt/README.md)。

## 机器可读清单

见 [`skills.yaml`](skills.yaml)。这个文件适合作为后续自动安装、批量更新、生成文档或构建个人 skill marketplace 的入口。

## 维护约定

- 每个 skill 保持独立仓库，方便单独安装、更新和版本管理。
- `SKILL.md` 的 frontmatter 必须包含清晰的 `name` 和 `description`。
- 如果 skill 依赖本地路径、私有数据或特定环境，应在 README 或 `SKILL.md` 中明确写出。
- 示例输出避免包含个人论文题目、真实作者名单、未公开项目或敏感材料。
- 涉及学术写作、评审、引用和投稿格式时，不编造文献、行号、实验结果或期刊要求。

## 仓库结构

```text
skills/
├── README.md
├── README.en.md
├── skills.yaml
└── skills/
    ├── earthquake-mc/
    │   ├── SKILL.md
    │   ├── agents/
    │   │   └── openai.yaml
    │   └── scripts/
    │       └── estimate_mc_normalized.py
    └── improve-journal-acceptance/
        ├── SKILL.md
        └── agents/
            └── openai.yaml
```
