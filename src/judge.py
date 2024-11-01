
# def dict_contains(dict1, dict2):
#     """
#     检查 dict1 中的所有键值对是否都存在于 dict2 中
#
#     :param dict1: 主字典，可能包含更多的键值对。
#     :param dict2: 被包含的字典，所有键值对必须存在于 dict1 中。
#     :return: 如果 dict1 包含 dict2 中所有的键值对，返回 True，否则返回 False。
#     """
#     return all(item in dict2.items() for item in dict1.items())

def part_match(resp: dict, expected_doc: dict) -> bool:
    for doc in resp:
        if dict_contains(doc, expected_doc):
            return True
    return False

def dict_equal(dict1, dict2):
    return dict1 == dict2

def dict_contains(dic1: dict, dic2: dict) -> bool:
    """if dic1 contains dic2
    """
    for key in dic2:
        if key in dic1:
            t = type(dic2[key])
            if not isinstance(dic1[key], t):
                return False
            if t is dict:
                if not dict_contains(dic1[key], dic2[key]):
                    return False
            elif t is list:
                if not list_contains(dic1[key], dic2[key]):
                    return False
            elif t is set:
                if not set_contains(dic1[key], dic2[key]):
                    return False
            elif t is float:
                if abs(dic1[key] - dic2[key]) > 1e-4:
                    return False
            elif dic1[key] != dic2[key]:
                return False
        else:
            return False
    return True

def list_contains(l1: list, l2: list) -> bool:
    for item2 in l2:
        t = type(item2)
        flag = False
        for item1 in l1:
            if not isinstance(item1, t):
                continue
            if ((t is dict and dict_contains(item1, item2)) or
                    (t is list and list_contains(item1, item2)) or
                    (t is set and set_contains(item1, item2)) or
                    (t is float and abs(item1 - item2) < 1e-4) or
                    item1 == item2):
                flag = True
                break
        if not flag:
            return False
    return True


def set_contains(s1: set, s2: set) -> bool:
    for item2 in s2:
        t = type(item2)
        flag = False
        for item1 in s1:
            if not isinstance(item1, t):
                continue
            if ((t is dict and dict_contains(item1, item2)) or
                    (t is list and list_contains(item1, item2)) or
                    (t is set and set_contains(item1, item2)) or
                    (t is float and abs(item1 - item2) < 1e-4) or
                    item1 == item2):
                flag = True
                break
        if not flag:
            return False
    return True