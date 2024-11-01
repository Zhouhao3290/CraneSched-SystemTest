import shlex
import subprocess
import os
import time

class MininetService:
    def __init__(self, command, path, log_file):
        self.process = None
        self.command = command
        self.path = path
        self.log_file = log_file

    def start(self):
        """启动服务并返回服务对象"""
        try:
            output_dir = os.path.dirname(self.log_file)
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir)

            with open(self.log_file, 'w') as outfile:
            # 使用 subprocess 启动服务
                self.process = subprocess.Popen(
                    self.command,
                    cwd=self.path,
                    stdout=outfile,
                    stderr=outfile,
                    preexec_fn=os.setsid,
                    shell=True
                )
            print(f"mininet服务已启动，PID: {self.process.pid}")
            start_time = time.time()
            timeout = 60
            search_string = 'successfully!'
            while self.is_running() and time.time() - start_time < timeout:
                with open(self.log_file, 'r') as log_file:
                    logs = log_file.read()
                    # 检查日志是否包含特定字符串
                    if search_string in logs:
                        print(f"Found '{search_string}' in logs.")
                        print(f"mininet服务启动完成，PID: {self.process.pid}")
                        return self
                time.sleep(5)
            print(f"mininet服务启动超时或失败，PID: {self.process.pid}")
            return None
        except Exception as e:
            print(f"启动mininet服务时异常: {e}")
            return None

    def stop(self):
        """停止服务"""
        if self.process:
            try:
                os.kill(self.process.pid, 15)  # 发送 SIGTERM 信号
                self.process.wait()  # 等待进程结束
                print(f"服务已停止，PID={self.process.pid}")
            except Exception as e:
                print(f"停止服务时出错: {e}")
            finally:
                self.process = None

    def is_running(self):
        """检查服务是否在运行"""
        if self.process :
            return self.process.poll() is None
        return False