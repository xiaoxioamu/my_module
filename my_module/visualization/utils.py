def get_color_palette(num_curves):
    """
    根据曲线数量返回最佳的颜色组合数组，确保颜色对比明显。

    参数:
    num_curves (int): 曲线数量

    返回:
    list: 十六进制颜色的数组
    ```python
    import matplotlib.pyplot as plt
    import numpy as np

    # 假设你有 num_curves 条曲线
    num_curves = 20
    x = np.linspace(0, 10, 100)
    colors = get_color_palette(num_curves)

    plt.figure()

    for i in range(num_curves):
        y = np.sin(x + i)
        plt.plot(x, y, label=f'Curve {i+1}', color=colors[i])

    plt.legend()
    plt.show()
    ```
    """
    # 预定义颜色集，包含明亮色、深色和中性色，确保区分度明显
    colors = [
        '#FF5733', '#33FF57', '#5733FF', '#FFD700',  # 明亮色
        '#00BFFF', '#FF4500', '#A9A9A9', '#6B8E23',  # 中性/深色
        '#8B4513', '#4682B4', '#BC8F8F', '#D3D3D3',  # 深色/浅色
        '#FF1493', '#00FFFF', '#1E90FF', '#FF6347',  # 更多明亮色
        '#7FFF00', '#FF00FF', '#FF6347', '#708090',  # 中性/暗色
        '#00FF00', '#CD853F', '#F0E68C', '#FAFAD2',  # 较柔和色
        '#E6E6FA', '#F5DEB3', '#BC8F8F', '#778899'   # 更多中性色
    ]
    
    # 如果曲线数量大于预定义颜色集，则通过循环选择颜色
    palette = [colors[i % len(colors)] for i in range(num_curves)]
    
    return palette
