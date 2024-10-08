import os
import re
import json
import logging
import collections

logger = logging.getLogger()


def get_all_system_test_cases(folder: str) -> list:
    """
    get all cases by path, and then merge by base case, the level of val in cur case is higher than it in base case.
    :param folder: path for all cases
    :return: get a deque with all system cases for running time
    """
    cases_deque = collections.deque()
    for dir_path, dir_names, file_names in os.walk(folder):  # 遍历folder文件夹下所有子目录和文件
        for file_name in file_names:
            match = re.search(r'^case_(?P<name>\w+)\.json$', file_name)
            if match is None:
                continue
            with open(os.path.join(dir_path, file_name), encoding='utf-8') as f:
                case_json = json.load(f)
                cases_deque.append(case_json)

    return cases_deque
