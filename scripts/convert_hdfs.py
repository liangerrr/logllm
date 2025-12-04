#!/usr/bin/env python3
"""
将 HuggingFace HDFS_v1 数据集转换为代码需要的格式

输入: /Users/lc/PycharmProjects/HDFS_v1 (HuggingFace datasets 格式)
输出: 
  - HDFS.log (原始日志文件)
  - anomaly_label.csv (BlockId 和 Label 映射)
"""

import os
import pandas as pd
from pathlib import Path
from tqdm import tqdm
from datasets import load_from_disk

# 输入路径（HuggingFace 数据集目录）
input_dir = "/Users/lc/PycharmProjects/HDFS_v1"

# 输出路径（本地路径）
output_dir = "/Users/lc/PycharmProjects/LogLLM/data/HDFS_data"
log_name = "HDFS.log"
anomaly_label_file = "anomaly_label.csv"

def convert_hdfs_dataset():
    """
    将 HuggingFace datasets 格式转换为代码需要的格式
    """
    print("=" * 60)
    print("HDFS_v1 数据集格式转换工具")
    print("=" * 60)
    
    # 步骤 1: 读取数据集
    print("\n步骤 1: 读取 HuggingFace 数据集...")
    
    try:
        ds = load_from_disk(input_dir)
        print(f"✅ 数据集加载成功！")
        print(f"数据集分割: {list(ds.keys())}")
    except Exception as e:
        print(f"❌ 加载失败: {e}")
        print(f"\n请先运行下载脚本:")
        print(f"  python download_hdfs.py")
        return
    
    # 合并所有分割
    all_data = []
    for split_name, split_data in ds.items():
        print(f"处理分割: {split_name} ({len(split_data)} 条记录)")
        all_data.append(split_data)
    
    # 转换为 pandas DataFrame
    if len(all_data) == 1:
        df_all = all_data[0].to_pandas()
    else:
        from datasets import concatenate_datasets
        combined = concatenate_datasets(all_data)
        df_all = combined.to_pandas()
    
    print(f"✅ 总共读取 {len(df_all)} 条日志记录")
    print(f"列名: {df_all.columns.tolist()}")
    
    # 步骤 2: 生成 HDFS.log 文件
    print("\n步骤 2: 生成 HDFS.log 文件...")
    
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)
    log_file_path = os.path.join(output_dir, log_name)
    
    # 组合日志行：Date Time Pid Level Component: Content
    with open(log_file_path, 'w', encoding='utf-8') as f:
        for _, row in tqdm(df_all.iterrows(), total=len(df_all), desc="写入日志"):
            date = str(row.get('date', ''))
            time = str(row.get('time', ''))
            pid = str(row.get('pid', ''))
            level = str(row.get('level', ''))
            component = str(row.get('component', ''))
            content = str(row.get('content', ''))
            
            # 组合成原始日志格式
            log_line = f"{date} {time} {pid} {level} {component}: {content}"
            f.write(log_line + '\n')
    
    print(f"✅ 日志文件已保存: {log_file_path}")
    
    # 步骤 3: 生成 anomaly_label.csv
    print("\n步骤 3: 生成 anomaly_label.csv 文件...")
    
    # 从 block_id 和 anomaly 列提取 BlockId 和 Label 映射
    block_label_dict = {}
    
    for _, row in tqdm(df_all.iterrows(), total=len(df_all), desc="提取 BlockId 标签"):
        block_ids_str = str(row.get('block_id', ''))
        anomaly = row.get('anomaly', 0)
        
        # block_id 可能是空格分隔的多个 BlockId
        if block_ids_str and block_ids_str != 'nan' and block_ids_str.strip():
            block_ids = block_ids_str.strip().split()
            for block_id in block_ids:
                if block_id:
                    # 如果 BlockId 已经存在，保留异常标签（1 优先于 0）
                    if block_id not in block_label_dict:
                        block_label_dict[block_id] = anomaly
                    elif anomaly == 1:
                        block_label_dict[block_id] = 1
    
    # 转换为 DataFrame
    label_data = []
    for block_id, anomaly in block_label_dict.items():
        label_data.append({
            'BlockId': block_id,
            'Label': 'Anomaly' if anomaly == 1 else 'Normal'
        })
    
    label_df = pd.DataFrame(label_data)
    label_file_path = os.path.join(output_dir, anomaly_label_file)
    label_df.to_csv(label_file_path, index=False)
    
    print(f"✅ 标签文件已保存: {label_file_path}")
    print(f"   共 {len(label_df)} 个 BlockId")
    print(f"   异常数量: {(label_df['Label'] == 'Anomaly').sum()}")
    print(f"   正常数量: {(label_df['Label'] == 'Normal').sum()}")
    
    # 步骤 4: 验证数据
    print("\n步骤 4: 数据验证...")
    print(f"日志文件行数: {len(df_all)}")
    print(f"唯一 BlockId 数量: {len(label_df)}")
    
    # 检查日志文件大小
    log_size_mb = os.path.getsize(log_file_path) / (1024 * 1024)
    print(f"日志文件大小: {log_size_mb:.2f} MB")
    
    print("\n" + "=" * 60)
    print("✅ 转换完成！")
    print("=" * 60)
    print(f"\n生成的文件:")
    print(f"  - {log_file_path}")
    print(f"  - {label_file_path}")
    print(f"\n下一步:")
    print(f"1. 将文件上传到服务器: {output_dir}")
    print(f"   服务器目标路径: /mnt/public/gw/SyslogData/HDFS_v1/")
    print(f"2. 在服务器上运行预处理: python prepareData/session_window.py")
    print(f"3. 运行评估: python eval.py (设置 dataset_name = 'HDFS_v1')")


if __name__ == '__main__':
    # 检查输入目录是否存在
    if not os.path.exists(input_dir):
        print(f"❌ 错误: 输入目录不存在: {input_dir}")
        print(f"请先运行下载脚本:")
        print(f"  python download_hdfs.py")
        exit(1)
    
    convert_hdfs_dataset()

