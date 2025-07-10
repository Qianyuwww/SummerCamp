# 下载Kona-8安装包
wget https://github.com/Tencent/TencentKona-8/releases/download/8.0.22-GA/TencentKona8.0.22.b1_jdk_linux-x86_64_8u452.tar.gz

# 安装
tar zxvf TencentKona8.0.22.b1_jdk_linux-x86_64_8u452.tar.gz

# 环境配置
export JAVA_HOME=/path/to/TencentKona-8
export PATH=$JAVA_HOME/bin:$PATH

# 测试运行
java -Xms4g -Xmx8g -XX:+UseG1GC -XX:+G1ParallelFullGC -XX:+G1RebuildRemSet -jar SPECjvm2008.jar –base -pf props/specjvm.properties
