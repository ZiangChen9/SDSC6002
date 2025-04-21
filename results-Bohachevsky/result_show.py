import os
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# ======================
# CONFIGURATION
# ======================
# Font settings (using Liberation Serif as Times New Roman alternative)
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Liberation Serif', 'Times']
plt.rcParams['mathtext.fontset'] = 'custom'
plt.rcParams['mathtext.rm'] = 'Liberation Serif'
plt.rcParams['mathtext.it'] = 'Liberation Serif:italic'
plt.rcParams['mathtext.bf'] = 'Liberation Serif:bold'

# Style settings
plt.rcParams['font.size'] = 12
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['axes.labelsize'] = 12
sns.set_style("whitegrid", {'axes.edgecolor': '0.2', 'grid.color': '0.85'})

# Output directory
output_dir = "plots"
os.makedirs(output_dir, exist_ok=True)  # Create folder if doesn't exist

# Input directory - 指定你的CSV文件所在的文件夹路径
input_dir = "raw_data"  # 修改为你想要的文件夹路径


# ======================
# PLOTTING FUNCTION
# ======================
def plot_csv_data(filename, data, rows_per_plot=5):
    """Generate and save plots for a CSV file"""
    base_name = os.path.splitext(os.path.basename(filename))[0]

    # Remove "result_reals_" prefix if present
    clean_name = base_name.replace("result_reals_", "")

    num_plots = (len(data) + rows_per_plot - 1) // rows_per_plot

    for i in range(num_plots):
        start_row = i * rows_per_plot
        end_row = min(start_row + rows_per_plot, len(data))

        fig, ax = plt.subplots(figsize=(12, 7), dpi=300)
        fig.set_facecolor('white')

        # Plot each line
        for idx, row in data.iloc[start_row:end_row].iterrows():
            ax.plot(row,
                    linestyle='-',
                    linewidth=1.8,
                    alpha=0.8,
                    marker='o',
                    markersize=5,
                    markevery=0.05,
                    label=f'Trial {idx + 1}')

        # Reference line and styling
        ax.axhline(y=0, color='red', linestyle='--', linewidth=2.2, label='Optimal Value')
        ax.set_title(f'{clean_name} (Trials {start_row + 1}-{end_row})', fontweight='bold')
        ax.set_xlabel('Number of Evaluations')
        ax.set_ylabel('Best Value Found')
        ax.legend(bbox_to_anchor=(1.02, 1), loc='upper left')
        ax.grid(True, linestyle=':', alpha=0.6)

        # Save the plot
        output_filename = f"{clean_name}_trials_{start_row + 1}_to_{end_row}.png"
        output_path = os.path.join(output_dir, output_filename)
        plt.tight_layout()
        plt.savefig(output_path, bbox_inches='tight', dpi=300)
        plt.close()

        print(f"Saved: {output_path}")


# ======================
# MAIN PROCESSING
# ======================
# Get all CSV files in the specified input directory
try:
    csv_files = [f for f in os.listdir(input_dir) if f.endswith('.csv')]

    if not csv_files:
        print(f"No CSV files found in directory: {input_dir}!")
    else:
        print(f"Found {len(csv_files)} CSV files to process in {input_dir}:")

        for csv_file in csv_files:
            try:
                print(f"\nProcessing: {csv_file}")
                file_path = os.path.join(input_dir, csv_file)
                df = pd.read_csv(file_path, header=None)
                plot_csv_data(csv_file, df)
            except Exception as e:
                print(f"Error processing {csv_file}: {str(e)}")

        print("\nAll processing completed! Plots saved in:", os.path.abspath(output_dir))
except FileNotFoundError:
    print(f"Input directory not found: {input_dir}")