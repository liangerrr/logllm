#!/usr/bin/env python3
"""
将数据集上传到 OSS（打包成 zip）

使用方法:
python scripts/upload_data_to_oss.py
"""

import os
import subprocess
import zipfile
import tempfile
from pathlib import Path

# OSS 配置
OSS_BUCKET = "oss://my_models/"
DATA_DIR = "/hy-tmp/data"

def create_zip(dataset_dir, dataset_name):
    """创建数据集的 zip 文件"""
    zip_path = os.path.join(tempfile.gettempdir(), f"{dataset_name}.zip")
    
    print(f"正在打包: {dataset_name}...")
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(dataset_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, dataset_dir)
                zipf.write(file_path, arcname)
                print(f"  添加: {arcname}")
    
    file_size_mb = os.path.getsize(zip_path) / (1024 * 1024)
    print(f"✅ 打包完成: {zip_path} ({file_size_mb:.2f} MB)")
    return zip_path

def upload_to_oss(local_path, oss_path):
    """上传文件到 OSS"""
    print(f"上传: {os.path.basename(local_path)} -> {oss_path}")
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
        
        # 检查是否有文件
        files_exist = False
        for filename in config['files']:
            if os.path.exists(os.path.join(local_dir, filename)):
                files_exist = True
                break
        
        if not files_exist:
            print(f"⚠️  跳过 {dataset_name}: 没有找到必需文件")
            continue
        
        # 打包成 zip
        zip_path = create_zip(local_dir, dataset_name)
        
        # 上传 zip 文件
        oss_path = f"{OSS_BUCKET}data/{dataset_name}.zip"
        if upload_to_oss(zip_path, oss_path):
            # 上传成功后删除临时 zip 文件
            os.remove(zip_path)
            print(f"✅ {dataset_name} 上传完成并清理临时文件")
    
    print("\n" + "=" * 60)
    print("✅ 上传完成！")
    print("=" * 60)
    print(f"\n数据已保存到: {OSS_BUCKET}data/")
    print("\n恢复数据时运行:")
    print("  python scripts/download_data_from_oss.py")

if __name__ == '__main__':
    main()

