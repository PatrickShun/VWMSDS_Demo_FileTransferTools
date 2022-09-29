#! /usr/bin/env python

import os
import configparser

# 获取绝对路径,__file__代表是本脚本文件,含‘run2.py'.如:/home/xslan/Documents/VWMSDS_Demo_FileTransferTools/run2.py;
PYFILEPWD = os.path.abspath(__file__)

# 根据当前脚本的绝对路径,split方法分割路径与文件名.如:('/home/xslan/Documents/VWMSDS_Demo_FileTransferTools', 'run2.py');
RUNNINGPWD = os.path.split(PYFILEPWD)

# 拼接ini文件的绝对路径.使用分割出来的第一位元素拼接配置文件名称.如:/home/xslan/Documents/VWMSDS_Demo_FileTransferTools/config.ini;
CONFIGPWD = os.path.join(RUNNINGPWD[0], 'config.ini')


class Config(object):
    def __init__(self):
        self.conf = configparser.ConfigParser()             # 初始化configparser模块;
        self.conf.read(CONFIGPWD)                           # 创建configparser对象;
        self.audio_path = self.conf['path']['audiopath']    # 获取需要本地音频的目录'/home/xslan/Music/';
        self.device_path = self.conf['path']['devicepath']   # 获取手机的目录，也就是目标路径'/sdcard/audiowav/';
        self.project = self.conf['config']['project']       # 获取需要push的选项目，eg'CNS_SOP1';
        self.language_list = self.conf.options('language')  # 获取需要push的语言;
        self.wavtype = self.conf.options('audio_type')      # 获取需要push的音频类型;
        self.txttype = self.conf.options('txt_type')        # 获取需要push的txt类型;
        self.scenes = self.conf.options('scenes')           # 获取需要push的场景类型;


if __name__ == "__main__":
    myrun = Config()
