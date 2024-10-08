#!/bin/bash

set -x  # 开启调试

DIR="$( cd "$( dirname "$0" )/.." && pwd )"
echo DIR

kill_process() {
  pid=`ps -ef | grep "$1" | grep -v "grep" | awk '{print $2}'`
  if [ ! -z "$pid" ]; then
    kill -9 $pid
    echo "killing process '$1' $pid"
  fi
}

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

if [ ! -e "$DIR/../CraneSched/build/src/CraneCtld/cranectld" ] || \
 [ ! -e "$DIR/../CraneSched/build/src/Craned/craned" ] || \
 [ "$need_compile" = true ]; then
  cd "$DIR/../CraneSched"
  if [ ! -d "$build" ]; then
    mkdir -p build
  fi
  cd build
  cmake -G Ninja ..
  cmake --build . --target cranectld craned pam_crane
  if [ $? -eq 0 ]; then
    echo "compile CraneSched failed"
    exit 1
  fi
  cd ..
fi

if [ ! -e "$DIR/../CraneSched-FrontEnd/build/bin/cinfo" ] || \
 [ "$need_compile" = true ]; then
  cd "$DIR/../CraneSched-FrontEnd"
  make
  make install
  if [ $? -eq 0 ]; then
    echo "compile CraneSched-FrontEnd failed"
    exit 1
  fi
fi

sh $DIR/../CraneSched/scripts.sh mode 5

cd $DIR
python3 src/main.py $test_args

usage() {
  echo "script usage: $0 [-i] [-c] [-a args]"
  echo "  -c 编译工程"
  echo '  -a 运行system test脚本所需参数，args要包含在""里，参考指定执行case1和case2, `./start.sh -a "--case=case1,case2"`'
}