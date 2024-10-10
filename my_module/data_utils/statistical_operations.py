import statistics

def mean(data):
    """
    计算数据的平均值
    
    :param data: 数值列表
    :return: 平均值
    """
    return statistics.mean(data)

def median(data):
    """
    计算数据的中位数
    
    :param data: 数值列表
    :return: 中位数
    """
    return statistics.median(data)

def mode(data):
    """
    计算数据的众数
    
    :param data: 数值列表
    :return: 众数
    """
    return statistics.mode(data)

def standard_deviation(data):
    """
    计算数据的标准差
    
    :param data: 数值列表
    :return: 标准差
    """
    return statistics.stdev(data)

def variance(data):
    """
    计算数据的方差
    
    :param data: 数值列表
    :return: 方差
    """
    return statistics.variance(data)