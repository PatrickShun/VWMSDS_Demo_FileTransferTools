# coding:utf-8
# -- coding: UTF-8 --

import os
import subprocess
import GetConfig
from time import sleep

config = GetConfig.Config()         # 初始化配置文件以及数据。
audio_path = config.audio_path      # 获取本地音频路径
project_path = config.project       # 获取需要push的项目
phone_path = config.phonepath       # 获取目标音频路径
language_list = config.language_list  # 获取所有语言的列表
wavtype = config.wavtype            # 获取需要push的音频类型


def runadb(commend):  # 用于执行adb命令，只需要传入命令即可执行。
    print(str(commend))
    ret = subprocess.run(commend, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
    if ret.returncode == 0:
        print('Success.', ret.returncode)
        return str(ret.returncode)
    else:
        print('Error:', ret.stderr)


def check_devces_file():  # 判断sdcard/目录下有没有audiowav目录, 如果没有则新创建
    files = subprocess.getoutput('adb shell ls /sdcard/')
    if 'audiowav' in str(files):
        print('有audiowav文件夹，即将开始推送...')
    else:
        print('无audiowav文件夹, 请确认是否继续？')
    i = input('是否继续？(Y/n)')
    if i == 'Y':
        return True
    else:
        return False


def create_android_dir():
    runadb('adb shell mkdir -p /sdcard/audiowav/')
    for lang in language_list:  # 语言
        for wy in wavtype:  # 音频类型
            for scenes in range(1, 5):  # 场景1234
                target_dir = os.path.join(phone_path, lang, (wy + str(scenes)))
                adb_command = 'adb shell mkdir -p ' + target_dir
                runadb(adb_command)


def push_file():
    for lang in language_list:
        for wt in wavtype:
            for scenes in range(1, 5):
                local_dir = os.path.join(audio_path, project_path, lang, wt + str(scenes))
                phone_dir = os.path.join(phone_path, lang, wt + str(scenes))
                adbpush_wav = 'adb push %s/*.wav %s' % (local_dir, phone_dir)
                runadb(adbpush_wav)
                sleep(0.5)
                local_num = total_quantity('other', 'wav', local_dir)
                print('本地音频路径%s,文件数：%s' % (local_dir, local_num))
                phone_num = total_quantity('adb', 'wav', phone_dir)
                print('手机音频路径%s,文件数：%s' % (phone_dir, phone_num))
                if phone_num == 0 or local_num == 0:
                    print("ERROR, 本地路径没有文件！\n")
                elif phone_num >= 1 and phone_num == local_num:
                    print("Done, Push完成，数量正确！\n")
                else:
                    print("！！！本地文件和手机文件的数量不一致，请检查！！！\n")
        # push txt
        local_txt_dir = os.path.join(audio_path, project_path, lang)
        phone_txt_dir = os.path.join(phone_path, lang)
        adbpush_txt = 'adb push %s/*.txt %s' % (local_txt_dir, phone_txt_dir)
        runadb(adbpush_txt)

        local_txt_num = total_quantity('other', 'txt', local_txt_dir)
        print('本地文本路径%s,文件数：%s' % (local_txt_dir, local_txt_num))
        phone_txt_num = total_quantity('adb', 'txt', phone_txt_dir)
        print('手机文本路径%s,文件数：%s' % (phone_txt_dir, phone_txt_num))
        if phone_txt_num == 0 or local_txt_num == 0:
            print("ERROR, 本地路径没有txt文件！\n")
        elif phone_txt_num >= 1 and phone_txt_num == local_txt_num:
            print("Done, Push完成，txt文件数量正确！\n")
        else:
            print("！！！本地文件和手机文件的数量不一致，请检查！！！\n")


def total_quantity(comm_type, filetype, total_path):
    # total_quantity = 'adb' or 'other' 用于区分在手机的还是本地执行
    # filetype = 'wav' or 'txt'
    # total_path = '/sdcard/audiowav/en_us/hotword1'
    if comm_type == 'adb':
        ad = 'adb shell '
    else:
        ad = ''
    adbcomm = '%sls -l %s | grep "^-" | grep -c "%s$"' % (ad, total_path, filetype)
    ret = subprocess.Popen(adbcomm, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='UTF-8')
    ret.wait()
    numb = int(ret.stdout.read())
    return numb


def statistics_results_wav():
    # 1.格式化打印出文件夹的文件数：
    lens = 12  # 设定列间距; 打印标题:('\t'是横向格式化符, 'len'参数用于设定str列的间距,'str'参数用于设定标题, 主要用于解决标题过长的问题.)
    titles = ['en_dev', 'en_loc', 'cn_dev', 'cn_loc', 'hk_dev', 'hk_loc', 'sc_dev', 'sc_loc', 'tw_dev', 'tw_loc']
    print('{str: <{len}}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}'.format(titles[0], titles[1], titles[2], titles[3],
                                                                         titles[4], titles[5], titles[6], titles[7],
                                                                         titles[8], titles[9], len=lens,
                                                                         str='Audio_type_wav'))
    # 创建保存路径的字典
    language_dev_num = dict.fromkeys(('en_us', 'zh_cn', 'zh_hk', 'zh_sc', 'zh_tw',), 0)
    language_loc_num = dict.fromkeys(('en_us', 'zh_cn', 'zh_hk', 'zh_sc', 'zh_tw',), 0)

    # 遍历字典，组装路径，使用路径请求adb命令，获取文件数量。
    for wt in wavtype:
        for i in range(1, 5):
            for lang in language_list:
                dev_path = os.path.join(phone_path, lang, wt + str(i))
                loc_path = os.path.join(audio_path, project_path, lang, wt + str(i))
                language_dev_num[lang] = total_quantity('adb', 'wav', dev_path)
                language_loc_num[lang] = total_quantity('local', 'wav', loc_path)

            print("{str: <{len}}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}".format
                  (language_dev_num['en_us'], language_loc_num['en_us'], language_dev_num['zh_cn'],
                   language_loc_num['zh_cn'], language_dev_num['zh_hk'], language_loc_num['zh_hk'],
                   language_dev_num['zh_sc'], language_loc_num['zh_sc'], language_dev_num['zh_tw'],
                   language_loc_num['zh_tw'], len=lens, str=wt + str(i)))


def statistics_results_txt():
    lens = 12  # 设定列间距;
    titles = ['en_dev', 'en_loc', 'cn_dev', 'cn_loc', 'hk_dev', 'hk_loc', 'sc_dev', 'sc_loc', 'tw_dev', 'tw_loc']
    print('{str: <{len}}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}'.format
          (titles[0], titles[1], titles[2], titles[3], titles[4], titles[5],
           titles[6], titles[7], titles[8], titles[9], len=lens, str='Test_txt'))

    language_dev = dict.fromkeys(('en_us', 'zh_cn', 'zh_hk', 'zh_sc', 'zh_tw'), 'null')
    language_loc = dict.fromkeys(('en_us', 'zh_cn', 'zh_hk', 'zh_sc', 'zh_tw'), 'null')
    language_dev_num = dict.fromkeys(('en_us', 'zh_cn', 'zh_hk', 'zh_sc', 'zh_tw'), 0)
    language_loc_num = dict.fromkeys(('en_us', 'zh_cn', 'zh_hk', 'zh_sc', 'zh_tw'), 0)

    for i, j, k in zip(language_dev, language_list, language_dev_num):
        i = os.path.join(phone_path, j)
        language_dev_num[j] = total_quantity('adb', 'txt', i)

    for i, j, k in zip(language_loc, language_list, language_loc_num):
        i = os.path.join(audio_path, project_path, j)
        language_loc_num[j] = total_quantity('local', 'txt', i)

    print("{str: <{len}}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}".format
          (language_dev_num['en_us'], language_loc_num['en_us'], language_dev_num['zh_cn'], language_loc_num['zh_cn'],
           language_dev_num['zh_hk'], language_loc_num['zh_hk'], language_dev_num['zh_sc'], language_loc_num['zh_sc'],
           language_dev_num['zh_tw'], language_loc_num['zh_tw'], len=lens, str='txt_num'))


def colon_change(colon_name, iplatform):
    try:
        if iplatform == '1':
            new_colon_name = colon_name.replace(":", "：")
            return new_colon_name
        elif iplatform == '2':
            new_colon_name = colon_name.replace("：", ":")
            return new_colon_name
    except:
        print('run.colon_change：error')

def change_colonFile():
    for lang in language_list:
        for wt in wavtype:
            for n in range(1, 5):
                local_path = os.path.join(audio_path, project_path, lang, wt+str(n))
                print('push %s ing...' % local_path)
                for dir_path, subpaths, files in os.walk(local_path, topdown=True):
                    for file in files:
                        local_file_path = os.path.join(dir_path, file)
                        device_file_path = os.path.join(phone_path, lang, wt + str(n))
                        if ":" in file:
                            small_colon = colon_change(local_file_path, '2')
                            big_colon = colon_change(local_file_path, '1')
                            runadb('mv %s %s' % (small_colon, big_colon))            # 重命名本地的文件未全角符号
                            runadb('adb push %s %s' % (big_colon, device_file_path))  # push到手机
                            device_file_path_detail1 = os.path.join(phone_path, lang, wt + str(n) + file)  # 获取手机的文件绝对路径
                            device_file_path_detail2 = colon_change(device_file_path_detail1, '2')  # 获取手机的文件绝对路径
                            runadb('adb shell rename %s %s' % (device_file_path_detail1, device_file_path_detail2))
                        else:
                            runadb('adb push %s %s' % (local_file_path, device_file_path))


def irun():
    print('====:: %s ::====' % project_path)
    if check_devces_file():       # 此方法用于检查手机是否存在audiowav文件夹，如无则运行create_android_dir();
        create_android_dir()      # 创建必须的文件夹
        # change_colonFile()      # 修改本地的冒号为全角冒号\\没能解决问题，较新的安卓系统无法使用半角冒号；
        push_file()               # push本地的wav文件和txt文件到手机;
        statistics_results_wav()  # push完成后，用于检查wav文件数量是否一致；
        statistics_results_txt()  # push完成后，用于检查txt文件数量是否一致；
    else:
        print('已退出~')
        quit()


if __name__ == "__main__":
    config = GetConfig.Config()  # 初始化配置文件以及数据
    irun()

