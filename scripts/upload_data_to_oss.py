#!/usr/bin/env python3
"""
将数据集上传到 OSS

使用方法:
python scripts/upload_data_to_oss.py
"""

import os
import subprocess
from pathlib import Path

# OSS 配置
OSS_BUCKET = "oss://my_models/"
DATA_DIR = "/hy-tmp/data"

def upload_to_oss(local_path, oss_path):
    """上传文件到 OSS"""
    print(f"上传: {local_path} -> {oss_path}")
    result = subprocess.run(
        ["oss", "cp", local_path, oss_path],
        capture_output=True,
        text=True
    )
    if result.returncode == 0:
        print(f"✅ 上传成功: {oss_path}")
        return True
    else:
        print(f"❌ 上传失败: {result.stderr}")
        return False

def main():
    print("=" * 60)
    print("上传数据集到 OSS")
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
    
    print(f"\n数据目录: {DATA_DIR}")
    print(f"OSS 路径: {OSS_BUCKET}data/\n")
    
    for dataset_name, config in datasets.items():
        local_dir = os.path.join(DATA_DIR, dataset_name)
        
        if not os.path.exists(local_dir):
            print(f"⚠️  跳过 {dataset_name}: 目录不存在")
            continue
        
        print(f"\n处理数据集: {dataset_name}")
        print("-" * 60)
        
        # 上传必需文件
        for filename in config['files']:
            local_path = os.path.join(local_dir, filename)
            if os.path.exists(local_path):
                oss_path = f"{OSS_BUCKET}data/{dataset_name}/{filename}"
                upload_to_oss(local_path, oss_path)
            else:
                print(f"⚠️  文件不存在: {local_path}")
        
        # 上传可选文件
        for filename in config.get('optional', []):
            local_path = os.path.join(local_dir, filename)
            if os.path.exists(local_path):
                oss_path = f"{OSS_BUCKET}data/{dataset_name}/{filename}"
                upload_to_oss(local_path, oss_path)
    
    print("\n" + "=" * 60)
    print("✅ 上传完成！")
    print("=" * 60)
    print(f"\n数据已保存到: {OSS_BUCKET}data/")
    print("\n恢复数据时运行:")
    print("  python scripts/download_data_from_oss.py")

if __name__ == '__main__':
    main()

