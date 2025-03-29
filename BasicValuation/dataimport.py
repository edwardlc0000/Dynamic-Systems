# dataimport.py
# Created On: 2025-03-25
# Created By: Edward Cromwell
# A tool for importing financial data from files for the basic valuation project\

import pandas as pd
import numpy as np
from tkinter import filedialog as fd
from pathlib import Path
from typing import Tuple, Dict

def load_is():
    file_types: Tuple[str] = (
        ('Excel Files', '.xlsx'),
        ('Delimited Files', '.csv')
    )

    is_name: str = fd.askopenfilename(
        title='Select the Income Statement',
        filetypes=file_types
    )

    is_path: Path = Path(is_name)

    if is_path.suffix == '.csv':
        is_df: pd.DataFrame = pd.read_csv(is_path)
    elif is_path.suffix == '.xlsx':
        is_df: pd.DataFrame = pd.read_excel(is_path)
    else:
        raise ValueError(f"Unsupported file type: {is_path.suffix()}. Please select a .csv or .xlsx file.")
    
    is_dict: Dict[str, np.ndarray] = is_df.to_dict()
    is_dict = {key: np.array(list(values.values())) for key, values in is_dict.items()}

    return is_dict

def load_bs():
    file_types: Tuple[str] = (
        ('Excel Files', '.xlsx'),
        ('Delimited Files', '.csv')
    )

    scf_name: str = fd.askopenfilename(
        title='Select the Balance Sheet',
        filetypes=file_types
    )

    scf_path: Path = Path(scf_name)

    if scf_path.suffix == '.csv':
        scf_df: pd.DataFrame = pd.read_csv(scf_path)
    elif scf_path.suffix == '.xlsx':
        scf_df: pd.DataFrame = pd.read_excel(scf_path)
    else:
        raise ValueError(f"Unsupported file type: {scf_path.suffix()}. Please select a .csv or .xlsx file.")
    
    scf_dict: Dict[str, np.ndarray] = scf_df.to_dict()
    scf_dict = {key: np.array(list(values.values())) for key, values in scf_dict.items()}

    return scf_dict

def load_scf():
    file_types: Tuple[str] = (
        ('Excel Files', '.xlsx'),
        ('Delimited Files', '.csv')
    )

    scf_name: str = fd.askopenfilename(
        title='Select the Statment of Cash Flows',
        filetypes=file_types
    )

    scf_path: Path = Path(scf_name)

    if scf_path.suffix == '.csv':
        scf_df: pd.DataFrame = pd.read_csv(scf_path)
    elif scf_path.suffix == '.xlsx':
        scf_df: pd.DataFrame = pd.read_excel(scf_path)
    else:
        raise ValueError(f"Unsupported file type: {scf_path.suffix()}. Please select a .csv or .xlsx file.")
    
    scf_dict: Dict[str, np.ndarray] = scf_df.to_dict()
    scf_dict = {key: np.array(list(values.values())) for key, values in scf_dict.items()}

    return scf_dict
