"""
This module provides functionality for processing and manipulating MATLAB scripts.
"""

import re
import matlab.engine
from typing import List, Dict, Any
import scipy.io
import h5py

def parse_matlab_script(file_path: str) -> Dict[str, Any]:
    """
    Parse a MATLAB script and extract various elements.

    Args:
        file_path (str): The path to the MATLAB script file.

    Returns:
        Dict[str, Any]: A dictionary containing extracted information, including:
            - functions: List of dictionaries with function names and their arguments.
            - variables: List of global variables found in the script.
            - comments: List of comments found in the script.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Extract functions
    function_pattern = re.compile(r'function\s+(?:\[?([^\]]+)\]?\s*=\s*)?(\w+)\s*\(([^)]*)\)', re.MULTILINE)
    functions = [
        {
            "name": match.group(2),
            "outputs": [out.strip() for out in (match.group(1) or "").split(',') if out.strip()],
            "inputs": [inp.strip() for inp in match.group(3).split(',') if inp.strip()]
        }
        for match in function_pattern.finditer(content)
    ]

    # Extract global variables
    global_var_pattern = re.compile(r'^\s*global\s+(.+)$', re.MULTILINE)
    variables = [var.strip() for match in global_var_pattern.finditer(content) for var in match.group(1).split(',')]

    # Extract comments
    comment_pattern = re.compile(r'(%.*$)|(^\s*%.*$)', re.MULTILINE)
    comments = [match.group().strip() for match in comment_pattern.finditer(content)]

    return {
        "functions": functions,
        "variables": variables,
        "comments": comments
    }

def generate_matlab_script(script_content: List[str]) -> str:
    """
    Generate a MATLAB script from a list of script lines.

    Args:
        script_content (List[str]): A list of strings representing MATLAB script lines.

    Returns:
        str: A string containing the generated MATLAB script.
    """
    return "\n".join(script_content)

def execute_matlab_script(script_path: str, matlab_engine) -> Any:
    """
    Execute a MATLAB script using a MATLAB engine.

    Note: This function requires a MATLAB engine to be set up and passed as an argument.
    You may need to install the MATLAB Engine API for Python for this to work.

    Args:
        script_path (str): The path to the MATLAB script to execute.
        matlab_engine: An instance of the MATLAB engine.

    Returns:
        Any: The result of the MATLAB script execution.
    """
    try:
        result = matlab_engine.run(script_path, nargout=0)
        return result
    except Exception as e:
        print(f"Error executing MATLAB script: {e}")
        return None

import numpy as np

def matlab_to_numpy(eng, var_name):
    """
    将 MATLAB 变量转换为 NumPy 数组。

    参数:
    eng -- MATLAB 引擎实例
    var_name -- MATLAB 工作空间中的变量名

    返回:
    numpy_var -- 转换后的 NumPy 数组
    """
    matlab_var = eng.workspace[var_name]

    if isinstance(matlab_var, matlab.double):
        numpy_var = np.array(matlab_var)
    elif isinstance(matlab_var, matlab.single):
        numpy_var = np.array(matlab_var, dtype=np.float32)
    elif isinstance(matlab_var, matlab.int8):
        numpy_var = np.array(matlab_var, dtype=np.int8)
    elif isinstance(matlab_var, matlab.int16):
        numpy_var = np.array(matlab_var, dtype=np.int16)
    elif isinstance(matlab_var, matlab.int32):
        numpy_var = np.array(matlab_var, dtype=np.int32)
    elif isinstance(matlab_var, matlab.int64):
        numpy_var = np.array(matlab_var, dtype=np.int64)
    elif isinstance(matlab_var, matlab.uint8):
        numpy_var = np.array(matlab_var, dtype=np.uint8)
    elif isinstance(matlab_var, matlab.uint16):
        numpy_var = np.array(matlab_var, dtype=np.uint16)
    elif isinstance(matlab_var, matlab.uint32):
        numpy_var = np.array(matlab_var, dtype=np.uint32)
    elif isinstance(matlab_var, matlab.uint64):
        numpy_var = np.array(matlab_var, dtype=np.uint64)
    elif isinstance(matlab_var, matlab.logical):
        numpy_var = np.array(matlab_var, dtype=bool)
    elif isinstance(matlab_var, str):
        numpy_var = np.array(matlab_var)
    else:
        print(f"Unsupported MATLAB type: {type(matlab_var)}")
        numpy_var = None

    return numpy_var

# # 使用示例
# kmph_numpy = matlab_to_numpy(eng, 'kmph')

# if kmph_numpy is not None:
#     print(f"NumPy array type: {kmph_numpy.dtype}")
#     print(f"NumPy array shape: {kmph_numpy.shape}")
# print(kmph_numpy)

def load_mat_file(filename):
    """
    Load a MATLAB .mat file, handling both older versions and v7.3 files,
    and converting MATLAB structures to nested Python dictionaries.
    """
    try:
        # Try loading using scipy.io.loadmat
        data = scipy.io.loadmat(filename, struct_as_record=False, squeeze_me=True)
        data = _check_keys(data)
    except NotImplementedError:
        # For v7.3 files, use h5py
        data = {}
        with h5py.File(filename, 'r') as f:
            def h5py_to_dict(obj):
                if isinstance(obj, h5py.Dataset):
                    return obj[()]
                elif isinstance(obj, h5py.Group):
                    return {key: h5py_to_dict(obj[key]) for key in obj.keys()}
                else:
                    return obj
            for key in f.keys():
                data[key] = h5py_to_dict(f[key])
    return data

def _check_keys(d):
    """
    Checks if entries in dictionary are mat-objects. If yes,
    convert them to nested dictionaries.
    """
    for key in d:
        if isinstance(d[key], scipy.io.matlab.mat_struct):
            d[key] = _todict(d[key])
    return d

def _todict(matobj):
    """
    Recursively constructs nested dictionaries from MATLAB structs.
    """
    d = {}
    for fieldname in matobj._fieldnames:
        elem = getattr(matobj, fieldname)
        if isinstance(elem, scipy.io.matlab.mat_struct):
            d[fieldname] = _todict(elem)
        else:
            d[fieldname] = elem
    return d

# Example usage
# if __name__ == "__main__":
#     file_path = "example.m"  # Replace with your MATLAB script path
#     parsed_data = parse_matlab_script(file_path)
#     print(parsed_data)
#
#     # Generate a simple MATLAB script
#     script_content = [
#         "% This is a sample MATLAB script",
#         "x = 1:10;",
#         "y = sin(x);",
#         "plot(x, y);",
#         "title('Sine Wave');",
#         "xlabel('X');",
#         "ylabel('Y');"
#     ]
#     generated_script = generate_matlab_script(script_content)
#     print(generated_script)
#
#     # To execute a MATLAB script, you would need to set up the MATLAB engine
#     # import matlab.engine
#     # eng = matlab.engine.start_matlab()
#     # result = execute_matlab_script("path_to_script.m", eng)
#     # eng.quit()