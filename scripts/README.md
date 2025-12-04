# Scripts 工具脚本目录

## 📁 脚本说明

### `download_hdfs.py` - 下载 HDFS 数据集

从 HuggingFace 下载 HDFS_v1 数据集。

**使用方法**:
```bash
# 设置 token（如果还没设置）
export HF_TOKEN=your_token

# 运行下载
python scripts/download_hdfs.py
```

**输出**: `/Users/lc/PycharmProjects/HDFS_v1` (HuggingFace datasets 格式)

---

### `convert_hdfs.py` - 转换数据格式

将 HuggingFace datasets 格式转换为代码需要的格式。

**使用方法**:
```bash
python scripts/convert_hdfs.py
```

**输入**: `/Users/lc/PycharmProjects/HDFS_v1`  
**输出**: `data/HDFS_data/HDFS.log` 和 `anomaly_label.csv`

---

### `test_huggingface.py` - 测试连接

测试 HuggingFace 连接和认证状态。

**使用方法**:
```bash
python scripts/test_huggingface.py
```

---

### `upload_data_to_oss.py` - 上传数据到 OSS（服务器上运行）

将服务器上的数据集上传到 OSS 备份。

**使用方法**（在服务器上）:
```bash
cd /root/logllm
python scripts/upload_data_to_oss.py
```

**上传内容**:
- 原始日志文件（.log）
- 标签文件（anomaly_label.csv）
- 预处理后的文件（train.csv, test.csv）

**OSS 路径**: `oss://my_models/data/`

---

### `download_data_from_oss.py` - 从 OSS 下载数据（服务器上运行）

从 OSS 下载数据集到服务器。

**使用方法**（在服务器上）:
```bash
cd /root/logllm
python scripts/download_data_from_oss.py
```

**下载到**: `/hy-tmp/data/`

---

## 🔄 完整流程

### 本地（Mac）

```bash
# 1. 测试连接
python scripts/test_huggingface.py

# 2. 下载数据集
python scripts/download_hdfs.py

# 3. 转换格式
python scripts/convert_hdfs.py
# 输出: data/HDFS_data/HDFS.log 和 anomaly_label.csv
```

### 服务器（Linux）

```bash
# 方式 1: 从 OSS 下载（推荐，速度快）
cd /root/logllm
python scripts/download_data_from_oss.py

# 方式 2: 从本地上传（如果 OSS 没有备份）
# 将本地 data/HDFS_data/ 上传到服务器 /hy-tmp/data/HDFS_data/

# 运行预处理（如果还没有 train.csv 和 test.csv）
python prepare_hdfs_data.py

# 上传到 OSS 备份（可选，方便下次恢复）
python scripts/upload_data_to_oss.py
```

