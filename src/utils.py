import subprocess

def get_response(command) -> dict:
    response = run_shell_command(command)
    if response is None: return {}
    output = response.stdout.strip()

    data = {}
    for line in output.splitlines():
        if ':' in line:
            key, value = line.split(':', 1)
            data[key.strip()] = value.strip()

    return data

def run_shell_command(command):
    """
    执行一个 Shell 命令。

    :param command: 需要执行的命令，字符串形式。
    :return: dict数据。
    """
    try:
        # 执行 Shell 命令
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {e}")
        return None
