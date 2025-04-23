import os
import pandas as pd
import numpy as np
from scipy import stats

# 输入输出路径配置
input_dir = "compare"
output_dir = os.path.join(input_dir, "processed_data")
os.makedirs(output_dir, exist_ok=True)

for filename in os.listdir(input_dir):
    if not filename.endswith(".csv"):
        continue

    try:
        # 构建完整文件路径
        filepath = os.path.join(input_dir, filename)

        # 读取CSV文件
        df = pd.read_csv(filepath, header=None)
        new_df = pd.DataFrame()

        # 处理每一列数据
        for col in df.columns:
            column_data = df[col].copy()

            if pd.api.types.is_numeric_dtype(column_data):
                # 计算统计指标
                mean_val = column_data.mean()
                std_dev = column_data.std()
                n = len(column_data)
                se = std_dev / np.sqrt(n)
                t_critical = stats.t.ppf(0.975, df=n - 1)

                # 追加统计结果
                column_data.loc[len(column_data)] = mean_val
                column_data.loc[len(column_data)] = std_dev
                column_data.loc[len(column_data)] = (
                    mean_val - t_critical * se
                )  # 置信下限
                column_data.loc[len(column_data)] = (
                    mean_val + t_critical * se
                )  # 置信上限

            new_df[col] = column_data

        # 保存处理结果
        output_filename = f"processed_{filename}"
        output_path = os.path.join(output_dir, output_filename)
        new_df.to_csv(output_path, index=False, header=False)
        print(f"[Success] 文件 {filename} 已处理 → 保存为 {output_path}")

    except pd.errors.EmptyDataError:
        print(f"[Warning] 文件 {filename} 为空文件，跳过处理")
    except Exception as e:
        print(f"[Error] 处理 {filename} 时发生错误: {str(e)}")
