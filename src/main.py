import logging
import argparse
import os

import yaml
import sys
import json
import traceback

from case_handle import get_all_system_test_cases
from src.judge import dict_contains
from src.service.crane_ctld import CraneCtldService
from utils import *

logger = logging.getLogger()


def main():
    ## 初始化
    parser = argparse.ArgumentParser()
    parser.add_argument('--config_path', type=str, default='conf/conf.yaml',
                        help='config file')
    parser.add_argument('--folder', type=str, default='testcases', help='cases to use')
    args = parser.parse_args()

    ## 修改启动配置
    config_dict = get_deploy_config("testcases/base_case.json")
    copy_and_modify_config_file("/etc/crane/config.yaml", "/etc/crane/config_backup.yaml", config_dict)

    ## 启动craned虚拟节点

    ## 启动ctld服务
    try:
        service = CraneCtldService().start()

    except:
        traceback.print_exc()
    ## 获取所有可执行的用例,并执行用例
    cases = get_all_system_test_cases(args.folder)
    failed, passed, error = 0, 0, 0
    for i, case in enumerate(cases):
        logger.info('execute case {} [{}/{}]'.format(case['name'], i + 1, len(cases)))
        case_name = case['name']
        judger = case['judger']
        command = case['command']
        is_succ = True
        try:
            case_pre_handle()
            resps = get_response(command)
        except:
            is_succ = False
            error = error + 1
            logger.error('case {} execute failed!'.format(case_name))
            traceback.print_exc()

        if is_succ:
            if dict_contains(resps, judger):
                passed = passed + 1
            else:
                failed = failed + 1
    post_handle(service)

def post_handle(self, service) -> None:
    self.service.stop()
    recover_config_file()

if __name__ == '__main__':
    main()
