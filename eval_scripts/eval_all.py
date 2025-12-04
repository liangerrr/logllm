"""
评估所有数据集
一次性运行所有数据集的评估
"""

import os
import re
import sys
from pathlib import Path
import numpy as np
import torch
from torch.utils.data import DataLoader
from tqdm import tqdm
import pandas as pd

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from model import LogLLM
from customDataset import CustomDataset, CustomCollator
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# 配置
max_content_len = 100
max_seq_len = 128
batch_size = 32

Bert_path = r"/hy-tmp/model_weights/AI-ModelScope/bert-base-uncased"
Llama_path = r"/hy-tmp/model_weights/LLM-Research/Meta-Llama-3-8B"
ROOT_DIR = Path(__file__).parent.parent
device = torch.device("cuda:0")

def evalModel(model, dataloader, dataset_name):
    """评估函数"""
    model.eval()
    preds = []

    with torch.no_grad():
        for bathc_i in tqdm(dataloader, desc=f"推理 {dataset_name}"):
            inputs = bathc_i['inputs']
            seq_positions = bathc_i['seq_positions']
            inputs = inputs.to(device)
            outputs_ids = model(inputs, seq_positions)
            outputs = model.Llama_tokenizer.batch_decode(outputs_ids)

            for text in outputs:
                match = re.search(r'normal|anomalous', text, re.IGNORECASE)
                if match:
                    preds.append(match.group())
                else:
                    preds.append('')

    preds_copy = np.array(preds)
    preds = np.zeros_like(preds_copy, dtype=int)
    preds[preds_copy == 'anomalous'] = 1
    preds[preds_copy != 'anomalous'] = 0
    gt = dataloader.dataset.get_label()

    precision = precision_score(gt, preds, average="binary", pos_label=1)
    recall = recall_score(gt, preds, average="binary", pos_label=1)
    f = f1_score(gt, preds, average="binary", pos_label=1)
    acc = accuracy_score(gt, preds)

    num_anomalous = (gt == 1).sum()
    num_normal = (gt == 0).sum()

    print(f'\n{"="*60}')
    print(f'数据集: {dataset_name}')
    print(f'{"="*60}')
    print(f'Number of anomalous seqs: {num_anomalous}; number of normal seqs: {num_normal}')

    pred_num_anomalous = (preds == 1).sum()
    pred_num_normal = (preds == 0).sum()

    print(f'Number of detected anomalous seqs: {pred_num_anomalous}; number of detected normal seqs: {pred_num_normal}')

    print(f'\n结果:')
    print(f'  Precision: {precision:.4f}')
    print(f'  Recall:    {recall:.4f}')
    print(f'  F1 Score:  {f:.4f}')
    print(f'  Accuracy:  {acc:.4f}')
    print(f'{"="*60}\n')
    
    return {
        'dataset': dataset_name,
        'precision': precision,
        'recall': recall,
        'f1': f,
        'accuracy': acc
    }

def run_eval(dataset_name, ft_model_name):
    """运行单个数据集的评估"""
    print(f"\n{'='*80}")
    print(f"开始评估: {dataset_name}")
    print(f"{'='*80}\n")
    
    # 数据路径映射
    data_paths = {
        'HDFS_v1': '/hy-tmp/data/HDFS_data/test.csv',
        'BGL': '/hy-tmp/data/BGL/test.csv',
        'Liberty': '/hy-tmp/data/Liberty/test.csv',
        'Thunderbird': '/hy-tmp/data/Thunderbird/test.csv'
    }
    data_path = data_paths.get(dataset_name, f'/hy-tmp/data/{dataset_name}/test.csv')
    ft_path = os.path.join(ROOT_DIR, f"ft_model_{ft_model_name}")
    
    try:
        dataset = CustomDataset(data_path)
        model = LogLLM(Bert_path, Llama_path, ft_path=ft_path, is_train_mode=False, 
                      device=device, max_content_len=max_content_len, max_seq_len=max_seq_len)
        
        tokenizer = model.Bert_tokenizer
        collator = CustomCollator(tokenizer, max_seq_len=max_seq_len, max_content_len=max_content_len)
        dataloader = DataLoader(
            dataset,
            batch_size=batch_size,
            collate_fn=collator,
            num_workers=4,
            shuffle=False,
            drop_last=False
        )
        
        result = evalModel(model, dataloader, dataset_name)
        return result
        
    except Exception as e:
        print(f"❌ 评估 {dataset_name} 时出错: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == '__main__':
    print("=" * 80)
    print("LogLLM 全数据集评估")
    print("=" * 80)
    
    results = []
    
    # 评估所有数据集
    datasets = [
        ('HDFS_v1', 'HDFS'),
        ('BGL', 'BGL'),
        ('Liberty', 'Liberty'),
        ('Thunderbird', 'Thunderbird')
    ]
    
    for dataset_name, ft_model_name in datasets:
        result = run_eval(dataset_name, ft_model_name)
        if result:
            result['dataset'] = dataset_name
            results.append(result)
    
    # 打印汇总结果
    print("\n" + "=" * 80)
    print("汇总结果")
    print("=" * 80)
    
    if results:
        df = pd.DataFrame(results)
        df = df[['dataset', 'precision', 'recall', 'f1', 'accuracy']]
        print("\n", df.to_string(index=False))
        
        # 计算平均 F1
        avg_f1 = df['f1'].mean()
        print(f"\n平均 F1 Score: {avg_f1:.4f}")
    else:
        print("❌ 没有成功评估的数据集")
    
    print("=" * 80)

