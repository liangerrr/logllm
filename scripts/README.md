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

## 🔄 完整流程

```bash
# 1. 测试连接
python scripts/test_huggingface.py

# 2. 下载数据集
python scripts/download_hdfs.py

# 3. 转换格式
python scripts/convert_hdfs.py

# 4. 上传到服务器
# 将 data/HDFS_data/ 上传到服务器 /mnt/public/gw/SyslogData/HDFS_v1/
```

