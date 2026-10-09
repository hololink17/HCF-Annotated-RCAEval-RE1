# 修订记录（CHANGELOG）

本文件记录 `HCF-Annotated-RCAEval (RE1)` 数据集的版本变更、改动范围与原因。
数据版本与 `README.md` 顶部标注的版本号一致。

---

## [1.1] — 2026-10

### 改动（Changed）

- **`hcf_annotations.csv`：25 个 `disk` 案例中的 20 个，其 `hcf_codes` 取值更新**，
  由单一诊断码增补为两个诊断码：
  - **16 例**：`E01` → `E01;E05`
  - **4 例**：`E01` → `E01;E10`
- **`baseline_vs_hcf.csv` 同步更新：60 个单元格**（上述 20 个案例 × 3 种基线方法各 1 行）。
- 两份文件修改单元格合计：**80 个**，全部位于 `hcf_codes` 字段。

### 原因（Reason）

对 `disk` 与 `loss` 两个子集，上游分析代码在提取与延迟相关的聚合指标时使用了
**固定的聚合键名**，而这两个子集数据中的**可用指标列名与其他子集不同构**。
其后果是：与该延迟指标相关的两类诊断码在这两个子集上**始终无法被触发**——
取不到键不会报错，流程照常完成，因此该情形在产物上表现为「这些案例只有 `E01`」。

修正聚合取键、使该指标在 `disk` 子集上可被正确读取后，**25 个 `disk` 案例中有 20 个**
新增一条与该延迟指标相关的诊断码（即上表）。`loss` 子集不在本数据集标注范围内，不受影响。

> 说明：本次修正只涉及**诊断码的取值本身**，不涉及任何检出判定与统计口径。

### 影响范围（Impact）

| 项目 | 是否变化 |
|---|---|
| 案例总数（147） | **不变** |
| `case_id` 及其顺序 | **不变** |
| 定位字段 `dataset` / `service` / `fault` / `repeat_no` | **不变** |
| `hcf_detected` | **不变**（147 例全部为 `TRUE`） |
| 三类基线（`pca_*` / `iforest_*` / `ocsvm_*`） | **不变** |
| `hcf_codes`（`hcf_annotations.csv`） | **20 个单元格变化**（见上表） |
| `hcf_codes`（`baseline_vs_hcf.csv`） | **60 个单元格变化**（同 20 例 × 3 方法）；其余列与 `hcf_status` 不变 |

`hcf_codes` 整体取值分布（全 147 例）：

| 取值 | 1.0 | 1.1 |
|---|---|---|
| `E01` | 60 | **40** |
| `E05` | 25 | 25 |
| `E01;E05` | 10 | **26** |
| `E01;E10` | 17 | **21** |
| `E01;E03;E05` | 29 | 29 |
| `E01;E03;E10` | 6 | 6 |

### 包内一致性

修订后，`hcf_annotations.csv` 与 `baseline_vs_hcf.csv` 中**同一 `case_id` 的 `hcf_codes`
完全一致**（全 147 个已标注案例逐一交叉比对，0 处不一致）。

### 逐案例对照表（20 例）

| `case_id` | 1.0 | 1.1 |
|---|---|---|
| `RE1-OB_adservice_disk_1` | `E01` | `E01;E10` |
| `RE1-OB_adservice_disk_2` | `E01` | `E01;E10` |
| `RE1-OB_adservice_disk_3` | `E01` | `E01;E10` |
| `RE1-OB_adservice_disk_4` | `E01` | `E01;E05` |
| `RE1-OB_adservice_disk_5` | `E01` | `E01;E10` |
| `RE1-OB_cartservice_disk_1` | `E01` | `E01;E05` |
| `RE1-OB_cartservice_disk_2` | `E01` | `E01;E05` |
| `RE1-OB_cartservice_disk_3` | `E01` | `E01;E05` |
| `RE1-OB_cartservice_disk_4` | `E01` | `E01;E05` |
| `RE1-OB_cartservice_disk_5` | `E01` | `E01;E05` |
| `RE1-OB_currencyservice_disk_1` | `E01` | `E01;E05` |
| `RE1-OB_currencyservice_disk_2` | `E01` | `E01;E05` |
| `RE1-OB_currencyservice_disk_3` | `E01` | `E01;E05` |
| `RE1-OB_currencyservice_disk_4` | `E01` | `E01;E05` |
| `RE1-OB_currencyservice_disk_5` | `E01` | `E01;E05` |
| `RE1-OB_productcatalogservice_disk_1` | `E01` | `E01;E05` |
| `RE1-OB_productcatalogservice_disk_2` | `E01` | `E01;E05` |
| `RE1-OB_productcatalogservice_disk_3` | `E01` | `E01;E05` |
| `RE1-OB_productcatalogservice_disk_4` | `E01` | `E01;E05` |
| `RE1-OB_productcatalogservice_disk_5` | `E01` | `E01;E05` |

---

## [1.0] — 2026-09

### 新增（Added）

- 首次发布：147 个故障注入案例的 HCF 逐案例诊断码标注
  （RE1-OB `cpu` 22 ＋ `delay` 25 ＋ `disk` 25 ＋ `mem` 25；RE1-SS `cpu` 25；RE1-TT `cpu` 25）。
- 三种无监督基线（PCA / Isolation Forest / OC-SVM）在相同逐案例协议下的检出标志与 AUC。
- 数据集说明、字段说明、评估协议与引用信息（见 `README.md`）。
