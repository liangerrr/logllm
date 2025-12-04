# 服务器迁移后设置指南

## 📋 迁移后检查清单

### 1. 检查代码

```bash
cd /root/logllm
ls -la
# 确保有 eval_scripts/, prepareData/, model.py 等文件
```

### 2. 检查模型文件

```bash
# Llama 模型
ls /hy-tmp/model_weights/LLM-Research/Meta-Llama-3-8B

# BERT 模型
ls /hy-tmp/model_weights/AI-ModelScope/bert-base-uncased

# 如果不存在，从 OSS 恢复
cd /hy-tmp
oss cp oss://my_models/llama3_backup.zip .
unzip -q llama3_backup.zip
rm llama3_backup.zip

oss cp oss://my_models/bert_backup.zip .
unzip -q bert_backup.zip
rm bert_backup.zip
```

### 3. 恢复数据文件（从 OSS）

```bash
cd /root/logllm
conda activate logllm

# 从 OSS 下载数据（推荐，速度快）
python scripts/download_data_from_oss.py
```

或者手动检查：

```bash
# 检查原始数据
ls /hy-tmp/data/HDFS_data/HDFS.log
ls /hy-tmp/data/HDFS_data/anomaly_label.csv

# 检查是否已划分数据集
ls /hy-tmp/data/HDFS_data/test.csv
ls /hy-tmp/data/HDFS_data/train.csv
```

## 🔧 HDFS 数据预处理（如果还没有划分）

如果 `/hy-tmp/data/HDFS_data/test.csv` 不存在，需要先运行预处理：

```bash
cd /root/logllm
conda activate logllm

# 运行预处理脚本
python prepare_hdfs_data.py
```

这会生成：
- `/hy-tmp/data/HDFS_data/train.csv` - 训练集
- `/hy-tmp/data/HDFS_data/test.csv` - 测试集

## ✅ 验证环境

```bash
# 测试模型加载
python test_model.py

# 应该看到: ✅ SUCCESS! Model loaded to GPU.
```

## 🚀 运行评估

```bash
# 评估所有数据集
python eval_scripts/eval_all.py

# 或评估单个数据集
python eval_scripts/eval_hdfs.py
```

## 📂 数据目录结构（服务器）

```
/hy-tmp/data/
├── HDFS_data/
│   ├── HDFS.log              # 原始日志（必需）
│   ├── anomaly_label.csv     # 标签文件（必需）
│   ├── train.csv             # 预处理后生成
│   └── test.csv              # 预处理后生成
├── BGL/
│   ├── BGL.log
│   ├── train.csv
│   └── test.csv
├── Liberty/
│   └── ...
└── Thunderbird/
    └── ...
```

## 📤 上传数据到 OSS（备份）

如果数据在服务器上，可以上传到 OSS 备份：

```bash
cd /root/logllm
python scripts/upload_data_to_oss.py
```

这会上传所有数据集到 `oss://my_models/data/`，包括：
- 原始日志文件（.log）
- 标签文件（anomaly_label.csv）
- 预处理后的文件（train.csv, test.csv）

## ⚠️ 常见问题

### Q: 找不到 test.csv

**解决**: 运行预处理脚本生成
```bash
python prepare_hdfs_data.py  # HDFS
# 或
python prepareData/sliding_window.py  # BGL/Liberty/Thunderbird
```

### Q: 找不到模型文件

**解决**: 从 OSS 恢复（见步骤 2）

### Q: 数据路径不对

**解决**: 检查 `prepareData/session_window.py` 和 `prepareData/sliding_window.py` 中的 `data_dir` 路径

