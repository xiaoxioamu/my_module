"""
This module provides functionality for processing and manipulating MATLAB scripts.
"""
import matlab.engine
import numpy as np
import scipy.io
import h5py
import pickle
from typing import Dict, Any, Optional

class MatlabInteractor:
    """
    功能说明:
    这个类提供了一个接口，用于在Python环境中与MATLAB进行交互。
    它允许用户启动MATLAB引擎，执行MATLAB代码，在Python和MATLAB之间传递数据，
    以及加载和保存MATLAB工作空间变量。

    属性:
    - eng: matlab.engine.MatlabEngine, MATLAB引擎实例
    - workspace: Dict[str, Any], 存储从MATLAB工作空间转换到Python的变量

    方法:
    - start_engine(): 启动MATLAB引擎
    - stop_engine(): 停止MATLAB引擎
    - matlab_to_numpy(var_name: str): 将MATLAB变量转换为NumPy数组
    - load_mat_file(filename: str): 加载MATLAB .mat文件
    - save_matlab_workspace(save_path: Optional[str] = None): 保存MATLAB工作空间到Python

    示例:
    ```python
    # 创建MatlabInteractor实例
    interactor = MatlabInteractor()

    # 启动MATLAB引擎
    interactor.start_engine()

    try:
        # 加载MATLAB .mat文件
        data = interactor.load_mat_file("example.mat")
        print("Loaded data:", data)

        # 执行MATLAB代码
        interactor.eng.eval("x = 1:10; y = sin(x);", nargout=0)

        # 将MATLAB变量转换为NumPy数组
        x = interactor.matlab_to_numpy('x')
        y = interactor.matlab_to_numpy('y')
        print("x:", x)
        print("y:", y)

        # 保存MATLAB工作空间到Python
        workspace = interactor.save_matlab_workspace("matlab_workspace.pkl")
        print("Saved workspace:", workspace.keys())

    finally:
        # 停止MATLAB引擎
        interactor.stop_engine()
    ```
    """

    def __init__(self):
        """
        功能说明:
        初始化MatlabInteractor类。
        """
        self.eng = None
        self.workspace = {}

    def start_engine(self):
        """
        功能说明:
        启动 MATLAB 引擎。如果引擎已连接，提示用户；否则，连接到共享的 'local' 引擎。

        返回值:
        - None
        """
        try:
            # 检查引擎是否已经存在并连接
            if hasattr(self, 'eng') and self.eng is not None:
                # 尝试调用一个简单的 MATLAB 命令以验证连接
                self.eng.eval('1;', nargout=0)
                print("MATLAB 引擎已经连接，无需重复连接。")
            else:
                # 尝试连接到共享的 'local' MATLAB 引擎
                self.eng = matlab.engine.connect_matlab('local')
                print("已连接到现有的 'local' MATLAB 引擎。")
        except matlab.engine.EngineError as e:
            print(f"无法连接到 MATLAB 引擎 'local'：{e}")
            # 根据需要，您可以选择在此启动新的 MATLAB 引擎或采取其他措施
            # 例如，您可以提示用户检查 MATLAB 引擎是否已共享
        except Exception as e:
            print(f"发生未知错误: {e}")

    def stop_engine(self):
        """
        功能说明:
        停止MATLAB引擎。

        返回值:
        - None
        """
        if self.eng:
            self.eng.quit()
            self.eng = None
            print("MATLAB engine stopped.")
        else:
            print("MATLAB engine is not running.")

    def matlab_to_numpy(self, var_name: str) -> np.ndarray:
        """
        功能说明:
        将MATLAB变量转换为NumPy数组。

        参数:
        - var_name: str, MATLAB工作空间中的变量名

        返回值:
        - np.ndarray: 转换后的NumPy数组
        """
        if not self.eng:
            raise RuntimeError("MATLAB engine is not started. Call start_engine() first.")

        matlab_var = self.eng.workspace[var_name]

        if isinstance(matlab_var, matlab.double):
            return np.array(matlab_var)
        elif isinstance(matlab_var, matlab.single):
            return np.array(matlab_var, dtype=np.float32)
        elif isinstance(matlab_var, (matlab.int8, matlab.int16, matlab.int32, matlab.int64,
                                     matlab.uint8, matlab.uint16, matlab.uint32, matlab.uint64)):
            return np.array(matlab_var, dtype=np.dtype(matlab_var.__class__.__name__[6:]))
        elif isinstance(matlab_var, matlab.logical):
            return np.array(matlab_var, dtype=bool)
        elif isinstance(matlab_var, str):
            return np.array(matlab_var)
        elif isinstance(matlab_var, (int, float)):
            return np.array(matlab_var)
        else:
            raise ValueError(f"Unsupported MATLAB type: {type(matlab_var)}")

    def load_mat_file(self, filename: str) -> Dict[str, Any]:
        """
        功能说明:
        加载MATLAB .mat文件，处理旧版本和v7.3版本的文件，
        并将MATLAB结构转换为嵌套的Python字典。

        参数:
        - filename: str, .mat文件的路径

        返回值:
        - Dict[str, Any]: 包含加载数据的字典
        """
        try:
            data = scipy.io.loadmat(filename, struct_as_record=False, squeeze_me=True)
            return self._check_keys(data)
        except NotImplementedError:
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

    def _check_keys(self, d: Dict[str, Any]) -> Dict[str, Any]:
        """
        功能说明:
        检查字典中的条目是否为mat对象。如果是，将它们转换为嵌套字典。

        参数:
        - d: Dict[str, Any], 要检查的字典

        返回值:
        - Dict[str, Any]: 处理后的字典
        """
        for key in d:
            if isinstance(d[key], scipy.io.matlab.mat_struct):
                d[key] = self._todict(d[key])
        return d

    def _todict(self, matobj: scipy.io.matlab.mat_struct) -> Dict[str, Any]:
        """
        功能说明:
        递归地将MATLAB结构转换为嵌套字典。

        参数:
        - matobj: scipy.io.matlab.mat_struct, MATLAB结构对象

        返回值:
        - Dict[str, Any]: 转换后的嵌套字典
        """
        d = {}
        for fieldname in matobj._fieldnames:
            elem = getattr(matobj, fieldname)
            if isinstance(elem, scipy.io.matlab.mat_struct):
                d[fieldname] = self._todict(elem)
            else:
                d[fieldname] = elem
        return d

    def save_matlab_workspace(self, save_path: Optional[str] = None) -> Dict[str, np.ndarray]:
        """
        功能说明:
        将MATLAB工作空间中的所有变量提取并转换为Python中的NumPy数组，支持保存到文件。

        参数:
        - save_path: str, 可选，指定保存转换后变量的文件路径（使用pickle格式）。如果不提供，则不保存。

        返回值:
        - Dict[str, np.ndarray]: 包含所有转换后变量的字典，键为变量名，值为对应的NumPy数组。
        """
        if not self.eng:
            raise RuntimeError("MATLAB engine is not started. Call start_engine() first.")

        self.workspace = {}
        workspace_vars = self.eng.eval('who', nargout=1)
        for var_name in workspace_vars:
            self.workspace[var_name] = self.matlab_to_numpy(var_name)

        if save_path:
            with open(save_path, 'wb') as f:
                pickle.dump(self.workspace, f)
            print(f"Variables saved to {save_path}")

        return self.workspace


