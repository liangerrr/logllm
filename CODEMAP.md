# LogLLM 项目代码地图

> **最后更新**: 2025-12-04  
> **项目结构**: 代码、数据、脚本分离

## 📁 目录结构

```
LogLLM/
├── data/                          # 数据目录（本地生成的数据）
│   └── HDFS_data/                 # HDFS 数据集转换后的文件
│       ├── HDFS.log              # 原始日志文件
│       └── anomaly_label.csv     # BlockId 和 Label 映射
│
├── scripts/                       # 工具脚本目录
│   ├── download_hdfs.py          # 下载 HDFS 数据集
│   ├── convert_hdfs.py            # 转换数据集格式
│   └── test_huggingface.py       # 测试 HuggingFace 连接
│
├── prepareData/                   # 数据预处理脚本
│   ├── helper.py                 # 辅助函数（窗口、日志解析等）
│   ├── sliding_window.py         # 滑动窗口（BGL/Thunderbird/Liberty）
│   └── session_window.py         # 会话窗口（HDFS）
│
├── ft_model_*/                   # 微调后的模型权重
│   ├── Bert_ft/                  # BERT LoRA 适配器
│   ├── Llama_ft/                 # Llama LoRA 适配器
│   └── projector.pt              # 投影层权重
│
├── model.py                       # LogLLM 模型定义
├── customDataset.py               # 自定义数据集和采样器
├── train.py                       # 训练脚本
├── eval.py                        # 评估脚本
├── test_model.py                  # 模型测试脚本
├── requirements.txt               # 依赖列表
└── README.md                      # 项目说明
```

---

## 🔄 数据流程

### 1. 数据下载和转换（本地）

```bash
# 步骤 1: 下载数据集
cd scripts
python download_hdfs.py
# 输出: /Users/lc/PycharmProjects/HDFS_v1 (HuggingFace 格式)

# 步骤 2: 转换格式
python convert_hdfs.py
# 输出: data/HDFS_data/HDFS.log 和 anomaly_label.csv
```

### 2. 数据预处理（服务器）

```bash
# 上传 data/HDFS_data/ 到服务器 /mnt/public/gw/SyslogData/HDFS_v1/

# 在服务器上运行预处理
python prepareData/session_window.py
# 输出: train.csv 和 test.csv
```

### 3. 训练和评估（服务器）

```bash
# 训练
python train.py

# 评估
python eval.py
```

---

## 📝 核心文件说明

### `model.py` - LogLLM 模型

- **LogLLM 类**: 主模型类
  - `Bert_path`: BERT 模型路径
  - `Llama_path`: Llama 模型路径
  - `ft_path`: 微调权重路径（可选）
- **关键方法**:
  - `train_helper()`: 训练时的前向传播
  - `forward()`: 推理时的前向传播
  - `save_ft_model()`: 保存微调权重

### `customDataset.py` - 数据集处理

- **CustomDataset**: 从 CSV 读取日志序列
- **CustomCollator**: 批处理和数据打包
- **BalancedSampler**: 平衡采样器（处理类别不平衡）

### `train.py` - 训练流程

**多阶段训练**:
1. **Phase 1**: 只训练 Llama (`set_train_only_Llama`)
2. **Phase 2-1**: 只训练 projector (`set_train_only_projector`)
3. **Phase 2-2**: 训练 projector + Bert (`set_train_projectorAndBert`)
4. **Phase 3**: 端到端微调 (`set_finetuning_all`)

### `eval.py` - 评估流程

- 加载微调后的模型
- 在测试集上推理
- 计算 precision, recall, F1, accuracy

### `prepareData/` - 数据预处理

- **sliding_window.py**: BGL/Thunderbird/Liberty 数据集
  - 使用固定大小窗口分组日志
  - 生成 `train.csv` 和 `test.csv`
- **session_window.py**: HDFS 数据集
  - 按 BlockId 分组日志
  - 需要 `anomaly_label.csv` 文件

---

## 🗂️ 数据路径配置

### 本地（Mac）

