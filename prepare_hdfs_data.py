"""
HDFS 数据预处理脚本
在服务器上运行，生成 train.csv 和 test.csv

使用方法:
python prepare_hdfs_data.py
"""

import os
import sys
from pathlib import Path

# 添加 prepareData 目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from prepareData.session_window import *

if __name__ == '__main__':
    print("=" * 60)
    print("HDFS 数据预处理")
    print("=" * 60)
    print(f"\n数据目录: {data_dir}")
    print(f"日志文件: {log_name}")
    print(f"输出目录: {output_dir}")
    
    # 检查必要文件
    log_file = os.path.join(data_dir, log_name)
    label_file = os.path.join(data_dir, "anomaly_label.csv")
    
    print(f"\n检查必要文件...")
    if not os.path.exists(log_file):
        print(f"❌ 错误: 日志文件不存在: {log_file}")
        print(f"请确保 HDFS.log 文件在 {data_dir} 目录下")
        sys.exit(1)
    else:
        print(f"✅ 找到日志文件: {log_file}")
    
    if not os.path.exists(label_file):
        print(f"❌ 错误: 标签文件不存在: {label_file}")
        print(f"请确保 anomaly_label.csv 文件在 {data_dir} 目录下")
        sys.exit(1)
    else:
        print(f"✅ 找到标签文件: {label_file}")
    
    print(f"\n开始预处理...")
    print("这可能需要一些时间，请耐心等待...\n")
    
    # 运行预处理（session_window.py 的 main 逻辑）
    # 这里直接执行 session_window.py 的逻辑
    exec(open('prepareData/session_window.py').read())

