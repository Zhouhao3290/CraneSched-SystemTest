import os
import re
import json
import logging
import collections

from constants import *
from judge import *
from utils import run_shell_command, get_response_dict

logger = logging.getLogger()


def get_all_system_test_cases(folder: str, case_list: list):
    """
    get all cases by path, and then merge by base case, the level of val in cur case is higher than it in base case.
    :param case_list: input case_name list
    :param folder: path for all cases
    :return: get a deque with all system cases for running time
    """
    cases_deque = collections.deque()
    for dir_path, dir_names, file_names in os.walk(folder):  # 遍历folder文件夹下所有子目录和文件
        for file_name in file_names:
            match = re.search(r'^case_(?P<name>\w+)\.json$', file_name)
            if match is None or (len(list) > 0 and file_name not in case_list):
                continue
            with open(os.path.join(dir_path, file_name), encoding='utf-8') as f:
                case_json = json.load(f)
                cases_deque.append(case_json)
    return cases_deque

def run_test_process(process) -> bool:
    if not process:
        return False
    for item in process:
        command = item.get('command')
        perfect_match = item.get('perfect_match', True)
        judger = item.get("judger")
        response = get_response_dict(command)
        if perfect_match:
            if not dict_equal(response, judger): return False
        else:
            if not dict_contains(response, judger): return False
    return True

def init_case():
    # 清空数据库
    run_shell_command(CLEAN_ALL_TABLES_SHELL_COMMAND)
    # 创建一个qos TestQos
    run_shell_command(ADD_QOS_CRANE_COMMAND)
    # 创建一个主账号 MainTestAccount
    run_shell_command(ADD_MAIN_ACCOUNT_CRANE_COMMAND)
    # 创建一个子账号 SubTestAccount
    run_shell_command(ADD_SUB_ACCOUNT_CRANE_COMMAND)
    # 创建一个用户 TestUser
    run_shell_command(ADD_USER_SHELL_COMMAND)
    run_shell_command(ADD_USER_CRANE_COMMAND)



