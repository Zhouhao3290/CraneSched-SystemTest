import argparse
import traceback

from service.ctld_service import CraneCtldService
from service.mininet_service import MininetService
from case_handle import *
from utils import *
from constants import *

logger = logging.getLogger()

def main():
    ## 初始化参数
    global mininet_service, ctld_service
    parser = argparse.ArgumentParser()
    parser.add_argument('--case', type=str, default='', help='specify cases')
    parser.add_argument('--folder', type=str, default='../testcases', help='path of system test case to main.py')
    args = parser.parse_args()
    case_list = []
    if len(args.case) > 0:
        case_list = args.case.split(',')
    ## 获取所有可执行的用例,并执行用例
    cases = get_all_system_test_cases(os.path.dirname(__file__) + '/' + args.folder, case_list)
    if not cases:
        print("case deque is empty.")
        exit(0)

    ## 初始化
    init()
    try:
        mininet_service = MininetService(MININET_SHELL_COMMAND, TEST_FRAME_PATH, 'mininet.log').start()  ## 启动mininet虚拟化craned
        if mininet_service is None:
            reset()
            exit(1)

        ctld_service = CraneCtldService(CTLD_SHELL_COMMAND, 'ctld.log').start()   ## 启动ctld服务
        if ctld_service is None:
            mininet_service.stop()
            reset()
            exit(1)
    except:
        traceback.print_exc()
        reset()
        exit(1)

    init_case()
    failed, passed, error = 0, 0, 0
    failed_case = []
    for i, case in enumerate(cases):
        case_name = case['name']
        logger.info('execute case {} [{}/{}]'.format(case_name, i + 1, len(cases)))
        process = case['process']
        try:
            if run_test_process(process):
                passed = passed + 1
                logger.error('case {} pass!'.format(case_name))
            else:
                failed_case.append(case_name)
                failed = failed + 1
                logger.error('case {} failed!'.format(case_name))
        except:
            error = error + 1
            failed_case.append(case_name)
            logger.error('case {} error!'.format(case_name))
            traceback.print_exc()
        finally:
            init_case()

    # mininet_service.stop()
    ctld_service.stop()
    # reset()

    if failed > 0 or error > 0:
        logger.warning('system test finishd. passed: {}/{}, failed: {}/{}, error: {}/{}'
                       .format(passed, len(cases), failed, len(cases), error, len(cases)))
        logger.warning('case {} failed, please fix and rerun with arg --case={}.'.format(failed_case,
                                                                                         ','.join(failed_case)))
        exit(1)
    else:
        logger.info('system test finishd. passed: {}/{}, failed: {}/{}, error: {}/{}'
                    .format(passed, len(cases), failed, len(cases), error, len(cases)))

def init():
    # service_config_dict = get_service_config("src/service/service_config.yaml") # 读取测试的服务配置
    # 临时修改ctld启动配置
    backup_and_copy_yaml_file(CONFIG_PATH + "/config.yaml", CONFIG_PATH + "/config_backup.yaml",
                                "src/service/service_config.yaml")
    # 临时修改craned启动配置
    backup_and_copy_yaml_file(TEST_FRAME_PATH + "/crane-mininet.yaml", TEST_FRAME_PATH + "/crane-mininet_backup.yaml",
                                "src/service/service_config.yaml")
    # 临时修改mininet启动配置
    backup_and_copy_yaml_file(TEST_FRAME_PATH + "/config.yaml", TEST_FRAME_PATH + "/config_backup.yaml",
                                "src/service/mininet_config.yaml")
    # mininet_config_dict = get_mininet_config()
    # backup_and_modify_yaml_file(TEST_FRAME_PATH + "/config.yaml", TEST_FRAME_PATH + "/config_backup.yaml",
    #                             mininet_config_dict)

def reset():
    # 恢复ctld启动配置
    recover_file(CONFIG_PATH + "/config.yaml", CONFIG_PATH + "/config_backup.yaml")
    # 恢复craned启动配置
    recover_file(TEST_FRAME_PATH + "/crane-mininet.yaml", TEST_FRAME_PATH + "/crane-mininet_backup.yaml")
    recover_file(TEST_FRAME_PATH + "/config.yaml", TEST_FRAME_PATH + "/config_backup.yaml")

    # 清除虚拟环境
    run_shell_command(CLEAN_NET_SHELL_COMMAND)
    run_shell_command(MININET_CLEAN_SHELL_COMMAND)

if __name__ == '__main__':
    main()
