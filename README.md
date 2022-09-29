# VWMSDS_Demo_FileTransferTools

1.设置配置文件config.ini：
----[audiopath]	本地音频目录, 电脑存放音频的路径; 
----[phonepath]	手机音频目录, 无需修改，除非开发改路径;
----[project]	Push的项目;

2.运行脚本check_devces_file.py：
----脚本会自动在config.ini的[audiopath]路径下生成具体存放音频的路径.
----例如/home/xslan/Music

3.本地存放wav文件和txt文件：
----需要手动把wav和txt放到相应的场景1234.
----如(/home/xslan/Music/zh_cn/mixasr1/xxx.wav).如(/home/xslan/Music/zh_cn/xxx.txt)

5.准备完毕后，直接运行run2.py执行Push文件。

--------------------------------------------------------------

此外：如要单独Push个别语言，仅需在 "config.ini" 中注释其他项即可。

（注：ZIP包中不能叠ZIP包，share中下载的时候需要注意这个问题。）
