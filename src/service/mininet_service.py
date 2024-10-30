import shlex
import subprocess
import os
import time


class MininetService:
    def __init__(self, command):
        self.process = None
        self.command = command

    def start(self):
        """启动服务并返回服务对象"""

        try:
            # 使用 subprocess 启动服务
            self.process = subprocess.Popen(
                shlex.split(self.command),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                preexec_fn=os.setsid
            )
            print(f"mininet服务已启动，PID: {self.process.pid}")
            start_time = time.time()
            timeout = 60
            while self.is_running() and time.time() - start_time < timeout:
                output = self.process.stdout.readline()
                if output:
                    decoded_output = output.decode('utf-8').strip()
                    print(decoded_output)
            print(f"mininet服务启动完成，PID: {self.process.pid}")
            return self
        except Exception as e:
            print(f"启动mininet服务时出错: {e}")
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