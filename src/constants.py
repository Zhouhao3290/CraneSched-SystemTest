# constants

## file path
CRANE_BIN_PATH = "../Crane/build/src"
CRANE_FRONT_PATH = "../CraneSched-FrontEnd/build/bin"
BIN_PATH = "usr/local/bin"
TEST_FRAME_PATH = "../CraneSched-TestFramework-Evaluator/TestFrame"
DB_SCRIPTS_PATH = "../Crane/scripts"
CONFIG_PATH = "/etc/crane"

## shell command
MININET_SHELL_COMMAND = "python3 crane-mininet.py --conf config.yaml --crane-conf crane-mininet.yaml"
MININET_CLEAN_SHELL_COMMAND = MININET_SHELL_COMMAND + " --clean"
MININET_INIT_SHELL_COMMAND = MININET_SHELL_COMMAND + " --head"
CTLD_SHELL_COMMAND = CRANE_BIN_PATH + "/CraneCtld/cranectld"
CLEAN_NET_SHELL_COMMAND = "mn -c"
CLEAN_ALL_TABLES_SHELL_COMMAND = "sh " + DB_SCRIPTS_PATH + "/WipeData.sh 5"
ADD_USER_SHELL_COMMAND = "useradd TestUser"

## python command
MININET_PYTHON_COMMAND = ['python', TEST_FRAME_PATH, '--conf', 'config.yaml', '--crane-conf', 'crane-mininet.yaml']

## crane command for case init
ADD_QOS_CRANE_COMMAND = "cacctmgr add qos -N=TestQos -D test -c=11 -J=2 -T=1800 -P=999"
ADD_MAIN_ACCOUNT_CRANE_COMMAND = "cacctmgr add account -N=MainTestAccount -D test -p CPU,GPU -q TestQos"
ADD_SUB_ACCOUNT_CRANE_COMMAND = "cacctmgr add account -N=SubTestAccount -P=MainTestAccount -D=test"
ADD_USER_CRANE_COMMAND = "cacctmgr add user -N=TestUser -A=SubTestAccount"
