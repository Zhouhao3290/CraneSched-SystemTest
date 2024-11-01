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

usage() {
  echo "script usage: $0 [-i] [-c] [-a args]"
  echo "  -c 编译工程"
  echo '  -a 运行system test脚本所需参数，args要包含在""里，参考指定执行case1和case2, `./start.sh -a "--case=case1,case2"`'
}

CRANE_BIN_PATH="../Crane/build/src"
CRANE_FRONT_PATH="../CraneSched-FrontEnd/build/bin"
BIN_PATH="/usr/local/bin"
TEST_FRAME_PATH="../CraneSched-TestFramework-Evaluator/TestFrame"
DB_SCRIPTS_PATH="../Crane/scripts"

if [ "$(id -u)" -ne 0 ]; then
    echo "current user is not root."
    exit 1
fi
if [ ! -e "$BIN_PATH" ]; then
    echo "Error: PATH $BIN_PATH does not exist."
    exit 1
fi
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
        h|help)
            usage
            exit 0
            ;;
        ?)
            usage
            exit 0
            ;;
    esac
done

# 1.1 compile crane
if [ ! -e "$CRANE_BIN_PATH/CraneCtld/cranectld" ] || \
    [ ! -e "$CRANE_BIN_PATH/Craned/craned" ] || \
    [ "$need_compile" = true ]; then
    cd ../Crane
    if [ ! -d "$build" ]; then
        mkdir -p build
    fi
    cd build
    cmake -G Ninja ..
      if [ $? -ne 0 ]; then
        echo "compile Crane Ninja failed"
        exit 1
    fi
    cmake --build . --target cranectld craned pam_crane
    if [ $? -ne 0 ]; then
        echo "compile Crane cranectld failed"
        exit 1
    fi
    cd $DIR
fi

# 1.2 compile crane front
if [ ! -e "$CRANE_FRONT_PATH/cinfo" ] || \
    [ ! -e "$BIN_PATH/cinfo" ] || \
    [ "$need_compile" = true ]; then
    cd ../CraneSched-FrontEnd
    make
    if [ $? -ne 0 ]; then
        echo "compile CraneSched-FrontEnd failed"
        exit 1
    fi
    make install
    if [ $? -ne 0 ]; then
        echo "compile CraneSched-FrontEnd failed"
        exit 1
    fi
    yes | cp -rf "$CRANE_FRONT_PATH/." "$BIN_PATH" || {
        echo "copy front bin failed";
        exit 1;
    }
fi

# 2. init
# 2.1 init test frame for virtualizing craned
cd $TEST_FRAME_PATH
mn -c
chmod +x crane-mininet.py
./crane-mininet.py --conf config.yaml --crane-conf crane-mininet.yaml --clean
yes y | ./crane-mininet.py --conf config.yaml --crane-conf crane-mininet.yaml --head

# 2.2 clear all mongoDB tables
cd $DIR
sh $DB_SCRIPTS_PATH/WipeData.sh 5

# 3. start system test
python3 src/main.py $test_args
