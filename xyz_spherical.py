# Script written by Youssef El Gharably, September 13th 2024 for Honors Thesis with Professor Ken Krebs.

import os
import numpy as np
import pandas as pd

def build_dataframe(file_path):
    col_names = ['Atom', 'x', 'y', 'z']  # Replace with actual column names
    try:
        return pd.read_csv(file_path, sep='\s+', skiprows=0, names=col_names)
    except (FileNotFoundError, pd.errors.EmptyDataError, pd.errors.ParserError) as e:
        print(f"Error reading the file at {file_path}: {e}")
        return None
    
def xyz_to_spherical(x, y, z):
    r = np.sqrt(x**2 + y**2 + z**2)
    theta = np.arccos(z / r)
    phi = np.arctan2(y, x)
    
    return r, theta, phi

def df_to_latex(df, caption="Insert Caption Here", label="tab:results"):
    df = df.round(2)
    
    table_code = "\\begin{table}[H]\n"
    table_code += "    \\centering\n"
    table_code += f"    \\caption{{{caption}}}\n"
    table_code += "    \\vspace{9pt}\n"
    table_code += f"    \\begin{{tabularx}}{{\\textwidth}}{{{'X' * len(df.columns)}}}\n"
    table_code += "        \\toprule\n"
    table_code += "        \\hline\n"
    table_code += "        \\addlinespace[0.5ex]\n"

    # Headers
    table_code += "        " + " & ".join(df.columns) + " \\\\\n"
    table_code += "        \\midrule\n"

    # Data Rows
    for i, row in df.iterrows():
        row_data = " & ".join(str(val) for val in row)
        table_code += "        " + row_data + " \\\\\n"
    
    table_code += "        \\bottomrule\n"
    table_code += "    \\end{tabularx}\n"
    table_code += f"    \\label{{{label}}}\n"
    table_code += "\\end{table}"

    return table_code

def df_to_txt(df, file_path):
    try:
        df.to_csv(file_path, sep=' ', index=False, header=True)
        print(f"DataFrame successfully written to {file_path}")
    except Exception as e:
        print(f"Error writing DataFrame to file: {e}")

def main():
    file = r"D:\Undergraduate Life\Honors\LiYF4_Pr_Harry_result.xyz"
    df = build_dataframe(file)

    center_atom = 'Pr'
    center_df = df[df['Atom'] == center_atom]

    center_x = float(center_df['x'])
    center_y = float(center_df['y'])
    center_z = float(center_df['z'])

    atom_np = df['Atom'].to_numpy()
    origin_x = df['x'].to_numpy() - center_x
    origin_y = df['y'].to_numpy() - center_y
    origin_z = df['z'].to_numpy() - center_z

    r, theta, phi = xyz_to_spherical(origin_x,origin_y,origin_z)

    theta_deg = np.degrees(theta)
    phi_deg = np.degrees(phi)

    # Correcting the (0,0,0):
    r[0] = 0
    theta_deg[0] = 0
    phi_deg[0] = 0

    df_new = pd.DataFrame({
        'Atom': atom_np,
        'R': r,
        'Theta': theta_deg,
        'Phi': phi_deg
    })

    df_to_txt(df_new,r"D:\Undergraduate Life\Honors\LiYF4_Pr_Harry_result_spherical.txt")

if __name__ == "__main__":
    main()