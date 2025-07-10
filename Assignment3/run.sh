# 检查perf是否安装
perf --version

# 如果未安装，安装perf
sudo apt-get install linux-tools-common linux-tools-generic linux-tools-`uname -r`

# 克隆FlameGraph仓库
git clone https://github.com/brendangregg/FlameGraph.git


# 克隆perf-map-agent仓库
git clone https://github.com/jvm-profiling-tools/perf-map-agent.git
cd perf-map-agent

# 编译
cmake .
make

# 启动Java应用时添加JVM参数
java -XX:+PreserveFramePointer -XX:+UnlockDiagnosticVMOptions -XX:+DebugNonSafepoints -jar SPECjvm2008.jar compress

# 运行perf stat收集系统级指标
perf stat -p <PID> sleep 30

# 记录调用栈信息
perf record -F 99 -g -p <PID> -- sleep 60

# 使用perf report查看概要
perf report

# 提取原始数据
perf script > perf.script

# 使用FlameGraph提供的脚本转换格式
~/FlameGraph/stackcollapse-perf.pl perf.script > perf.folded

# 使用Python导出数据到SQLite数据库
python import_perf.py

# 进入SQLite交互模式
sqlite3 perf.db

# 设置输出格式
.mode column
.headers on
SELECT stack, SUM(count) AS total_count 
FROM perf_data 
GROUP BY stack 
ORDER BY total_count DESC 
LIMIT 10;

# 生成火焰图
FlameGraph/flamegraph.pl perf.folded > compress-flamegraph.svg
