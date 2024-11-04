import shlex
import subprocess
import os
import time

class CraneCtldService:
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

            with open(self.log_file, 'w') as outfile:
            # 使用 subprocess 启动服务
                self.process = subprocess.Popen(
                    shlex.split(self.command),
                    stdout=outfile,
                    stderr=outfile,
                    preexec_fn=os.setsid
                )
            print(f"ctld服务已启动，PID={self.process.pid}")

            start_time = time.time()
            timeout = 180
            search_success_string = 'All craned nodes are up'
            search_up_string = 'is up now'
            need_cnt = 4
            while self.is_running() and time.time() - start_time < timeout:
                success_cnt = 0
                is_start = False
                with open(self.log_file, 'r') as log_file:
                    for line in log_file:
                        if search_success_string in line:
                            is_start = True
                        if search_up_string in line:
                            success_cnt += 1
                            if success_cnt >= need_cnt:
                                is_start = True
                if  is_start:
                    print(f"Found '{search_success_string}' or '{search_up_string}' in {self.log_file}.")
                    print(f"ctld服务启动完成，PID: {self.process.pid}")
                    return self
                else:
                    time.sleep(10)
            print(f"ctld服务启动超时或失败，PID: {self.process.pid}, 详情可见：{self.log_file}")
            self.stop()
            return None
        except Exception as e:
            print(f"启动ctld服务时出错: {e}, 详情可见：{self.log_file}")
            self.stop()
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