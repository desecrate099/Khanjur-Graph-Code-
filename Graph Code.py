import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# ----------------------------- USER SETTINGS -----------------------------
file_path = Path(r"C:\Users\sprid\Downloads\TiNiCu_700_15min_acid6+CuAPS.csv")

start = 34          # Row number where the header row is (1-based)
end = None          # Set to a number OR None to read to the bottom

# For Excel only (ADD or REMOVE SHEETS HERE).
# If empty or None, the code will plot ALL sheets in the workbook.
sheet_colors = {
    # "Sheet1": "red",
    # "Sheet2": "blue",
}

x_axis = "Angle"    # column name for X-axis
y_axis = "ESD"      # column name for Y-axis

# Optional display labels (set to None to use column names)
x_label = None
y_label = None

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
if skip < 0:
    raise ValueError("'start' must be >= 1")

if end is not None:
    if end < start:
        raise ValueError(f"'end' ({end}) must be >= 'start' ({start}).")
    rows = end - start + 1
else:
    rows = None

x_label_to_use = x_label if x_label is not None else x_axis
y_label_to_use = y_label if y_label is not None else y_axis

plt.figure()

def plot_df(df, label, color=None):
    df.columns = [str(c).strip() for c in df.columns]

    # Column checks
    for col in (x_axis, y_axis):
        if col not in df.columns:
            raise KeyError(
                f"Column '{col}' not found in '{label}'. "
                f"Available columns: {list(df.columns)}"
            )

    plt.scatter(
        df[x_axis],
        df[y_axis],
        label=label,
        color=color,
        s=15,
        alpha=0.8
    )

if ext == ".csv":
    df = pd.read_csv(
        file_path,
        skiprows=skip,
        nrows=rows,
        header=0,
        skipinitialspace=True,
        on_bad_lines="skip"
    )
    plot_df(df, label=file_path.stem, color=None)

elif ext in [".xls", ".xlsx"]:
    engine = "xlrd" if ext == ".xls" else "openpyxl"

    if sheet_colors:
        sheets_to_plot = list(sheet_colors.items())  
    else:
        xl = pd.ExcelFile(file_path, engine=engine)
        sheets_to_plot = [(name, None) for name in xl.sheet_names]

    for sheet_name, color in sheets_to_plot:
        df = pd.read_excel(
            file_path,
            sheet_name=sheet_name,
            skiprows=skip,
            nrows=rows,
            header=0,
            engine=engine
        )
        plot_df(df, label=sheet_name, color=color)

else:
    raise ValueError(f"Unsupported file type: {ext}. Use .csv, .xls, or .xlsx")

row_range = f"{start}–{end}" if end is not None else f"{start}–end"

plt.xlabel(x_label_to_use, fontsize=label_fontsize)
plt.ylabel(y_label_to_use, fontsize=label_fontsize)

plt.title(
    f"{y_label_to_use} vs {x_label_to_use} (rows {row_range})",
    fontsize=title_fontsize
)

plt.xticks(fontsize=tick_fontsize)
plt.yticks(fontsize=tick_fontsize)

plt.legend(fontsize=legend_fontsize)
plt.grid(True)
plt.tight_layout()
plt.show()
