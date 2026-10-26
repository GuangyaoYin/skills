# 输入与目录的数据契约

## 必需输入

| 输入 | 最少信息 | 预检／失败处理 |
|---|---|---|
| 连续波形 | 文件位置、网络／台站／位置码／通道、起止时刻、采样率、原始单位 | 逐段核查头段；不能从文件名假定 100 Hz 或午夜起始 |
| 台站部署 | 经纬度、台站高程、起止有效期、坐标基准 | 更换位置拆时段；无坐标不能定位 |
| 响应与增益 | 每通道、每时段的响应／灵敏度、输入输出单位、增益状态 | 缺失时可以定位，不能填造 ML；需输出缺测原因 |
| 初始速度模型 | 深度、Vp、Vs、单位、基准、分层或梯度语义 | 同源生成 TauP、VELEST、hypoDD 输入，保留转换差异 |
| 时间／研究范围 | UTC 转换规则、分析时段、研究范围、搜索缓冲区 | 目录范围、关联搜索范围、制图范围分别配置 |
| 软件与权重 | 每个可执行文件／代码版本、PhaseNet 权重 | 记录路径及 SHA256；PATH 中同名程序不能被当作同一版本 |

输入清单以文件／连续段为粒度。波形只读引用，不复制 TB 级数据到运行目录；科学发布前按项目策略完成内容校验。部署记录、响应和模型应完整内容哈希。若快速盘点暂用路径／大小／mtime，要在清单注明尚未完成内容哈希，不能宣称输入字节已冻结。

`start_time_utc`、`end_time_utc` 采用 ISO 8601，显式 `Z` 或偏移；规范输出统一 UTC。原始时区不明必须阻断时间相关处理，不能凭外部参考目录、文件名或系统时区推断。未声明时区的外部目录只可在单独参考模块按其源时钟展示，不混入本地主目录。

台站与波形跨日按真实 UTC 连续时间处理；日文件是存储方式，不是新的时间零点。采样点时刻＝本连续段起始时刻＋点号／实际采样率，再加已记录的裁剪偏移。重采样要记录抗混叠方法、原采样率与目标采样率。

源台站CSV的最小字段见`assets/schemas/`模板；若没有`station_epoch_uid`，适配器应按网络／台站和有效时段生成稳定时段ID，并将映射写入规范化部署表。所有阶段伴表使用该ID，不凭台站名推断部署或仪器。高程统一以m存储，写入要求km的旧程序时显式转换。

## 模型与走时表

通用模型 `velocity_layers.csv` 至少有 `top_depth_km,vp_km_s,vs_km_s`。该接口是分层模型，不能把带重复深度间断面的 `.nd` 文件简单去重后当作等价模型。转换器必须在规范记录中说明：层速度还是节点梯度、海平面还是地表深度、S 速度是否独立、是否用固定 Vp/Vs、台站高程如何参与走时。

每张走时表配套 JSON：模型 SHA、生成程序 SHA、深度／距离节点及单位、节点顺序、P/S 分支选择、台站高程处理、生成日期。读表端使用同一个 JSON 生成控制参数。禁止生成器一套最大深度、REAL 一套范围、FDTCC 再一套范围；禁止靠文件名断定表已更新。

现有本地格式从第一个正距离步长开始，深度优先、距离次之。检查程序验证每个节点及顺序，不只比较总行数。合法但不同的格式需要明确适配器，不能强行套入这项检查。不同软件对深度、球面／平面和高程的处理不同，格式一致也不等于射线路径模型完全一致，必须留转换与敏感性报告。

## 阶段表与主键

| 表 | 主键与核心字段 | 不能丢失的信息 |
|---|---|---|
| `waveform_index.csv` | waveform_uid、路径、NSLC、起止时刻、采样率 | 单位、响应时段、缺测、削波、时钟状态、原文件 SHA |
| `picks.csv` | pick_uid、waveform_uid、station_epoch_uid、P/S、到时、概率 | 原样点号、窗口偏移、权重版本、拒绝原因 |
| `events_real.csv` | event_uid、初始时空位置 | 关联参数、关联震相数量、待质控状态 |
| `event_picks.csv` | event_uid＋pick_uid | 是否采用、到时残差、事件—震相关系 |
| `events_absolute/dtct/dtcc.csv` | event_uid、各阶段时空位置 | 各阶段模型与参数哈希、失败原因、有效台站、残差 |
| `pair_qc.csv` | event_uid_1＋event_uid_2＋台站＋震相 | 原目录差分时、CC 差分时、CC 系数、时差符号、频带、窗口、采用原因 |
| `station_magnitudes.csv` | event_uid＋station_epoch_uid＋测幅方法 | E/N 原幅值及单位、响应、增益、测幅窗、SNR、最终震源距、系数版本、站 ML |
| `location_uncertainty.csv` | event_uid＋方法＋试验版本 | 成功／总次数、分位数、散布、模型敏感性、绝对约束状态 |
| `event_lineage.csv` | event_uid＋阶段 | 旧软件局部整数 ID、父／模板事件、来源、去重组、各阶段选择理由 |

