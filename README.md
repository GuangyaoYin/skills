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
| `nsfc-project-review` | 批量评审国家自然科学基金项目申请书 PDF，生成中文通讯评审意见、评分/资助建议和横向比较。 | [`skill-nsfc-project-review`](https://github.com/GuangyaoYin/skill-nsfc-project-review) | `.` |
| `paper2pdf` | 将学术论文按期刊模板、出版社指南、样例 PDF 或 SciSpace 链接排版为 DOCX/PDF 风格稿。 | [`skill-paper2pdf`](https://github.com/GuangyaoYin/skill-paper2pdf) | `paper2pdf` |
| `review-response-docx` | 根据审稿意见和论文原文逐条撰写 Response to Reviewers，并生成返修分析、回复信、标红修订稿和 clean version。 | [`skill-review-response-docx`](https://github.com/GuangyaoYin/skill-review-response-docx) | `review-response-docx` |
| `skill-endnote-research` | 根据研究想法检索本地 EndNote 文献库，生成文献清单、复制 PDF 并整理综述文件夹。 | [`skill-endnote-research`](https://github.com/GuangyaoYin/skill-endnote-research) | `.` |
| `locflow` | 管理 LOC-FLOW 地震目录处理流程，覆盖 PhaseNet、REAL、VELEST、hypoDD dtct、FDTCC 和 hypoDD dtcc 的审计、质控、制图和报告。 | [`skills`](https://github.com/GuangyaoYin/skills) | `skills/locflow` |
| `earthquake-mc` | 使用归一化累积地震发生曲线估计地震目录完备震级 Mc，并生成候选阈值曲线、分离度表和方法说明。 | [`skills`](https://github.com/GuangyaoYin/skills) | `skills/earthquake-mc` |
| `skillscreator` | 将模糊任务想法、示例材料、工作流或已有仓库转化为可安装、可复用、可上架 GitHub 的 Codex skill。 | [`skill-skillscreator`](https://github.com/GuangyaoYin/skill-skillscreator) | `skillscreator` |

## 安装命令

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

### locflow

```bash
python ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo GuangyaoYin/skills \
  --path skills/locflow
```

### earthquake-mc

```bash
python ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo GuangyaoYin/skills \
  --path skills/earthquake-mc
```

### skillscreator

```bash
python ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo GuangyaoYin/skill-skillscreator \
  --path skillscreator
```

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
    └── locflow/
        └── SKILL.md
```
