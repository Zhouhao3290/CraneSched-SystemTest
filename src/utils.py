import json
import logging
import string
import subprocess
import os
import traceback

import yaml
import shutil

logger = logging.getLogger()

def get_response_dict(command) -> dict:
    """
    执行shell命令，拿到string的标准输出，并转为dict

    :param command: shell命令
    :return: dict
    """
    output = get_command_response(command)
    try:
        data = json.loads(output)
        return data
    except:
        traceback.print_exc()
        return {}

def get_command_response(command) -> string:
    """
    执行shell命令，并拿到string的标准输出

    :param command: shell命令
    :return: string
    """
    response = run_shell_command(command)
    if response is None:
        print("command is " +  command + ", response is None")
        return ''
    else:
        print("command is " +  command + ", response is " + response.stdout.strip())
        return response.stdout.strip()

def run_shell_command(command):
    """
    执行一个 Shell 命令。

    :param command: 需要执行的命令，字符串形式
    :return:
    """
    try:
        # 执行 Shell 命令
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {e}")
        return None

def read_yaml_to_dict(file_path) -> dict:
    """
    读取执行文件的yaml文件，并转为dict返回

    :param file_path: 文件路径
    :return: dict数据
    """
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"{file_path} not found.")
    with open(file_path, 'r', encoding='utf-8') as file:
        return yaml.safe_load(file) or {}

def backup_and_copy_yaml_file(source_path, backup_path, test_path):
    """
    1. source_path拷贝到backup_path
    2. 删除
    :param source_path: 源文件路径
    :param new_path: 目标文件路径
    :param test_path: 测试配置
    """
    try:
        # config.yaml复制为config_backup.yaml
        if os.path.exists(backup_path):
            os.remove(backup_path)
        shutil.copy(source_path, backup_path)

        if os.path.exists(test_path):
            os.remove(source_path)
            shutil.copy(test_path, source_path)
    except PermissionError:
        print(f"错误：没有权限访问文件")
    except Exception as e:
        print(f"操作失败：{e}")

def backup_and_modify_yaml_file(source_path, backup_path, test_dict):
    """
    备份配置文件并修改配置文件中的内容
    :param source_path: 源文件路径
    :param new_path: 目标文件路径
    :param new_dict: 需要替换的字段和新值
    """
    try:
        # config.yaml复制为config_backup.yaml
        if os.path.exists(backup_path):
            os.remove(backup_path)
        shutil.copy(source_path, backup_path)

        # # 读取yaml文件
        # yaml_content = read_yaml_to_dict(source_path)
        # # 内容替换
        # yaml_content.update(test_dict)

        # 将测试的内容写入文件
        if test_dict:
            with open(source_path, 'w', encoding='utf-8') as file:
                yaml.safe_dump(test_dict, file, default_flow_style=False, allow_unicode=True)
    # except FileNotFoundError:
    #     print(f"错误：源文件 {source_path} 不存在")
    except PermissionError:
        print(f"错误：没有权限访问文件")
    except Exception as e:
        print(f"操作失败：{e}")

def recover_file(source_path, backup_path):
    """
    删除测试用的config.yaml文件，config_backup.yaml改回config.yaml
    """
    try:
        if os.path.exists(backup_path):
            # 删除config.yaml
            os.remove(source_path)
            # config_back.yaml改回config.yaml
            os.rename(backup_path, source_path)
    except FileNotFoundError:
        print(f"错误：文件 {source_path} 不存在")
    except PermissionError:
        print(f"错误：没有权限访问文件")
    except Exception as e:
        print(f"删除失败：{e}")

# def get_service_config(file_path) -> dict:
#     test_config_dict = read_yaml_to_dict(file_path)
#     host_name = get_command_response("hostname")
#     if host_name is None:
#         logger.info('hostname is none.')
#         return exit(1)
#     else:
#         test_config_dict["ControlMachine"] = host_name  ## 更新测试启动配置的hostname
#     return test_config_dict

# def get_mininet_config() -> dict:
#     host_name = get_command_response("hostname")
#     host_ip = get_command_response("hostname -I")
#     if host_name is None or host_ip is None:
#         logger.info('hostname or hostIP is none.')
#         return exit(1)
#     mininet_dict = {
#         "head": host_name,
#         host_name: {
#             "NodeAddr": host_ip + "/24",
#             "HostNum": 4,
#             "Offset": 1,
#             "Subnet": "10.231.0.0/16",
#             "SwitchNum": 1
#         }
#     }
#
#     return mininet_dict