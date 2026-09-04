# HCF-Annotated-RCAEval (RE1)

**根因定位诊断级标注数据集（派生标注层）** · 版本 1.0 · 2026-09

> 为 147 个微服务故障注入案例提供 HCF（Holographic Coding Framework，全息编码框架）
> 逐案例诊断码标注，以及三种无监督异常检测基线方法在相同逐案例协议下的对照结果。

---

## 一、数据集简介

本数据集是在 [RCAEval](https://arxiv.org/abs/2412.17015) 基准（RE1 数据，微服务故障注入）之上构建的
"诊断级标注层"：

- **147 个故障注入案例**的 HCF 逐案例诊断码标注（如 `E01;E03;E05`）
- 三种无监督基线（PCA / Isolation Forest / OC-SVM）在相同逐案例协议下的检出与 AUC

**定位**：现有微服务根因定位数据多为原始观测数据（指标/日志/Trace），
本数据集补充的是稀缺的"诊断级标注"——每个案例除故障类型与根因服务标签外，
还带有结构化诊断码标注，可直接用于根因定位方法的**诊断粒度评测**。

## 二、来源与派生关系（重要）

- **原始数据**：RCAEval (Pham et al., 2024, [arXiv:2412.17015](https://arxiv.org/abs/2412.17015))，
  RE1 子集（Online Boutique / Sock Shop / Train Ticket 三个微服务架构的故障注入数据）。
- **本数据集为派生标注层，不包含任何原始监控数据**。原始数据请从 RCAEval 官方渠道获取，
  其许可条款以官方发布为准。
- 使用本数据集时必须同时引用 RCAEval 原始数据集。

**数据可获得性（Data Availability）：** 本目录仅包含派生标注层（HCF 诊断码 +
三类基线逐案例结果）。RCAEval 原始监控数据（指标序列、日志、调用链等）需通过
Pham 等的 RCAEval 仓库（参见 §七 引用）按其官方许可获取；本数据集不打包原始
监控数据，也不代理其分发。HCF 的领域阈值表、冲突矩阵数值与诊断码-干预动作
映射表为专利保护的专有内容，不在本数据集或本论文范围内公开。

## 三、覆盖范围

HCF 逐案例诊断码标注覆盖 **147 个**故障注入案例（基线对比全量 300 案例 =
100 案例 × 3 数据集；标注分布与主稿 §6.4 披露一致）：

| 子集 | 架构 | HCF 标注案例构成 | 小计 | 基线全量 |
|---|---|---|---|---|
| RE1-OB | Online Boutique | cpu 22 + delay 25 + disk 25 + mem 25 | 97 | 100（cpu/delay/disk/mem 各 25）|
| RE1-SS | Sock Shop | cpu 25 | 25 | 100（cpu/delay/disk/mem 各 25）|
| RE1-TT | Train Ticket | cpu 25 | 25 | 100（cpu/delay/disk/mem 各 25）|
| **合计** | | | **147** | **300** |

HCF 标注未覆盖 RE1-SS/RE1-TT 的 delay/disk/mem 子集（150 案例），其余案例
的 HCF 输出可用同一管线直接生成，不影响本对比结论；范围限制与主稿
§6.4 一致。

## 四、文件清单

| 文件 | 说明 |
|---|---|
| `hcf_annotations.csv` | 【核心】147 案例的逐案例标注：故障类型、根因服务、注入时间戳、窗口行数、HCF 检出与诊断码、三种基线的检出与 AUC |
| `baseline_per_case.csv` | 300 案例 × 3 基线方法的逐案例明细（训练/校准/测试行数、报警占比、检出、AUC） |
| `baseline_summary.csv` | 按数据集 × 故障类型 × 方法汇总的检出率与平均 AUC（全 300 案例） |
| `baseline_vs_hcf.csv` | 300 案例的基线结果与 HCF 匹配状态完整对照表（NA=该案例无 HCF 输出） |
| `baseline_sliding.csv` | 滑动窗口分析：W1 健康窗口误报标志与首报窗口（300 案例 × 3 方法） |
| `baseline_sliding_windows.csv` | 滑动窗口 W1-W6 原始得分 |
| `README.md` | 本文件 |
| `LICENSE` | CC BY 4.0 许可证 |

**示例样例（hcf_annotations.csv 首条记录，字段对应见 §五）：**

```
case_id,dataset,service,fault,repeat_no,inject_time_unix,n_train,n_cal,n_ab,hcf_detected,hcf_codes,pca_detected,pca_auc,iforest_detected,iforest_auc,ocsvm_detected,ocsvm_auc
RE1-OB_adservice_cpu_1,RE1-OB,adservice,cpu,1,1685202688,180,120,300,TRUE,E01,TRUE,0.998,TRUE,0.672,TRUE,0.999
```

## 五、hcf_annotations.csv 字段说明

| 字段 | 说明 |
|---|---|
| `case_id` | 案例标识：`{数据集}_{服务}_{故障}_{重复编号}` |
| `dataset` | RE1-OB / RE1-SS / RE1-TT |
| `service` | 注入目标服务（根因服务标签；TT 服务名中连字符归一化为点号，与原始目录名 `ts-auth-service` 对应） |
| `fault` | 故障类型：cpu / mem / delay / disk |
| `repeat_no` | 重复实验编号 |
| `inject_time_unix` | 故障注入时刻（Unix 时间戳，取自案例目录 `inject_time.txt`） |
| `n_train/n_cal/n_ab` | 训练行数 / 校准行数 / 故障窗口行数 |
| `hcf_detected` | HCF 检出标志（全部 147 例均为 TRUE） |
| `hcf_codes` | HCF 诊断码（分号分隔，如 `E01;E03;E05`） |
| `pca_detected` 等 | 三种基线（PCA / Isolation Forest / OC-SVM）的检出标志与该案例 AUC |

## 六、评估协议（基线方法）

与 HCF 分析严格对齐的逐案例（per-case）协议：

- **训练**：该案例注入前健康窗口（5 分钟）的前 60% 行
- **校准**：健康窗口后 40% 行，取 99 分位为阈值（名义误报率 1%）
- **测试**：注入后 5 分钟故障窗口
- **检出判据**：故障窗口中超过阈值的行占比 >= 10%
- 每案例检测器只用自身注入前数据训练，与 HCF 可用信息相同
- W1 健康窗口误报率：全部方法为 0%

## 七、引用

```bibtex
@article{liu_hcf_annotated_rcaeval,
  title   = {HCF-Annotated RCAEval (RE1): A Diagnostic-Level Annotated Dataset for Root Cause Analysis},
  author  = {Liu, Xiangyu},
  year    = {2026},
  note    = {Derived from RCAEval; CC BY 4.0}
}

@article{pham_rcaeval_2024,
  title   = {RCAEval: A Benchmark for Root Cause Analysis of Microservice Systems with Telemetry Data},
  author  = {Pham, Luan and Zhang, Hongyu and Ha, Huong and Salim, Flora and Zhang, Xiuzhen},
  year    = {2024},
  journal = {arXiv preprint},
  eprint  = {2412.17015}
}
```

1. 原始数据集（**必须引用**）：Pham, L., Zhang, H., Ha, H., Salim, F., Zhang, X. *RCAEval: A Benchmark for
   Root Cause Analysis of Microservice Systems with Telemetry Data*. arXiv:2412.17015, 2024.
2. HCF 方法：Xiangyu Liu. *Holographic Coding Framework 软件系统验证论文*
   （投稿于 IEEE Transactions on Software Engineering）。

## 八、边界与披露说明

- 本数据集**不包含** HCF 的领域阈值表、冲突矩阵数值与诊断码-干预动作映射表
  （该部分为专利保护的专有内容）；`hcf_codes` 仅提供码值序列本身用于诊断粒度评测。
- RE1-OB_LOSS（丢包）案例因监控栈未采集该指标而被排除（与论文口径一致）。
- 未检出案例与 OC-SVM 在 SS/TT 上的高维退化现象均如实保留，未做挑选。

## 九、许可证

本数据集以 [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) 授权（详见 `LICENSE`）。
使用或引用时必须同时署名并引用 RCAEval 原始数据集与 HCF 方法论文。

## 十、联系方式

Xiangyu Liu（通讯作者）
Email: liuxiangyu@liuxiangyu.com.cn
