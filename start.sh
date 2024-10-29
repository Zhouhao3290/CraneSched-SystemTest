#!/bin/bash

set -x  # 开启调试

DIR="$( cd "$( dirname "$0" )" && pwd )"
echo DIR

kill_process() {
    pid=`ps -ef | grep "$1" | grep -v "grep" | awk '{print $2}'`
    if [ ! -z "$pid" ]; then
        kill -9 $pid
        echo "killing process '$1' $pid"
    fi
}

CRANE_BIN_PATH="../Crane/build/src"
CRANE_FRONT_PATH="../CraneSched-FrontEnd/build/bin"
#BIN_PATH="/usr/local/bin"
TEST_FRAME_PATH="../CraneSched-TestFramework-Evaluator/TestFrame"
DB_SCRIPTS_PATH="../Crane/scripts"

if [ "$(id -u)" -ne 0 ]; then
    echo "current user is not root."
    exit 1
fi
echo "current user is root."
if [ ! -e "$CRANE_BIN_PATH" ]; then
    echo "Error: PATH $CRANE_BIN_PATH does not exist."
    exit 1
fi
if [ ! -e "$CRANE_FRONT_PATH" ]; then
    echo "Error: PATH $CRANE_FRONT_PATH does not exist."
    exit 1
fi
if [ ! -f "$TEST_FRAME_PATH/crane-mininet.py" ]; then
    echo "Error: FILE $TEST_FRAME_PATH/crane-mininet.py does not exist."
    exit 1
fi
if [ ! -f "$DB_SCRIPTS_PATH/WipeData.sh" ]; then
  echo "Error: FILE $DB_SCRIPTS_PATH/WipeData.sh does not exist."
    exit 1
fi

# 1. compile
need_compile=false
while getopts icha: flag; do
    case $flag in
        c)
            need_compile=true
            ;;
        a)
            test_args=$OPTARG
            ;;
        h)
            usage
            exit 0
            ;;
        ?)
            usage
            exit 0
            ;;
    esac
done

# 1.1 compile ctld
if [ ! -e "$CRANE_BIN_PATH/CraneCtld/cranectld" ] || \
    [ ! -e "$CRANE_BIN_PATH/Craned/craned" ] || \
    [ "$need_compile" = true ]; then
    cd ../Crane
    echo "start compile crane."
    if [ ! -d "$build" ]; then
        mkdir -p build
    fi
    cd build
    cmake -G Ninja ..
    cmake --build . --target cranectld craned pam_crane
    if [ $? -eq 0 ]; then
        echo "compile Crane failed"
        exit 1
    fi
    cd $DIR
fi

# 1.2 compile craned
if [ ! -e "$CRANE_FRONT_PATH/cinfo" ] || \
#    [ ! -e "$BIN_PATH/cinfo" ] || \
    [ "$need_compile" = true ]; then
    echo "start compile crane front."
    cd ../CraneSched-FrontEnd
    make
    make install
    if [ $? -eq 0 ]; then
        echo "compile CraneSched-FrontEnd failed"
        exit 1
    fi
    cd $DIR
fi

# 2. init
# 2.1 init test frame for virtualizing craned

cd $TEST_FRAME_PATH
echo "start clean net."

mn -c
chmod +x crane-mininet.py
./crane-mininet.py --conf config.yaml --crane-conf crane-mininet.yaml --clean

echo "start clean table."
# 2.2 clear data table
cd $DIR
sh $DB_SCRIPTS_PATH/WipeData.sh 5


echo "start system test."
python3 src/main.py $test_args

usage() {
  echo "script usage: $0 [-i] [-c] [-a args]"
  echo "  -c 编译工程"
  echo '  -a 运行system test脚本所需参数，args要包含在""里，参考指定执行case1和case2, `./start.sh -a "--case=case1,case2"`'
}