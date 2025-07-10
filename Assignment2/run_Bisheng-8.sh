# 下载Bishneg-8安装包
wget https://mirrors.huaweicloud.com/kunpeng/archive/compiler/bisheng_jdk/bisheng-jdk-8u452-b12-linux-x64.tar.gz

# 安装
tar zxvf bisheng-jdk-8u452-b12-linux-x64.tar.gz

# 环境配置
export JAVA_HOME=/path/to/bisheng-jdk-8
export PATH=$JAVA_HOME/bin:$PATH

# 测试运行
java -Xms4g -Xmx8g -XX:+UseG1GC -jar SPECjvm2008.jar –base -pf props/specjvm.properties
