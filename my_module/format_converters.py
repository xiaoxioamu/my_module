def json_to_dict(json_string):
    """
    将JSON字符串转换为Python字典。

    :param json_string: JSON格式的字符串
    :return: 转换后的Python字典
    """
    import json
    try:
        return json.loads(json_string)
    except json.JSONDecodeError as e:
        print(f"JSON解析错误: {e}")
        return None

def dict_to_json(dict_obj):
    """
    将Python字典转换为JSON字符串。

    :param dict_obj: Python字典对象
    :return: JSON格式的字符串
    """
    import json
    try:
        return json.dumps(dict_obj, ensure_ascii=False, indent=2)
    except TypeError as e:
        print(f"字典转JSON错误: {e}")
        return None

def csv_to_list(csv_string):
    """
    将CSV字符串转换为Python列表。

    :param csv_string: CSV格式的字符串
    :return: 转换后的Python列表
    """
    import csv
    from io import StringIO
    try:
        f = StringIO(csv_string)
        reader = csv.reader(f)
        return list(reader)
    except csv.Error as e:
        print(f"CSV解析错误: {e}")
        return None

def list_to_csv(list_obj):
    """
    将Python列表转换为CSV字符串。

    :param list_obj: Python列表对象
    :return: CSV格式的字符串
    """
    import csv
    from io import StringIO
    try:
        output = StringIO()
        writer = csv.writer(output)
        writer.writerows(list_obj)
        return output.getvalue().strip()
    except csv.Error as e:
        print(f"列表转CSV错误: {e}")
        return None
    
import warnings

def map_c_type_to_simulink(c_type: str) -> str:
    """
    Maps C data types to corresponding Simulink data types.
    If the type is not recognized, it returns the original type and issues a warning.
    
    Args:
    c_type (str): The C data type to be mapped.
    
    Returns:
    str: The corresponding Simulink data type or the original type if not recognized.
    
    Raises:
    TypeError: If the input is not a string.
    """
    if not isinstance(c_type, str):
        raise TypeError(f"Input must be a string, not {type(c_type)}")

    type_mapping = {
        "u8": "uint8",
        "s8": "int8",
        "u16": "uint16",
        "s16": "int16",
        "u32": "uint32",
        "s32": "int32",
        "u64": "uint64",
        "s64": "int64",
        "f32": "single",
        "f64": "double",
        "bool": "boolean",
        "char": "int8",
        "short": "int16",
        "int": "int32",
        "long": "int32",
        "long long": "int64",
        "float": "single",
        "double": "double"
    }
    
    # Strip any whitespace and convert to lowercase for case-insensitive matching
    c_type_lower = c_type.strip().lower()
    
    if c_type_lower not in type_mapping:
        warnings.warn(f"Unrecognized C type: {c_type}. Using original type.", UserWarning)
        return c_type
    
    return type_mapping[c_type_lower]