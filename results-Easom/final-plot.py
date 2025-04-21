import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from matplotlib.ticker import MaxNLocator
from collections import defaultdict
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from matplotlib.ticker import MaxNLocator
from collections import defaultdict

# ======================
# CONFIGURATION
# ======================
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Liberation Serif', 'Times New Roman', 'Times']
plt.rcParams['mathtext.fontset'] = 'custom'
plt.rcParams['mathtext.rm'] = 'Liberation Serif'
plt.rcParams['mathtext.it'] = 'Liberation Serif:italic'
plt.rcParams['mathtext.bf'] = 'Liberation Serif:bold'

plt.rcParams['font.size'] = 12
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['legend.fontsize'] = 11
plt.rcParams['xtick.labelsize'] = 11
plt.rcParams['ytick.labelsize'] = 11

# Enhanced color palette
PALETTE = [
    '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
    '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf',
    '#aec7e8', '#ffbb78', '#98df8a', '#ff9896', '#c5b0d5'
]

LINE_STYLES = ['-', '--', '-.', ':']
MARKERS = ['o', 's', 'D', '^', 'v', '<', '>', 'p', '*', 'h', 'H', '+', 'x', 'X', 'd']

sns.set_style("whitegrid", {
    'axes.edgecolor': '0.3',
    'grid.color': '#f0f0f0',
    'axes.grid': True,
    'axes.axisbelow': True
})

input_dir = "final"
output_dir = "statistic_show"
os.makedirs(output_dir, exist_ok=True)
os.makedirs(input_dir, exist_ok=True)

# ======================
# UTILITY FUNCTIONS
# ======================
def clean_algorithm_name(filename):
    """Clean algorithm name from filename"""
    name = os.path.splitext(filename)[0]
    return name.replace("result_reals_", "").replace("_processed", "")

# ======================
# PLOTTING FUNCTION
# ======================
def plot_all_data(all_files_data, color_palette):
    """Plot all algorithms in a single plot with refined styling"""
    fig, ax = plt.subplots(figsize=(14, 8), dpi=300)
    fig.set_facecolor('white')

    # Ensure all files have at least 81 columns
    min_columns = 81
    x_values = np.arange(min_columns)
    sample_freq = max(1, len(x_values) // 15)  # Show ~15 error bars per line

    num_algorithms = len(all_files_data)
    # Stagger control
    base_stagger = 0.0  # Moderate stagger
    stagger_factor = base_stagger / max(1, num_algorithms - 1)

    for idx, (filename, data) in enumerate(all_files_data.items()):
        # Truncate data to the first 81 columns
        if len(data.columns) >= min_columns:
            truncated_data = data.iloc[:, :min_columns]
        else:
            print(f"Warning: File {filename} has fewer than {min_columns} columns. Skipping.")
            continue

        # Calculate statistics
        mean_values = truncated_data.mean(axis=0)
        std_dev = truncated_data.std(axis=0)
        n = len(truncated_data)
        se = std_dev / np.sqrt(n)
        t_critical = stats.t.ppf(0.975, n - 1)
        ci_width = t_critical * se

        # Calculate staggered x positions
        offset = (idx - (num_algorithms - 1) / 2) * stagger_factor
        staggered_x = x_values + offset

        # Get visual properties
        color = color_palette[idx % len(color_palette)]
        line_style = LINE_STYLES[(idx // len(color_palette)) % len(LINE_STYLES)]
        marker = MARKERS[idx % len(MARKERS)] if num_algorithms <= 6 else None
        algorithm_name = clean_algorithm_name(filename)

        # Plot main line
        ax.plot(staggered_x, mean_values,
                color=color,
                linestyle=line_style,
                linewidth=1.8,
                marker=marker,
                markersize=5,
                markeredgecolor=color,
                markerfacecolor='white',
                markevery=sample_freq,
                label=algorithm_name,
                zorder=4)

        # Add error bars
        ax.errorbar(staggered_x[::sample_freq],
                    mean_values[::sample_freq],
                    yerr=ci_width[::sample_freq],
                    fmt='none',
                    ecolor=color,
                    elinewidth=0.8,
                    capsize=3,
                    capthick=0.8,
                    alpha=0.8,
                    zorder=3)

    # Reference line
    ax.axhline(y=0, color='black', linestyle='--', linewidth=1.2, alpha=0.6, zorder=5)

    # Styling
    ax.set_title(f"Performance Comparison: Easom", fontweight='bold', pad=15)
    ax.set_xlabel('Number of Evaluations', labelpad=10)
    ax.set_ylabel('Best Value Found', labelpad=10)
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    ax.yaxis.set_major_locator(MaxNLocator(10))
    ax.set_xlim(x_values[0] - 0.5, x_values[-1] + 0.5)

    # Grid and borders
    ax.grid(True, linestyle=':', linewidth=0.5, alpha=0.6)
    for spine in ax.spines.values():
        spine.set_edgecolor('0.3')
        spine.set_linewidth(0.8)

    # Legend
    legend = ax.legend(loc='best', framealpha=0.95,
                       edgecolor='0.9', facecolor='white')
    legend.get_frame().set_linewidth(0.7)

    # Save
    output_filename = "all_algorithms.png"
    output_path = os.path.join(output_dir, output_filename)
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved plot: {output_path}")

# ======================
# MAIN PROCESSING
# ======================
def main():
    csv_files = sorted([f for f in os.listdir(input_dir) if f.endswith('.csv')])

    if not csv_files:
        print(f"No CSV files found in directory: {input_dir}")
        return

    print(f"Found {len(csv_files)} CSV files to process")

    # Read all files and prepare data for plotting
    all_files_data = {}

    for filename in csv_files:
        try:
            filepath = os.path.join(input_dir, filename)
            data = pd.read_csv(filepath, header=None)
            # Check if the file has at least 81 columns
            if len(data.columns) >= 81:
                all_files_data[filename] = data
            else:
                print(f"Warning: File {filename} has fewer than 81 columns. Skipping.")
        except Exception as e:
            print(f"Error processing {filename}: {str(e)}")
            continue

    # Plot all data in a single plot
    if all_files_data:
        plot_all_data(all_files_data, PALETTE)
    else:
        print("No valid files with at least 81 columns found.")

    print(f"\nProcessing complete! Results saved to: {os.path.abspath(output_dir)}")

if __name__ == "__main__":
    main()