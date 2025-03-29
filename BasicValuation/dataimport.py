# dataimport.py
# Created On: 2025-03-25
# Created By: Edward Cromwell
# A tool for importing financial data from files for the basic valuation project\

import pandas as pd
import numpy as np
import wx
from pathlib import Path
from typing import Dict

def load_file() -> Dict[str, np.ndarray]:
    app = wx.App(False)

    dialog = wx.FileDialog(
        None,
        "Select a File",
        wildcard="Excel Files (*.xlsx)|*.xlsx|CSV Files (*.csv)|*.csv",
        style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST
    )

    if dialog.ShowModal() == wx.ID_OK:
        file_name = dialog.GetPath()
    else:
        print("No file selected.")
        dialog.Destroy()
        app.Exit()
        return {}

    dialog.Destroy()
    app.Destroy()

    stmt_path: Path = Path(file_name)
    if stmt_path.suffix == '.csv':
        stmt_df: pd.DataFrame = pd.read_csv(stmt_path)
    elif stmt_path.suffix == '.xlsx':
        stmt_df: pd.DataFrame = pd.read_excel(stmt_path)
    else:
        raise ValueError(f"Unsupported file type: {stmt_path.suffix}. Please select a .csv or .xlsx file.")

    stmt: Dict[str, np.ndarray] = stmt_df.to_dict()
    stmt = {key: np.array(list(values.values())) for key, values in stmt.items()}

    return stmt