import subprocess
import os
import time


class CraneCtldService:
    def __init__(self, command):
        self.process = None
        self.command = command

    def start(self):
        """启动服务并返回服务对象"""
        try:
            # 使用 Popen 启动服务并创建新的进程组
            self.process = subprocess.Popen(self.command, shell=True, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, preexec_fn=os.setsid)
            print(f"ctld服务已启动，PID={self.process.pid}")

            start_time = time.time()
            timeout = 180
            success = 'All craned nodes are up'
            while self.is_running():
                time.sleep(10)
                output = self.process.stdout.readline()
                if output:
                    decoded_output = output.decode('utf-8').strip()
                    print(decoded_output)  # 打印输出
                    if success in decoded_output:
                        print(f"Found the string '{success}' in the output.")
                        return self

                # 检查是否超时
                if time.time() - start_time >= timeout:
                    print("Timeout reached, service did not return the expected output.")
                    break
            return None
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
        """检查服务是否在运行"""
        if self.process :
            return self.process.poll() is None
        return False