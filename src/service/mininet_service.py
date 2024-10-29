import shlex
import subprocess
import os

class MininetService:
    def __init__(self, command):
        self.process = None
        self.command = command

    def start(self):
        """启动服务并返回服务对象"""

        try:
            # 使用 subprocess 启动服务
            self.process = subprocess.Popen(
                shlex.split(self.command),   # 分割命令行字符串，以便正确处理参数
                stdout=subprocess.PIPE,      # 将标准输出重定向到管道
                stderr=subprocess.PIPE,      # 将标准错误重定向到管道
                preexec_fn=os.setsid         # 在新的进程组中运行子进程
            )
            print(f"服务已启动，PID: {self.process.pid}")
            return self
        except Exception as e:
            print(f"启动服务时出错: {e}")
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