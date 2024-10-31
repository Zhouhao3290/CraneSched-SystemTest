import shlex
import subprocess
import os
import sys
import time

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)
from src.utils import run_shell_command


class MininetService:
    def __init__(self, command, log_file):
        self.process = None
        self.command = command
        self.log_file = log_file

    def start(self):
        """启动服务并返回服务对象"""
        try:
            output_dir = os.path.dirname(self.log_file)
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir)
            # env = os.environ.copy()

            # python_executable = sys.executable
            # env['PYTHONPATH'] = os.path.dirname(os.path.abspath('/nfs/home/zhouhao/repo/CraneSched-TestFramework-Evaluator/TestFrame/crane-mininet.py'))
            with open(self.log_file, 'w') as outfile:
            # 使用 subprocess 启动服务
            #     self.process = subprocess.Popen(
            #         ['/nfs/home/zhouhao/repo/CraneSched-TestFramework-Evaluator/TestFrame/crane-mininet.py', '--conf', '/nfs/home/zhouhao/repo/CraneSched-TestFramework-Evaluator/TestFrame/config.yaml', '--crane-conf', '/nfs/home/zhouhao/repo/CraneSched-TestFramework-Evaluator/TestFrame/crane-mininet.yaml'],
            #         # cwd='/nfs/home/zhouhao/repo/CraneSched-TestFramework-Evaluator/TestFrame',
            #         stdout=outfile,
            #         stderr=outfile,
            #         preexec_fn=os.setsid,
            #         # env=env
            #     )
            #     cmd =  ['python', '/nfs/home/zhouhao/repo/CraneSched-TestFramework-Evaluator/TestFrame/crane-mininet.py', '--conf', '/nfs/home/zhouhao/repo/CraneSched-TestFramework-Evaluator/TestFrame/config.yaml', '--crane-conf', '/nfs/home/zhouhao/repo/CraneSched-TestFramework-Evaluator/TestFrame/crane-mininet.yaml']
            #     process = subprocess.run(cmd, text=True, capture_output=True)
            #     if process.returncode != 0:
            #         print(f"Error: {process.stdout} {process.stderr} ")
            # print(f"mininet服务已启动，PID: {self.process.pid}")
                cmd = 'python /nfs/home/zhouhao/repo/CraneSched-TestFramework-Evaluator/TestFrame/crane-mininet.py --conf /nfs/home/zhouhao/repo/CraneSched-TestFramework-Evaluator/TestFrame/config.yaml --crane-conf /nfs/home/zhouhao/repo/CraneSched-TestFramework-Evaluator/TestFrame/crane-mininet.yaml'
                run_shell_command(cmd)

            start_time = time.time()
            timeout = 60
            search_string = 'successfully!'
            while time.time() - start_time < timeout:
                with open(self.log_file, 'r') as log_file:
                    logs = log_file.read()
                    # 检查日志是否包含特定字符串
                    if search_string in logs:
                        print(f"Found '{search_string}' in logs.")
                        # print(f"mininet服务启动完成，PID: {self.process.pid}")
                        return self
                time.sleep(5)
            # print(f"mininet服务启动超时或失败，PID: {self.process.pid}")
            return None
        except Exception as e:
            print(f"启动mininet服务时异常: {e}")
            return None

    def stop(self):
        """停止服务"""
        if self.process:
            try:
                # os.kill(self.process.pid, 15)  # 发送 SIGTERM 信号
                # self.process.wait()  # 等待进程结束
                print(f"服务已停止，PID=")
            except Exception as e:
                print(f"停止服务时出错: {e}")
            finally:
                self.process = None

    # def is_running(self):
    #     """检查服务是否在运行"""
    #     if self.process :
    #         return self.process.poll() is None
    #     return False