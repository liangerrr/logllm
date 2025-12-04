# 评估脚本目录

这个目录包含所有数据集的评估脚本。

## 📁 文件说明

### 单个数据集评估

- `eval_hdfs.py` - 评估 HDFS 数据集
- `eval_bgl.py` - 评估 BGL 数据集
- `eval_liberty.py` - 评估 Liberty 数据集
- `eval_thunderbird.py` - 评估 Thunderbird 数据集

### 总评估脚本

- `eval_all.py` - 一次性评估所有数据集

## 📂 数据路径（服务器）

所有脚本从以下路径读取测试数据：

```
/hy-tmp/data/
├── HDFS_data/
│   └── test.csv
├── BGL/
│   └── test.csv
├── Liberty/
│   └── test.csv
└── Thunderbird/
    └── test.csv
```

**注意**: 
- 这些路径是服务器上的绝对路径（临时盘）
- 确保在服务器上运行前，对应的 `test.csv` 文件已经存在
- 如果只有原始日志文件（如 `HDFS.log`），需要先运行预处理脚本生成 `test.csv`

## 🚀 使用方法

### 评估单个数据集

```bash
cd /root/logllm
conda activate logllm

# 评估 HDFS
python eval_scripts/eval_hdfs.py

# 评估 BGL
python eval_scripts/eval_bgl.py

# 评估 Liberty
python eval_scripts/eval_liberty.py

# 评估 Thunderbird
python eval_scripts/eval_thunderbird.py
```

### 评估所有数据集（推荐）

```bash
cd /root/logllm
conda activate logllm

python eval_scripts/eval_all.py
```

这会依次评估所有4个数据集，并输出汇总结果表格。

## ⚠️ 运行前检查

在服务器上运行前，请确保：

1. **测试数据已准备好**:
   ```bash
   ls /hy-tmp/data/HDFS_data/test.csv
   ls /hy-tmp/data/BGL/test.csv
   ls /hy-tmp/data/Liberty/test.csv
   ls /hy-tmp/data/Thunderbird/test.csv
   ```
   
   如果只有原始日志文件，需要先运行预处理：
   ```bash
   # HDFS: 需要 HDFS.log 和 anomaly_label.csv
   # 编辑 prepareData/session_window.py 设置 data_dir = '/hy-tmp/data/HDFS_data'
   python prepareData/session_window.py
   
   # BGL/Liberty/Thunderbird: 需要对应的 .log 文件
   # 编辑 prepareData/sliding_window.py 设置 data_dir
   python prepareData/sliding_window.py
   ```

2. **微调模型已存在**:
   ```bash
   ls /root/logllm/ft_model_HDFS/
   ls /root/logllm/ft_model_BGL/
   ls /root/logllm/ft_model_Liberty/
   ls /root/logllm/ft_model_Thunderbird/
   ```

3. **基础模型路径正确**:
   - Llama: `/hy-tmp/model_weights/LLM-Research/Meta-Llama-3-8B`
   - BERT: `/hy-tmp/model_weights/AI-ModelScope/bert-base-uncased`

## 📊 输出格式

每个评估脚本会输出：
- Precision（精确率）
- Recall（召回率）
- F1 Score
- Accuracy（准确率）

`eval_all.py` 还会输出一个汇总表格，包含所有数据集的结果和平均 F1 Score。

