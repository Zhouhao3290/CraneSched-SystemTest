import argparse
import time
import traceback
from src.service.ctld_service import CraneCtldService
from src.service.mininet_service import MininetService
from src.case_handle import *
from src.utils import *
from src.constants import *

logger = logging.getLogger()

def main():
    ## 初始化参数
    logger.info('start main.py')
    global mininet_service, ctld_service
    parser = argparse.ArgumentParser()
    parser.add_argument('--case', type=str, default='', help='specify cases')
    parser.add_argument('--folder', type=str, default='../testcases', help='cases to use')
    args = parser.parse_args()
    case_list = []
    if len(args.case) > 0:
        case_list = args.case.split(',')

    ## 初始化
    init()
    cur_path = os.getcwd()

    try:
        # mininet_service = MininetService(MININET_SHELL_COMMAND, 'mininet.log').start()  ## 启动mininet虚拟化craned
        # if mininet_service is None:
        #     os.chdir(cur_path)
        #     reset()
        #     exit(1)
        log = 'mininet.log'
        cmd = 'python /nfs/home/zhouhao/repo/CraneSched-TestFramework-Evaluator/TestFrame/crane-mininet.py --conf /nfs/home/zhouhao/repo/CraneSched-TestFramework-Evaluator/TestFrame/config.yaml --crane-conf /nfs/home/zhouhao/repo/CraneSched-TestFramework-Evaluator/TestFrame/crane-mininet.yaml'
        with open(log, "w") as output_file:
            # 使用 subprocess.run 执行命令，并将结果重定向到文件
            subprocess.run(cmd, shell=True, stdout=output_file, stderr=subprocess.STDOUT)
        isFind = False
        start_time = time.time()
        timeout = 60
        search_string = 'successfully!'
        while time.time() - start_time < timeout:
            with open(log, 'r') as log_file:
                logs = log_file.read()
                # 检查日志是否包含特定字符串
                if search_string in logs:
                    print(f"Found '{search_string}' in logs.")
                    isFind = True
                    # print(f"mininet服务启动完成，PID: {self.process.pid}")
            time.sleep(5)
        # print(f"mininet服务启动超时或失败，PID: {self.process.pid}")
        if not isFind:
            print(f"mininet服务启动超时或失败")
            exit(1)

        print("before change, cur_path is " + cur_path)
        os.chdir(TEST_FRAME_PATH)
        print("after change, cur_path is " + os.getcwd())
        run_shell_command(MININET_INIT_SHELL_COMMAND)
        os.chdir(cur_path)
        ctld_service = CraneCtldService(CTLD_SHELL_COMMAND, cur_path + 'ctld.log').start()   ## 启动ctld服务
        if ctld_service is None:
            reset()
            exit(1)
    except:
        traceback.print_exc()
        reset()
        exit(1)

    ## 获取所有可执行的用例,并执行用例
    cases = get_all_system_test_cases(args.folder, case_list)
    if not cases:
        init_case()
    else:
        exit(0)
    failed, passed, error = 0, 0, 0
    failed_case = []
    for i, case in enumerate(cases):
        logger.info('execute case {} [{}/{}]'.format(case['name'], i + 1, len(cases)))
        case_name = case['name']
        process = case['process']
        try:
            if run_test_process(process):
                passed = passed + 1
            else:
                failed = failed + 1
        except:
            error = error + 1
            logger.error('case {} execute failed!'.format(case_name))
            traceback.print_exc()
        finally:
            init_case()

    mininet_service.stop()
    ctld_service.stop()
    reset()

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
    mininet_config_dict = get_mininet_config()
    print("mininet_config_dict is " + json.dumps(mininet_config_dict, indent=4))
    backup_and_modify_yaml_file(TEST_FRAME_PATH + "/config.yaml", TEST_FRAME_PATH + "/config_backup.yaml",
                                mininet_config_dict)

def reset():
    # 恢复ctld启动配置
    recover_file(CONFIG_PATH + "/config.yaml", CONFIG_PATH + "/config_backup.yaml")
    # 恢复craned启动配置
    recover_file(TEST_FRAME_PATH + "/crane-mininet.yaml", TEST_FRAME_PATH + "/crane-mininet_backup.yaml")
    recover_file(TEST_FRAME_PATH + "/config.yaml", TEST_FRAME_PATH + "/config_backup.yaml")

    # 清除虚拟环境
    run_shell_command(CLEAN_NET_SHELL_COMMAND)
    run_shell_command(MININET_CLEAN_SHELL_COMMAND)

def debug():
    if not os.path.exists(TEST_FRAME_PATH + "/crane-mininet.yaml"):
        print("文件 " + TEST_FRAME_PATH + "/crane-mininet.yaml" + " 不存在")
    else:
        print("文件 " + TEST_FRAME_PATH + "/crane-mininet.yaml" + " 存在")
    if not os.path.exists(TEST_FRAME_PATH + "/config.yaml"):
        print("文件 " + TEST_FRAME_PATH + "/config.yaml" + " 不存在")
    else:
        print("文件 " + TEST_FRAME_PATH + "/config.yaml" + " 存在")
    if not os.path.exists(CONFIG_PATH + "/config.yaml"):
        print("文件 " + CONFIG_PATH + "/config.yaml" + " 不存在")
    else:
        print("文件 " + CONFIG_PATH + "/config.yaml" + " 存在")

if __name__ == '__main__':
    main()