事件 UID 从首次接受事件起保持稳定；每月重新编号的整数 ID 只能作软件内部键。必须维护 `run_id/source_partition/local_event_id ↔ event_uid` 映射，不能仅用 `event_id=10` 跨月合并。事件对规范化排序时若交换事件顺序，差分时的符号必须同步转换并有单元测试。

## 发布目录字段

`catalog_all.csv` 包含可信的全部本地解，允许震级或误差缺测但要附原因；`catalog_complete.csv` 是经纬度、深度、发震时刻、震级数值及其类型均有效的派生视图；`catalog_high_precision.csv` 另要求定位精度与稳定性门槛通过。输出视图均由同一个主目录和版本化筛选配置生成，不能手动各维护一份。

| 字段组 | 建议规范字段 | 单位／约定 |
|---|---|---|
| 身份 | `event_uid,run_id,catalog_source,detection_source` | 字符串；来源动态，不固定两类或固定数量 |
| 时空 | `origin_time_utc,longitude,latitude,depth_km` | UTC、度、km；深度基准见 manifest |
| 震级 | `magnitude,magnitude_type,magnitude_method,magnitude_calibration_id` | 数值与标度绑定；未测量写空；不以 0 填补，不混 ML／Ms／Mw |
| 定位来源 | `final_relocation_stage,location_source,model_hash,parameter_hash` | VELEST／hypoDD_dtct／hypoDD_dtcc 必须区分 |
| 支持度 | `n_p,n_s,n_location_stations,nccp,nccs,rms_absolute_s,rcc_s,azimuth_gap_deg` | 定位与测幅台数分开，定义与程序原字段逐项映射 |
| 震级质量 | `n_magnitude_stations,magnitude_mad,magnitude_mad_definition,magnitude_qc` | MAD 是否缩放必须显式写明 |
| 定位质量 | `location_qc,relative_stability_pass,absolute_accuracy_status` | 质量标签与定量误差分开 |
| 扰动误差 | `uncertainty_method,n_replicates,n_success,success_fraction,horizontal_p95_km,depth_p025_km,depth_p975_km` | 分位数围绕何种参考点必须声明 |
| 系统误差 | `velocity_sensitivity_horizontal_km,velocity_sensitivity_depth_km,station_jackknife_status` | 不与随机散布合并成虚构总误差 |
| 去重／回退 | `duplicate_group_id,template_event_uid,fallback_reason` | 保留被合并记录的追溯表 |

定位台站数与测幅台站数可能不同，契约应拆为`n_location_stations`与`n_magnitude_stations`；不要直接将含混的`n_station`解释为所有阶段的台站数。软件形式误差与另表的扰动结果也必须保留各自定义，不能改列名后假充相同误差。

目前`audit-catalog`验收的是**非空、震级齐全的complete／正式发布视图**，默认读取`magnitude`与`magnitude_type`。旧表的其他列名通过`--magnitude-column`／`--magnitude-type-column`显式映射；原表没有类型列时必须用`--default-magnitude-type`明确声明，工具不按文件名或数值猜测类型。不同标度分别统计，不转换后混合。带缺震级的`catalog_all`需先按显式规则提取complete视图，不能直接用此检查把缺测事件删除或判为假事件。工具只验收必填值、有限数、UID／精确重复、时间与来源闭合；尚未实现上述全部关系表和逐项科学验收。没有 `uncertainty_method` 会产生提示，不会伪造量化误差。

## 模板匹配扩展

模板匹配为可选分支：模板选取 → 匹配检测 → 跨模板去重 → 新事件震相／本地位置 → 可用的 dtct／dtcc → 震级与各自误差 → 与主链去重合并。匹配检测时间不等同最终发震时刻，模板 S 到时也不是新的独立人工观测。

绝对定位失败、双差断链或缺少 CC 支持的新事件，可按冻结规则保留低阶段位置，但必须标注；不能把模板位置或外部参考位置复制为本地高精度位置。总体数量可增加，新增事件的误差不能继承模板或其他来源事件的误差。

项目发布入口由该项目自己的manifest／registry选择；事件数、来源种类、部署数量和日期均从输入统计，不设置预期常数。历史案例放入`examples/<case>/`，只有显式选择时才能读取；通用工具和默认配置不依赖这些文件。
