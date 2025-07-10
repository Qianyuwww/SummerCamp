# 下载基准
wget https://www.spec.org/downloads/osg/java/SPECjvm2008_1_01_setup.jar

# 安装
java -jar SPECjvm2008_1_01_setup.jar -i console

# 运行
java -jar SPECjvm2008.jar –base -pf props/specjvm.properties
