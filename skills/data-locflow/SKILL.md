---
name: data-locflow
description: "为任意研究区建立、迁移或核验 LOC-FLOW 地震目录工作流，涵盖连续波形、PhaseNet拾取、REAL关联、绝对与双差定位、震级、定位误差和可复现图件。用于项目配置、输入/目录验收、后端适配与流程整理；一般地震知识问答或独立背景制图无需启用。"
---

# Data Loc-Flow

帮助用户将自己的连续波形、台站部署与响应、速度模型和项目配置转为可追溯地震目录及结果图。保持研究区无关：地区、日期、仪器、采样率、科学阈值、事件数量和震级经验系数均来自当前项目，不从历史案例或父目录补齐。

## 按任务加载

先读 [能力与实现边界](references/06_implementation_and_acceptance.md)，确定本次是设计、检查、实现适配器、科学运行还是绘图。只继续读取本次所需资料：

| 工作 | 阅读／使用 |
|---|---|
| 初始化、接入新区域、补全配置 | [数据契约](references/02_inputs_and_catalogue_contract.md)、[项目profile](references/07_project_profiles.md)、`assets/config/workflow.example.json` |
| 检测、关联、定位及后端迁移 | [检测与定位](references/01_detection_and_location.md) |
| 测幅、震级、校准、定位误差 | [震级与不确定性](references/03_magnitude_and_uncertainty.md) |
| 文件组织、缓存、恢复与发布 | [复现规范](references/04_folders_and_reproducibility.md) |
| 图件规划或绘制已有结果 | [图件规范](references/05_figure_specification.md)、`assets/config/figure_plan.json` |

`assets/schemas/`的CSV仅演示格式，不是任何实际区域的模型或台站。不要加载全部参考来处理一次窄修改；绘图任务只读取已验收结果，不因此重跑检测或定位。

## 处理项目

1. 明确本次输入、已有结果和要交付的内容。利用用户已提供的数据与配置，先检查可独立推进的部分；缺失信息集中列出，区分能从可靠元数据确定的值与真正需要用户提供的内容。
2. 定位至少需要波形、台站坐标／有效时段、适用速度模型和时间／坐标／深度基准。物理震级另需要逐通道时段的响应、增益、单位及适用的震级方法。只有输入包已可靠包含这些信息时，用户才可能只填写波形和模型路径。
3. 在用户项目的独立run目录创建配置和产物。按需从assets复制模板；不要向安装的skill目录写入项目状态或结果。脚本的相对输入路径基于配置文件目录，输出路径应明确指向项目run。
4. 科学参数无通用默认值时保留未设置，给出元数据推导或小样本试验方案；不要暗中复制采样率、深度范围、概率／CC门槛、Vp/Vs、震级系数或扰动次数。资源批大小与科学筛选阈值分开记录。
5. 运行本次所需的管理检查，保留报告与实际检查范围。科学阶段使用已安装并核验版本的后端；确认接口、模型、走时表、时基和身份映射后，再按任务授权推进。后端未接通时，具体说明缺少哪个接口，继续完成已授权的实现／整理工作，不伪造结果。

## 科学数据约束

- 主链为PhaseNet → REAL → VELEST → ph2dt/hypoDD_dtct → FDTCC → hypoDD_dtcc。可按用户任务替换后端，但需保持标准表、事件UID、绝对到时和各阶段来源；不要把每次重编号的整数ID直接跨阶段或跨月份连接。
- 固定模型、权重、可执行文件和参数版本。验证走时表节点与排列、读表声明和实际查询范围；hypoDD的NLAY、TOP和VEL长度严格一致。更换位置／原时不得改变原始绝对到时。
- 物理测幅支路与归一化拾取支路分开。响应路径存在不等于响应已验证；更换响应、幅值算子、单位、距离定义或标度时重新核验适用性。最终位置变化后核验缓存幅值并重算距离项与震级质量。
- 目录默认使用`magnitude`＋`magnitude_type`；ML、Ms、Mw等分开保留，不自动转换或混合统计。旧列名只能显式映射；缺震级／误差不得补0。
- 区分形式误差、观测扰动、事件对重采样、台站删减、模型敏感性与独立绝对约束。成功运行、残差下降、簇变紧或QC标签不能单独证明高精度。精度视图依据项目预先冻结的标准，误差只用于实际完成该试验的事件。
- 模板匹配是可选分支：新增事件须本地定位、去重并保留实际定位阶段与到时来源；不得继承模板位置或其他来源事件的误差。

## 可直接执行的管理工具

`scripts/locflow.py`仅需要Python 3.11+标准库；可选波形头检查需ObsPy。以下用`SKILL_ROOT`表示**本次实际加载的skill文件夹**，用`RUN`表示用户项目输出目录；不要假设skill安装在某个固定用户名路径。

```bash
# 只生成计划；模板中未配置的输入会原样列出，不启动后端。
python "$SKILL_ROOT/scripts/locflow.py" plan \
  --config "$RUN/config/project.json" --output "$RUN/reports/plan.json"

# -1检查全部匹配文件的头；0不检查头，正数只抽查对应文件数。
python "$SKILL_ROOT/scripts/locflow.py" preflight \
  --config "$RUN/config/project.json" --header-limit -1 \
  --output "$RUN/reports/preflight.json"

python "$SKILL_ROOT/scripts/locflow.py" audit-catalog \
  --catalog "$RUN/products/catalogs/catalog_complete.csv" \
  --output "$RUN/reports/catalogue_acceptance.json"

# 若源表缺类型列，只有用户或可信元数据明确标度后才使用fallback。
python "$SKILL_ROOT/scripts/locflow.py" audit-catalog \
  --catalog "$RUN/input/legacy_catalog.csv" \
  --magnitude-column local_ml --default-magnitude-type ML \
  --output "$RUN/reports/legacy_acceptance.json"

python "$SKILL_ROOT/scripts/locflow.py" check-hypodd-model \
  --input "$RUN/config/hypoDD.inp" --output "$RUN/reports/layers.json"
```

`check-travel-table`还需显式提供`--table`、`--distance-max-deg`、`--distance-step-deg`、`--depth-max-km`和`--depth-step-km`；数值应来自同一张表的生成记录。它仅支持参考文档中的REAL/FDTCC十列约定，其他格式需适配。

检查命令退出0表示本项通过、2表示失败。`plan`的WRITTEN只表示计划写出；空模板预检FAIL正常。`audit-catalog`只验收非空、震级与类型齐全的complete视图，不验收允许缺测的all视图，也不证明科学精度。

## 结果与交付

维护一个主目录，并按需要派生all、complete和high_precision视图。保留输入哈希、配置／模型／后端版本、lineage、接受与拒绝原因、误差方法和来源。缓存恢复必须核对依赖签名，不以旧`.done`或文件存在当作成功。

绘图消费冻结结果；根据输入生成适用图，不用旧图或占位数据补齐。默认不放图名、备注或样本数提示，保留轴名、单位、色标、图例与必要标识；静态输出PNG＋TXT／JSON／TSV。范围、分期、投影和深度色标由项目决定，色标上限不能过滤科学目录；地质、断层及外部目录为可选背景。

交付时说明本次生成／修改了什么、实际执行哪些检查／后端、结果位置及仍未验证的部分。当前skill包含流程知识、模板与五项管理命令，**不自带完整科学计算后端或自动绘图实现**；创建或调用skill不表示已完成原始波形到高精度目录的端到端验证。