- **HuggingFace 数据集**: `/Users/lc/PycharmProjects/HDFS_v1`
- **转换后的数据**: `data/HDFS_data/`
  - `HDFS.log`
  - `anomaly_label.csv`

### 服务器（Linux）

- **模型路径**:
  - Llama: `/hy-tmp/model_weights/LLM-Research/Meta-Llama-3-8B`
  - BERT: `/hy-tmp/model_weights/AI-ModelScope/bert-base-uncased`
- **数据路径**: `/mnt/public/gw/SyslogData/{dataset_name}/`
  - `train.csv`
  - `test.csv`

---

## 🚀 快速开始

### 本地环境（数据转换）

```bash
# 1. 安装依赖
pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple datasets pandas pyarrow tqdm

# 2. 设置 HuggingFace token
export HF_TOKEN=your_token

# 3. 下载和转换数据
cd scripts
python download_hdfs.py
python convert_hdfs.py
```

### 服务器环境（训练/评估）

```bash
# 1. 激活环境
conda activate logllm

# 2. 上传数据到服务器

# 3. 运行预处理
python prepareData/session_window.py

# 4. 训练或评估
python train.py
python eval.py
```

---

## 📊 数据集支持

| 数据集 | 预处理脚本 | 微调模型 | LogLLM F1 |
|:------|:---------|:--------|:---------|
| **HDFS** | `session_window.py` | `ft_model_HDFS/` | 0.997 |
| **BGL** | `sliding_window.py` | `ft_model_BGL/` | 0.916 |
| **Liberty** | `sliding_window.py` | `ft_model_Liberty/` | 0.958 |
| **Thunderbird** | `sliding_window.py` | `ft_model_Thunderbird/` | 0.966 |

---

## 🔧 脚本说明

### `scripts/download_hdfs.py`

从 HuggingFace 下载 HDFS_v1 数据集。

**使用方法**:
```bash
python scripts/download_hdfs.py
```

**输出**: `/Users/lc/PycharmProjects/HDFS_v1` (HuggingFace datasets 格式)

### `scripts/convert_hdfs.py`

将 HuggingFace datasets 格式转换为代码需要的格式。

**使用方法**:
```bash
python scripts/convert_hdfs.py
```

**输入**: `/Users/lc/PycharmProjects/HDFS_v1`  
**输出**: `data/HDFS_data/HDFS.log` 和 `anomaly_label.csv`

### `scripts/test_huggingface.py`

测试 HuggingFace 连接和认证状态。

**使用方法**:
```bash
python scripts/test_huggingface.py
```

---

## ⚙️ 配置要点

### 训练配置 (`train.py`)

```python
dataset_name = 'HDFS_v1'  # 或 'BGL', 'Liberty', 'Thunderbird'
Bert_path = "/hy-tmp/model_weights/AI-ModelScope/bert-base-uncased"
Llama_path = "/hy-tmp/model_weights/LLM-Research/Meta-Llama-3-8B"
data_path = f'/mnt/public/gw/SyslogData/{dataset_name}/train.csv'
```

### 评估配置 (`eval.py`)

```python
dataset_name = 'HDFS_v1'
data_path = f'/mnt/public/gw/SyslogData/{dataset_name}/test.csv'
ft_path = f"ft_model_{dataset_name}"  # 自动加载对应微调模型
```

---

## 📌 注意事项

1. **本地和服务器环境分离**:
   - 本地：只安装数据处理依赖（datasets, pandas, pyarrow, tqdm）
   - 服务器：安装完整依赖（PyTorch, transformers, peft 等）

2. **数据路径**:
   - 本地生成的数据在 `data/` 目录
   - 需要上传到服务器的 `/mnt/public/gw/SyslogData/` 目录

3. **模型路径**:
   - 服务器上的模型路径是固定的（见 README_SERVER.md）
   - 本地不需要模型文件

4. **HuggingFace Token**:
   - 下载数据集需要 token
   - 在环境变量中设置 `HF_TOKEN`

---

**Happy Coding! 🚀**

