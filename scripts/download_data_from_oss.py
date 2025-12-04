#!/usr/bin/env python3
"""
从 OSS 下载数据集（解压 zip）

使用方法:
python scripts/download_data_from_oss.py
"""

import os
import subprocess
import zipfile
import tempfile
from pathlib import Path

# OSS 配置
OSS_BUCKET = "oss://my_models/"
DATA_DIR = "/hy-tmp/data"

def download_and_extract(oss_path, dataset_name):
    """从 OSS 下载 zip 并解压"""
    # 下载到临时目录
    zip_path = os.path.join(tempfile.gettempdir(), f"{dataset_name}.zip")
    local_dir = os.path.join(DATA_DIR, dataset_name)
    
    print(f"下载: {dataset_name}.zip")
    result = subprocess.run(
        ["oss", "cp", oss_path, zip_path],
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        print(f"⚠️  下载失败或文件不存在: {oss_path}")
        return False
    
    print(f"✅ 下载成功: {zip_path}")
    
    # 解压
    print(f"正在解压到: {local_dir}")
    os.makedirs(local_dir, exist_ok=True)
    
    with zipfile.ZipFile(zip_path, 'r') as zipf:
        zipf.extractall(local_dir)
        print(f"✅ 解压完成: {len(zipf.namelist())} 个文件")
    
    # 删除临时 zip 文件
    os.remove(zip_path)
    print(f"✅ 清理临时文件")
    
    return True

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
    
    datasets_list = ['HDFS_data', 'BGL', 'Liberty', 'Thunderbird']
    
    for dataset_name in datasets_list:
        print(f"\n处理数据集: {dataset_name}")
        print("-" * 60)
        
        # 下载并解压 zip
        oss_path = f"{OSS_BUCKET}data/{dataset_name}.zip"
        download_and_extract(oss_path, dataset_name)
    
    print("\n" + "=" * 60)
    print("✅ 下载完成！")
    print("=" * 60)
    print(f"\n数据已保存到: {DATA_DIR}")
    print("\n检查文件:")
    for dataset_name in datasets_list:
        local_dir = os.path.join(DATA_DIR, dataset_name)
        if os.path.exists(local_dir):
            files = os.listdir(local_dir)
            print(f"  {dataset_name}: {len(files)} 个文件")
            for f in files[:5]:  # 显示前5个文件
                print(f"    - {f}")
            if len(files) > 5:
                print(f"    ... 还有 {len(files) - 5} 个文件")

if __name__ == '__main__':
    main()

