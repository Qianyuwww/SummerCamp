# 下载OpenJDK-8安装包
wget https://builds.openlogic.com/downloadJDK/openlogic-openjdk/8u452-b09/openlogic-openjdk-8u452-b09-linux-x64.t

# 安装
tar zxvf openjdk-8u452-b09_linux-x64_bin.tar.gz

# 环境配置
export JAVA_HOME=/path/to/openjdk-8
export PATH=$JAVA_HOME/bin:$PATH

# 测试运行
java -Xms4g -Xmx8g -XX:+UseG1GC -jar SPECjvm2008.jar –base -pf props/specjvm.properties 
