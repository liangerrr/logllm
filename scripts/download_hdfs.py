#!/usr/bin/env python3
"""
下载 HDFS_v1 数据集

使用方法:
python download_hdfs.py
"""

from datasets import load_dataset
import os

output_dir = "/Users/lc/PycharmProjects/HDFS_v1"

print("=" * 60)
print("正在下载 HDFS_v1 数据集...")
print("=" * 60)
print(f"保存位置: {output_dir}")
print("\n这可能需要几分钟，请耐心等待...\n")

try:
    # 尝试加载数据集（如果需要认证会自动提示）
    print("正在加载数据集...")
    print("提示: 如果需要 token，会在下载时提示输入")
    
    # 加载数据集
    ds = load_dataset("logfit-project/HDFS_v1")
    
    print(f"\n✅ 数据集加载成功！")
    print(f"数据集分割: {list(ds.keys())}")
    
    # 显示数据集信息
    for split_name in ds.keys():
        print(f"  {split_name}: {len(ds[split_name])} 条记录")
    
    # 保存到本地
    print(f"\n正在保存到本地: {output_dir}")
    print("这可能需要几分钟...")
    ds.save_to_disk(output_dir)
    
    print(f"\n✅ 完成！数据集已保存到: {output_dir}")
    print("\n下一步: 运行数据转换脚本")
    print("  python convert_hdfs.py")
    
except Exception as e:
    print(f"\n❌ 错误: {e}")
    if "authentication" in str(e).lower() or "token" in str(e).lower():
        print("\n需要 HuggingFace token，请:")
        print("1. 访问 https://huggingface.co/settings/tokens")
        print("2. 创建 token")
        print("3. 设置环境变量: export HF_TOKEN=your_token")
        print("   然后重新运行此脚本")
    elif "not found" in str(e).lower():
        print("\n请检查:")
        print("1. 网络连接是否正常")
        print("2. 数据集名称是否正确: logfit-project/HDFS_v1")

