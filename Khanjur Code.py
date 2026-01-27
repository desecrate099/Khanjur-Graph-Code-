import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Go to the file, right-click it, choose "Copy as path", then paste it here after the r
file_path = Path(r"C:\Users\sprid\Downloads\SMAstrain.xls")

# ----------------------------- USER SETTINGS -----------------------------
start = 10          # Row where the header row
end = None          # Set to a number OR None to read to the bottom

# Sheet name → color mapping (ADD or REMOVE SHEETS HERE)
sheet_colors = {
    "300um samle": "red",     # Chang this to the exact Excel sheet name
    "100um sample": "blue",
}

x_axis = "Time sec"     # column name for X-axis (from file)
y_axis = "LOAD N"       # column name for Y-axis (from file)

# Optional display labels (set to None to use column names)
x_label = "Time (seconds)"
y_label = "Load (Newtons)"

label_fontsize = 20  # Size for x and y axis labels
title_fontsize = 20  # Size for the plot title
tick_fontsize  = 10  # Size for the tick numbers on axes
legend_fontsize = 12 # Size for legend text
# ------------------------------------------------------------------------

# ------------------------- DO NOT TOUCH BELOW ---------------------------
if not file_path.exists():
    raise FileNotFoundError(f"File not found: {file_path}")

ext = file_path.suffix.lower()

skip = start - 1

if end is not None:
    if end < start:
        raise ValueError(f"'end' ({end}) must be >= 'start' ({start}).")
    rows = end - start + 1
else:
    rows = None

x_label_to_use = x_label if x_label is not None else x_axis
y_label_to_use = y_label if y_label is not None else y_axis

plt.figure()

for sheet_name, color in sheet_colors.items():

    if ext == ".csv":
        raise ValueError("Multiple sheets only work with Excel (.xls/.xlsx) files.")

    elif ext in [".xls", ".xlsx"]:
        engine = "xlrd" if ext == ".xls" else "openpyxl"
        df = pd.read_excel(
            file_path,
            sheet_name=sheet_name,
            skiprows=skip,
            nrows=rows,
            header=0,
            engine=engine
        )
    else:
        raise ValueError(f"Unsupported file type: {ext}. Use .csv, .xls, or .xlsx")

    # Basic column checks
    for col in (x_axis, y_axis):
        if col not in df.columns:
            raise KeyError(
                f"Column '{col}' not found in sheet '{sheet_name}'. "
                f"Available columns: {list(df.columns)}"
            )

    # Plot each sheet with chosen color
    plt.scatter(
        df[x_axis],
        df[y_axis],
        label=sheet_name,   # Legend entry
        color=color,        # YOUR COLOR HERE
        s=15,
        alpha=0.8
    )

row_range = f"{start}–{end}" if end is not None else f"{start}–end"
sheet_list = ", ".join(sheet_colors.keys())

plt.xlabel(x_label_to_use, fontsize=label_fontsize)
plt.ylabel(y_label_to_use, fontsize=label_fontsize)

plt.title(
    f"{y_label_to_use} vs {x_label_to_use} "
    f"(Sheets: {sheet_list}, rows {row_range})",
    fontsize=title_fontsize
)

plt.xticks(fontsize=tick_fontsize)
plt.yticks(fontsize=tick_fontsize)

plt.legend(fontsize=legend_fontsize)
plt.grid(True)
plt.tight_layout()
plt.show()
