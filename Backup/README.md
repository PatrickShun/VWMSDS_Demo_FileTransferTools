# VWMSDS_Demo_FileTransferTools

1.设置配置文件config.ini：
[audiopath]确认本地音频目录, 后续从这个路径执行push; 
[phonepath]一般不用修改, 用于保存手机的音频目录;
[project]确认测试项目, 用于创建本地的音频目录;

2.运行check_devces_file.py ,自动在自定义的[audiopath]目录生成详细的目录.

3.本地存放音频，需要手动把wav和txt放到相应的场景1234.如(/xx/xx/zh_cn/mixasr1/).如(/xx/xx/zh_cn/)

5.需要push的文件准备好后直接运行run.py执行push。


（注：ZIP包中不能跌ZIP包，share中下载的时候需要注意这个问题。）
