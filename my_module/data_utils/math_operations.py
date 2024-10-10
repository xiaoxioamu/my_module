import math
from scipy.signal import butter, filtfilt
def add(a, b):
    """
    计算两个数的和
    
    :param a: 第一个数
    :param b: 第二个数
    :return: a 和 b 的和
    """
    return a + b

def subtract(a, b):
    """
    计算两个数的差
    
    :param a: 被减数
    :param b: 减数
    :return: a 减 b 的差
    """
    return a - b

def multiply(a, b):
    """
    计算两个数的乘积
    
    :param a: 第一个因数
    :param b: 第二个因数
    :return: a 和 b 的乘积
    """
    return a * b

def divide(a, b):
    """
    计算两个数的商
    
    :param a: 被除数
    :param b: 除数
    :return: a 除以 b 的商
    :raises ZeroDivisionError: 当 b 为 0 时
    """
    if b == 0:
        raise ZeroDivisionError("除数不能为0")
    return a / b

def power(base, exponent):
    """
    计算幂
    
    :param base: 底数
    :param exponent: 指数
    :return: base 的 exponent 次幂
    """
    return math.pow(base, exponent)

# Apply a low-pass filter to further smooth the engine torque
def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = filtfilt(b, a, data)
    return y
