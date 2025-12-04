#!/usr/bin/env python3
"""
测试 HuggingFace 连接和认证状态

使用方法:
python test_huggingface.py
"""

import os
import sys

print("=" * 60)
print("测试 HuggingFace 连接")
print("=" * 60)

# 检查环境变量
print("\n1. 检查环境变量...")
hf_token = os.environ.get('HF_TOKEN') or os.environ.get('HUGGINGFACE_HUB_TOKEN')
if hf_token:
    print(f"✅ 找到 HF_TOKEN 环境变量 (长度: {len(hf_token)})")
else:
    print("⚠️  未找到 HF_TOKEN 环境变量")

# 检查 huggingface_hub
print("\n2. 检查 huggingface_hub 库...")
try:
    import huggingface_hub
    print(f"✅ huggingface_hub 已安装 (版本: {huggingface_hub.__version__})")
except ImportError:
    print("❌ huggingface_hub 未安装")
    print("   安装: pip3 install huggingface_hub")
    sys.exit(1)

# 测试连接
print("\n3. 测试网络连接...")
try:
    from huggingface_hub import HfApi
    api = HfApi()
    
    # 尝试获取数据集信息（不需要认证）
    print("   正在测试连接...")
    dataset_info = api.dataset_info("logfit-project/HDFS_v1")
    print(f"✅ 连接成功！")
    print(f"   数据集: {dataset_info.id}")
    
except Exception as e:
    print(f"❌ 连接失败: {e}")
    print("   可能原因:")
    print("   1. 网络连接问题")
    print("   2. 需要代理")
    print("   3. 防火墙阻止")

# 测试认证
print("\n4. 测试认证状态...")
try:
    from huggingface_hub import whoami
    
    try:
        user_info = whoami()
        print(f"✅ 已登录！")
        print(f"   用户名: {user_info.get('name', 'N/A')}")
        print(f"   邮箱: {user_info.get('email', 'N/A')}")
    except Exception as e:
        print("⚠️  未登录或 token 无效")
        print(f"   错误: {e}")
        print("\n   如何登录:")
        print("   1. 访问 https://huggingface.co/settings/tokens")
        print("   2. 创建 token (read 权限即可)")
        print("   3. 设置环境变量: export HF_TOKEN=your_token")
        print("   4. 或在代码中: from huggingface_hub import login; login()")
        
except ImportError:
    print("⚠️  无法检查认证状态")

# 测试 datasets 库
print("\n5. 检查 datasets 库...")
try:
    import datasets
    print(f"✅ datasets 已安装 (版本: {datasets.__version__})")
    
    # 尝试加载数据集（不下载，只检查）
    print("\n6. 测试数据集访问...")
    try:
        from datasets import get_dataset_config_names
        configs = get_dataset_config_names("logfit-project/HDFS_v1")
        print(f"✅ 可以访问数据集！")
        print(f"   配置: {configs}")
    except Exception as e:
        print(f"⚠️  访问数据集时出错: {e}")
        if "authentication" in str(e).lower() or "token" in str(e).lower():
            print("   这个数据集可能需要认证")
        else:
            print("   可能是网络问题")
            
except ImportError:
    print("❌ datasets 未安装")
    print("   安装: pip3 install datasets")

print("\n" + "=" * 60)
print("测试完成！")
print("=" * 60)
print("\n如果连接成功，可以运行:")
print("  python download_hdfs.py")

