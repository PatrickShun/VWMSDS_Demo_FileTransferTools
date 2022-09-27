import os
import subprocess
import GetConfig
from time import sleep

config = GetConfig.Config()             # 初始化配置文件以及数据。
audio_path = config.audio_path          # 获取本地音频路径
device_path = config.device_path        # 获取手机目标路径
project_path = config.project           # 获取需要push的项目
language_list = config.language_list    # 获取所有语言的列表
wavtype = config.wavtype                # 获取需要push的音频类型
txttype = config.txttype                # 获取需要push的txt类型
scenes = config.scenes                  # 获取需要push的场景


def runadb(commend):
    print(str(commend))
    ret = subprocess.run(commend, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
    if ret.returncode == 0:
        print('Success.', ret.returncode)
        return str(ret.returncode)
    else:
        print('Error:', ret.stderr)


def create_android_dir():
    pass


def push_file():
    pass


def statistics_results_wav():
    pass


def statistics_results_txt():
    pass



def irun():
    files = subprocess.getoutput('adb shell ls /sdcard/')
    i = input('是否继续？(Y/n)')
    if i == 'Y':
        create_android_dir()      # 创建必须的文件夹
        push_file()               # push本地的wav文件和txt文件到手机;
        statistics_results_wav()  # push完成后，用于检查wav文件数量是否一致；
        statistics_results_txt()  # push完成后，用于检查txt文件数量是否一致；
    else:
        print('已退出~')
        quit()


if __name__ == "__main__":
    config = GetConfig.Config()  # 初始化配置文件以及数据
    irun()