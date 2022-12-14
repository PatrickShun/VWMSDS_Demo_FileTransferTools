#! /usr/bin/env python

import os
import configparser

PWD = os.path.split(os.path.abspath(__file__))[0]              # 获取当前文件run.py的绝对路径，返回元组，仅保存第一个。
CONFIG_FILE = os.path.join(PWD, 'config.ini')                  # 设置ini文件的常量，join拼接绝对路径。
LANGUAGE = ['en_us', 'zh_cn', 'zh_hk', 'zh_sc', 'zh_tw']       # 设置语言列表，用于后续遍历
# LANGUAGE = ['zh_hk', 'zh_sc', 'zh_tw']                        # 设置语言列表，用于后续遍历
WAVTYPE = ['hotword', 'mixasr', 'offlineasr', 'psm']           # 音频的类型
TXTTYPR = ['offnlu.txt', 'psmkey.txt', 'hotwordkey.txt', 'album_all.txt', 'artist_all.txt', 'contact.txt', 'song_all.txt']
changjing = ['场景1', '场景2', '场景3', '场景4']


class Config(object):
    def __init__(self):
        self.conf = configparser.ConfigParser()                # 初始化configparser模块
        self.conf.read(CONFIG_FILE)                            # 创建configparser对象
        self.language_list = LANGUAGE                          # 获取语言列表
        self.wavtype = WAVTYPE                                 # 获取所有的音频类型
        self.audio_path = self.conf['path']['audiopath']       # 获取需要本地音频的目录'/home/xslan/Music/'
        self.project = self.conf['config']['project']          # 获取需要push的选项目'CNS_SOP1'
        self.phonepath = self.conf['path']['phonepath']        # 获取手机的目录，也就是目标路径'/sdcard/audiowav/'


    def abcc(self):
        pass


if __name__ == "__main__":
    myrun = Config()
    print(myrun.project_path)
