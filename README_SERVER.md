
````markdown
# LogLLM 项目服务器运维指南

> **最后更新**: 2025-12-03
> **服务器平台**: 恒源云 (GPUGeek)
> **显卡配置**: RTX 3090 / 4090 (24GB)
> **环境状态**: 基础环境已配好，模型已备份至 OSS

## 🗺️ 1. 核心目录地图 (Where is What?)

| 资产类型 | 存放路径 (Path) | 状态说明 |
| :--- | :--- | :--- |
| **项目代码** | `/root/logllm` | **[系统盘]** 永久保存，关机不丢。 |
| **Conda环境**| `logllm` (Python 3.10) | **[系统盘]** 永久保存。 |
| **Llama-3** | `/hy-tmp/model_weights/LLM-Research/Meta-Llama-3-8B` | **[临时盘]** 关机>24h 会被**清空**。 |
| **BERT** | `/hy-tmp/model_weights/AI-ModelScope/bert-base-uncased` | **[临时盘]** 关机>24h 会被**清空**。 |
| **云端备份** | `oss://my_models/` | **[OSS云盘]** 永久冷备份，用于恢复数据。 |

---

## ⚡ 2. 开机恢复流程 (Disaster Recovery)

**⚠️ 警告**：如果服务器关机超过 24 小时，`/hy-tmp` 下的模型文件会丢失。开机后请务必先运行以下命令检查和恢复：

### 第一步：检查模型是否存在
```bash
ls -F /hy-tmp/model_weights/
````

*如果报错或文件夹为空，请执行下面的恢复命令。*

### 第二步：从 OSS 云盘“秒传”恢复

*(耗时约 3-5 分钟，走内网不耗流量)*

```bash
# 1. 进入临时盘
cd /hy-tmp

# 2. 拉取备份包 (两个模型)
oss cp oss://my_models/llama3_backup.zip .
oss cp oss://my_models/bert_backup.zip .

# 3. 解压模型
unzip -q llama3_backup.zip  # 解压 Llama-3 (-q 静默模式)
unzip -q bert_backup.zip    # 解压 BERT

# 4. 清理压缩包 (释放空间)
rm llama3_backup.zip bert_backup.zip
```

-----

## 🚀 3. 如何运行代码 (How to Run)

### 3.1 激活环境

```bash
conda activate logllm
```

### 3.2 运行测试脚本 (冒烟测试)

用于验证显卡是否正常，以及模型路径是否正确：

```bash
cd /root/logllm
python test_model.py
```

*预期输出：`✅ SUCCESS! Model loaded to GPU.`*

### 3.3 运行 LogLLM 主程序

**注意**：代码中的 `model_name` 和 `encoder_name` 必须使用以下绝对路径！

  * **Llama-3 路径**: `"/hy-tmp/model_weights/LLM-Research/Meta-Llama-3-8B"`
  * **BERT 路径**: `"/hy-tmp/model_weights/AI-ModelScope/bert-base-uncased"`

<!-- end list -->

```bash
# 运行示例 (根据实际脚本调整)
python main.py
```

-----

## 🔄 4. 开发工作流 (Git Workflow)

**不要直接在服务器上修改核心代码！** 请遵循以下流程：

1.  **本地电脑 (Local)**:
      * 修改代码 (VSCode/PyCharm)。
      * 提交推送: `git add .` -\> `git commit -m "update"` -\> `git push`。
2.  **服务器 (Server)**:
      * 拉取最新:
        ```bash
        cd /root/logllm
        git pull
        ```
      * 运行验证。

-----

## 🛠️ 5. 常用工具备忘 (Cheat Sheet)

  * **查看显存占用**: `nvidia-smi -l 1`
  * **查看临时盘空间**: `df -h | grep hy-tmp`
  * **OSS 工具命令**:
      * 查看云端文件: `oss ls oss://my_models/`
      * 上传文件: `oss cp <本地文件> oss://my_models/`
      * 下载文件: `oss cp oss://my_models/<云端文件> <本地路径>`

<!-- end list -->

```

---

### 🎉 恭喜你！
等你看到上传进度条跑完，并在本地保存好这份 Readme，你的**“基于 Llama-3 的 Log-BPD 实验环境”**就正式搭建完毕了。

现在，你可以放心地关机休息，或者开始你的代码魔改之旅了！如果有任何新问题，随时来找我。
```