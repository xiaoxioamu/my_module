class VehicleParameters:
    def __init__(self, mass, drag_coefficient, frontal_area, engine_efficiency):
        self.mass = mass  # 车辆质量(kg)
        self.drag_coefficient = drag_coefficient  # 空气阻力系数
        self.frontal_area = frontal_area  # 车辆前面积(m^2)
        self.engine_efficiency = engine_efficiency  # 发动机效率

def convert_kw_to_hp(power_kw):
    """
    将千瓦转换为马力。
    
    :param power_kw: 功率 (千瓦)
    :return: 功率 (马力)
    """
    return power_kw * 1.341

def convert_liters_to_gallons(liters):
    """
    将升转换为加仑。
    
    :param liters: 体积 (升)
    :return: 体积 (加仑)
    """
    return liters * 0.264172