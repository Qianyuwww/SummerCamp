# 下载Dragonwell-8安装包
wget https://dragonwell.oss-cn-shanghai.aliyuncs.com/8.25.24/Alibaba_Dragonwell_Standard_8.25.24_x64_linux.tar.gz

# 安装
tar zxvf Alibaba_Dragonwell_Standard_8.25.24_x64_linux.tar.gz

# 环境配置
export JAVA_HOME=/path/to/dragonwell-8
export PATH=$JAVA_HOME/bin:$PATH

# 测试运行
java -Xms4g -Xmx4g -XX:+UseG1GC -jar SPECjvm2008.jar –base -pf props/specjvm.properties
