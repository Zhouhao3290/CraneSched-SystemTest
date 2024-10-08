import subprocess
import os

class CraneCtldService:
    def __init__(self):
        self.process = None

    def start(self):
        """启动服务并返回服务对象"""
        try:
            # 使用 Popen 启动服务并创建新的进程组
            self.process = subprocess.Popen("CraneCtld/cranectld", shell=True, preexec_fn=os.setsid)
            print(f"ctld服务已启动，PID={self.process.pid}")
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

    def is_running(self):
        """检查craned服务是否在运行"""
        if self.process :
            return self.process.poll() is None
        return False