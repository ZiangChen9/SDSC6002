import os
import pandas as pd
import numpy as np
from scipy import stats


def process_csv(input_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    for filename in os.listdir(input_dir):
        if not filename.endswith(".csv"):
            continue

        filepath = os.path.join(input_dir, filename)
        filename_without_ext = os.path.splitext(filename)[0]
        df = pd.read_csv(filepath, header=None)
        new_df = pd.DataFrame()
        for col in df.columns:
            column_data = df[col].copy()

            if pd.api.types.is_numeric_dtype(column_data):
                mean_value = column_data.mean()
                std_dev = column_data.std()
                n = len(column_data)
                se = std_dev / np.sqrt(n)
                t_critical = stats.t.ppf(0.975, n - 1)
                lower_bound = mean_value - t_critical * se
                upper_bound = mean_value + t_critical * se
                column_data.loc[len(column_data)] = mean_value
                column_data.loc[len(column_data)] = std_dev
                column_data.loc[len(column_data)] = lower_bound
                column_data.loc[len(column_data)] = upper_bound
            new_df[col] = column_data
        output_path = os.path.join(output_dir, f"{filename_without_ext}_processed.csv")

        try:
            new_df.to_csv(output_path, index=False, header=False)
            print(f"处理后的 {filename_without_ext} 已保存到 {output_path}")
        except Exception as e:
            print(f"保存文件 {output_path} 时出错：{e}")


input_directory = "/home/ziangchen9/home/ziangchen9/home/ziangchen9/yao-SDSC6002/Experiments/TS/raw_data"
output_directory = "/home/ziangchen9/home/ziangchen9/home/ziangchen9/yao-SDSC6002/Experiments/TS/processed_data"

process_csv(input_directory, output_directory)
