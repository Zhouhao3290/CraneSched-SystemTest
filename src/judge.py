
def dict_contains(dict1, dict2):
    """
    判断 dict1 是否包含 dict2 的所有键值对。

    :param dict1: 主字典，可能包含更多的键值对。
    :param dict2: 被包含的字典，所有键值对必须存在于 dict1 中。
    :return: 如果 dict1 包含 dict2 中所有的键值对，返回 True，否则返回 False。
    """
    for key, value in dict2.items():
        # 检查 dict1 中是否有 dict2 的 key，并且 dict1[key] == dict2[key]
        if key not in dict1 or dict1[key] != value:
            return False
    return True

def dict_equal(dict1, dict2):
    return dict1 == dict2