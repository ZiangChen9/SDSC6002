import csv
import os

if __name__ == "__main__":
    # Get the absolute path of the current script's directory
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct the path to your data folder
    data_folder = os.path.join(script_dir, "processed_data")

    # Single output file for all tables
    output_filename = os.path.join(script_dir, "combined_tables.txt")

    # Define the row names
    row_names = ["Mean", "S.D.", "95\\% CI LB", "95\\% CI UB"]

    with open(output_filename, "w", encoding="utf-8") as output_file:
        for filename in os.listdir(data_folder):
            if not filename.endswith(".csv"):
                continue

            filepath = os.path.join(data_folder, filename)

            # Extract table name (between first and last underscore)
            parts = filename.split("_")
            if len(parts) > 2:
                table_name = "_".join(
                    parts[1:-1]
                )  # Join all parts between first and last
            else:
                table_name = filename.replace(".csv", "")

            with open(filepath, "r", newline="") as csvfile:
                reader = csv.reader(csvfile)
                rows = list(reader)
                last_four_rows = rows[-4:]
                results = []
                for row in last_four_rows:
                    row_len = len(row)
                    indices = [
                        # Skip 0% (index 0)
                        max(0, (row_len - 1) // 4),  # 25%
                        max(0, (row_len - 1) // 2),  # 50%
                        max(0, 3 * (row_len - 1) // 4),  # 75%
                        row_len - 1,  # 100%
                    ]
                    selected_columns = [row[i] if i < row_len else "" for i in indices]
                    results.append(selected_columns)

                # Start building LaTeX table
                latex_table = "\\begin{table*}[htbp]\n"  # table* for two-column span
                latex_table += "\\centering\n"
                name = table_name.replace("_", " ")
                name = name.replace("reals", "")
                latex_table += f"\\caption{{Performance Metrics for {name}}}\n"
                latex_table += f"\\label{{tab:{name.lower()}}}\n"
                latex_table += "\\begin{tabular}{lcccc}\n"  # One less column now
                latex_table += "\\hline\n"
                latex_table += "Metric & 25\\% & 50\\% & 75\\% & 100\\% \\\\\n"
                latex_table += "\\hline\n"

                # Add rows with their names
                for name, row in zip(row_names, results):
                    escaped_row = [
                        str(item).replace("_", "\\_").replace("%", "\\%")
                        for item in row
                    ]
                    latex_table += f"{name} & {' & '.join(escaped_row)} \\\\\n"

                latex_table += "\\hline\n"
                latex_table += "\\end{tabular}\n"
                latex_table += "\\end{table*}\n\n"  # Extra newline between tables

                output_file.write(latex_table)
                print(f"Added table for: {table_name}")

    print(f"\nAll tables have been saved to: {output_filename}")
