import numpy as np
from typing import List

def array_sum(arr):
    """
    计算数组元素的和
    
    :param arr: 输入数组
    :return: 数组元素的和
    """
    return np.sum(arr)

def array_product(arr):
    """
    计算数组元素的乘积
    
    :param arr: 输入数组
    :return: 数组元素的乘积
    """
    return np.prod(arr)

def array_mean(arr):
    """
    计算数组元素的平均值
    
    :param arr: 输入数组
    :return: 数组元素的平均值
    """
    return np.mean(arr)

def array_max(arr):
    """
    找出数组中的最大值
    
    :param arr: 输入数组
    :return: 数组中的最大值
    """
    return np.max(arr)

def array_min(arr):
    """
    找出数组中的最小值
    
    :param arr: 输入数组
    :return: 数组中的最小值
    """
    return np.min(arr)

def extract_consecutive_elements_within_range(
    array: np.ndarray, 
    lower_bound: float, 
    upper_bound: float
) -> List[np.ndarray]:
    """
    Extracts consecutive subarrays from the input NumPy array where each element 
    is within the specified range [lower_bound, upper_bound].

    Parameters:
    ----------
    array : np.ndarray
        The input NumPy array containing numerical elements.
    lower_bound : float
        The lower bound of the range (inclusive).
    upper_bound : float
        The upper bound of the range (inclusive).

    Returns:
    -------
    List[np.ndarray]
        A list of NumPy subarrays, each containing a sequence of consecutive elements 
        from the input array that are within the specified range.

    Raises:
    ------
    TypeError:
        If the input `array` is not a NumPy ndarray or if `lower_bound`/`upper_bound` 
        are not numerical (int or float) types.
    ValueError:
        If `lower_bound` is greater than `upper_bound`.

    Example:
    -------
    >>> import numpy as np
    >>> array = np.array([0.5, 2.0, -0.3, 0.1, 3.0, -0.5, 0.2])
    >>> extract_consecutive_elements_within_range(array, -1, 1)
    [array([0.5]), array([-0.3,  0.1]), array([-0.5,  0.2])]
    """
    # ---------------------
    # Input Validation
    # ---------------------
    if not isinstance(array, np.ndarray):
        raise TypeError(f"Input 'array' must be a NumPy ndarray, got {type(array)} instead.")
    
    if not isinstance(lower_bound, (int, float)):
        raise TypeError(f"'lower_bound' must be a numerical type (int or float), got {type(lower_bound)} instead.")
    
    if not isinstance(upper_bound, (int, float)):
        raise TypeError(f"'upper_bound' must be a numerical type (int or float), got {type(upper_bound)} instead.")
    
    if lower_bound > upper_bound:
        raise ValueError(f"'lower_bound' ({lower_bound}) cannot be greater than 'upper_bound' ({upper_bound}).")
    
    # ---------------------
    # Step 1: Create a Boolean Mask
    # ---------------------
    mask = (array >= lower_bound) & (array <= upper_bound)
    # Debug: Print the boolean mask
    # print("Boolean Mask:", mask)
    
    # ---------------------
    # Step 2: Identify Start and End Indices of Consecutive Sequences
    # ---------------------
    # Calculate the difference between consecutive elements in the mask
    diff = np.diff(mask.astype(int))
    # Debug: Print the difference array
    # print("Difference:", diff)
    
    # Find indices where sequences start (transition from False to True)
    starts = np.where(diff == 1)[0] + 1
    # Find indices where sequences end (transition from True to False)
    ends = np.where(diff == -1)[0] + 1
    
    # ---------------------
    # Step 3: Handle Edge Cases
    # ---------------------
    # If the first element is within the range, prepend 0 to starts
    if mask[0]:
        starts = np.insert(starts, 0, 0)
    
    # If the last element is within the range, append the length of the array to ends
    if mask[-1]:
        ends = np.append(ends, len(mask))
    
    # ---------------------
    # Step 4: Extract the Subarrays
    # ---------------------
    subarrays = [array[start:end] for start, end in zip(starts, ends)]
    
    return subarrays

# ---------------------
# Example Usage
# ---------------------
# if __name__ == "__main__":
#     # Sample array
#     sample_array = np.array([0.5, 2.0, -0.3, 0.1, 3.0, -0.5, 0.2])

#     # Define the range
#     lower = -1
#     upper = 1

#     # Extract consecutive elements within the range
#     result = extract_consecutive_elements_within_range(sample_array, lower, upper)

#     # Display the results
#     for idx, subarray in enumerate(result, 1):
#         print(f"Subarray {idx}: {subarray}")
