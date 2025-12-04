#!/usr/bin/env python3
"""
从 OSS 下载数据集

使用方法:
python scripts/download_data_from_oss.py
"""

import os
import subprocess
from pathlib import Path

# OSS 配置
OSS_BUCKET = "oss://my_models/"
DATA_DIR = "/hy-tmp/data"

def download_from_oss(oss_path, local_path):
    """从 OSS 下载文件"""
    # 确保本地目录存在
    os.makedirs(os.path.dirname(local_path), exist_ok=True)
    
    print(f"下载: {oss_path} -> {local_path}")
    result = subprocess.run(
        ["oss", "cp", oss_path, local_path],
        capture_output=True,
        text=True
    )
    if result.returncode == 0:
        print(f"✅ 下载成功: {local_path}")
        return True
    else:
        print(f"⚠️  下载失败或文件不存在: {oss_path}")
        return False

def main():
    print("=" * 60)
    print("从 OSS 下载数据集")
    print("=" * 60)
    
    datasets = {
        'HDFS_data': {
            'files': ['HDFS.log', 'anomaly_label.csv', 'train.csv', 'test.csv'],
            'optional': ['train_info.txt', 'test_info.txt', 'HDFS.log_structured.csv']
        },
        'BGL': {
            'files': ['BGL.log', 'train.csv', 'test.csv'],
            'optional': ['train_info.txt', 'test_info.txt', 'BGL.log_structured.csv']
        },
        'Liberty': {
            'files': ['Liberty.log', 'train.csv', 'test.csv'],
            'optional': ['train_info.txt', 'test_info.txt', 'Liberty.log_structured.csv']
        },
        'Thunderbird': {
            'files': ['Thunderbird.log', 'train.csv', 'test.csv'],
            'optional': ['train_info.txt', 'test_info.txt', 'Thunderbird.log_structured.csv']
        }
    }
    
    print(f"\nOSS 路径: {OSS_BUCKET}data/")
    print(f"本地目录: {DATA_DIR}\n")
    
    # 创建数据目录
    os.makedirs(DATA_DIR, exist_ok=True)
    
    for dataset_name, config in datasets.items():
        local_dir = os.path.join(DATA_DIR, dataset_name)
        os.makedirs(local_dir, exist_ok=True)
        
        print(f"\n处理数据集: {dataset_name}")
        print("-" * 60)
        
        # 下载必需文件
        for filename in config['files']:
            oss_path = f"{OSS_BUCKET}data/{dataset_name}/{filename}"
            local_path = os.path.join(local_dir, filename)
            download_from_oss(oss_path, local_path)
        
        # 下载可选文件
        for filename in config.get('optional', []):
            oss_path = f"{OSS_BUCKET}data/{dataset_name}/{filename}"
            local_path = os.path.join(local_dir, filename)
            download_from_oss(oss_path, local_path)
    
    print("\n" + "=" * 60)
    print("✅ 下载完成！")
    print("=" * 60)
    print(f"\n数据已保存到: {DATA_DIR}")
    print("\n检查文件:")
    for dataset_name in datasets.keys():
        local_dir = os.path.join(DATA_DIR, dataset_name)
        if os.path.exists(local_dir):
            files = os.listdir(local_dir)
            print(f"  {dataset_name}: {len(files)} 个文件")

if __name__ == '__main__':
    main()

