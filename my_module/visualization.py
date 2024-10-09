import matplotlib.pyplot as plt

def plot_data(data):
    """
    绘制数据的简单图表。
    
    :param data: 要绘制的数据列表或数组
    """
    plt.plot(data)
    plt.title("简单数据可视化")
    plt.xlabel("X轴")
    plt.ylabel("Y轴")
    plt.show()