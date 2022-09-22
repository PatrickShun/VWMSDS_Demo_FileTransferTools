#! /usr/bin/env python
# 用于Push 文件到Android手机
import os
import subprocess
import GetConfig
from time import sleep

config = GetConfig.Config()  # 初始化配置文件以及数据。
audio_path = config.audio_path  # 获取本地音频路径
project_path = config.project  # 获取需要push的项目
phone_path = config.phonepath  # 获取目标音频路径
language_list = config.language_list  # 获取所有语言的列表
wavtype = config.wavtype  # 获取需要push的音频类型
changjing = ['场景1', '场景2', '场景3', '场景4']


def runadb(commend):  # 用于执行adb命令，只需要传入命令即可执行。
    print(commend)
    sleep(0.2)
    # ret = subprocess.Popen(commend, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
    # ret.wait()
    ret = subprocess.run(commend, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8',
                         timeout=59)
    if ret.returncode == 0:
        print('Success.')
        return str(ret.returncode)
    else:
        print('Error:', ret.stderr)


def check_devces_file():  # 判断sdcard/目录下有没有audiowav目录, 如果没有则新创建
    files = subprocess.getoutput('adb shell ls /sdcard/')
    if 'audiowav' in str(files):
        print('有audiowav文件夹')
    else:
        print('无audiowav文件夹')
        i = input('是否新创建文件夹？(Y/n)')
        if i == 'Y':
            create_android_dir()
            print('Done!')
        else:
            print('已退出...')


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
                # adbpush_wav = 'adb push ' + local_tar_dir + '/*.wav ' + '/sdcard/audiowav/'+lang+'/'+wt+str(scenes)
                adbpush_wav = 'adb push %s/*.wav %s' % (local_dir, phone_dir)
                # print(adbpush_wav)
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

        local_txt_dir = os.path.join(audio_path, project_path, lang)
        phone_txt_dir = os.path.join(phone_path, lang)
        # adbpush_txt = 'adb push ' + local_txt_dir + '/*.txt ' + '/sdcard/audiowav/' + lang
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
    # total_quantity = adb or '' 用于区分统计手机的还是本地的
    # filetype = wav or txt
    # total_path = eg:/sdcard/audiowav/en_us/hotword1
    if comm_type == 'adb':
        ad = 'adb shell '
    else:
        ad = ''
    adbcomm = '%sls -l %s | grep "^-" | grep -c "%s$"' % (ad, total_path, filetype)
    ret = subprocess.Popen(adbcomm, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
    ret.wait()
    numb = int(ret.stdout.read())
    return numb


def statistics_results_wav():
    # 1.格式化打印出文件夹的文件数：
    lens = 12  # 设定列间距;
    # 打印标题:('\t'是横向格式化符, 'len'参数用于设定str列的间距,'str'参数用于设定标题, 主要用于解决标题过长的问题.)
    titles = ['en_dev', 'en_loc', 'cn_dev', 'cn_loc', 'hk_dev', 'hk_loc', 'sc_dev', 'sc_loc']
    print('{str: <{len}}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}'.format(titles[0], titles[1], titles[2], titles[3], titles[4],
                                                                 titles[5], titles[6], titles[7], len=lens,
                                                                 str='Audio_type_wav'))

    # 2.打印各个文件夹下的文件数值;
    seq = dict.fromkeys(('en_dev', 'en_loc', 'cn_dev', 'cn_loc', 'hk_dev', 'hk_loc', 'sc_dev', 'sc_loc'), 0)
    for wt in wavtype:
        for scenes in range(1, 5):
            en_dev_dir = os.path.join(phone_path, language_list[0], wt + str(scenes))
            cn_dev_dir = os.path.join(phone_path, language_list[1], wt + str(scenes))
            hk_dev_dir = os.path.join(phone_path, language_list[2], wt + str(scenes))
            sc_dev_dir = os.path.join(phone_path, language_list[3], wt + str(scenes))

            en_loc_dir = os.path.join(audio_path, project_path, language_list[0], wt + str(scenes))
            cn_loc_dir = os.path.join(audio_path, project_path, language_list[1], wt + str(scenes))
            hk_loc_dir = os.path.join(audio_path, project_path, language_list[2], wt + str(scenes))
            sc_loc_dir = os.path.join(audio_path, project_path, language_list[3], wt + str(scenes))

            seq['en_dev'] = total_quantity('adb', 'wav', en_dev_dir)
            seq['cn_dev'] = total_quantity('adb', 'wav', cn_dev_dir)
            seq['hk_dev'] = total_quantity('adb', 'wav', hk_dev_dir)
            seq['sc_dev'] = total_quantity('adb', 'wav', sc_dev_dir)

            seq['en_loc'] = total_quantity('', 'wav', en_loc_dir)
            seq['cn_loc'] = total_quantity('', 'wav', cn_loc_dir)
            seq['hk_loc'] = total_quantity('', 'wav', hk_loc_dir)
            seq['sc_loc'] = total_quantity('', 'wav', sc_loc_dir)

            title = wt + str(scenes)

            print("{str: <{len}}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}".format(seq['en_dev'], seq['en_loc'], seq['cn_dev'],
                                                                         seq['cn_loc'], seq['hk_dev'], seq['hk_loc'],
                                                                         seq['sc_dev'], seq['sc_loc'], len=lens,
                                                                         str=title))


def statistics_results_txt():
    lens = 12  # 设定列间距;
    titles = ['en_dev', 'en_loc', 'cn_dev', 'cn_loc', 'hk_dev', 'hk_loc', 'sc_dev', 'sc_loc']
    print('{str: <{len}}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}'.format(titles[0], titles[1], titles[2], titles[3], titles[4],
                                                                 titles[5], titles[6], titles[7], len=lens,
                                                                 str='Test_txt'))
    seq = dict.fromkeys(('en_dev', 'en_loc', 'cn_dev', 'cn_loc', 'hk_dev', 'hk_loc', 'sc_dev', 'sc_loc'), 0)
    language_dev = dict.fromkeys(('en_dev_dir', 'cn_dev_dir', 'hk_dev_dir', 'sc_dev_dir'),'0')
    language_dev_num = dict.fromkeys(('en_dev_dir', 'cn_dev_dir', 'hk_dev_dir', 'sc_dev_dir'), 0)

    print(language_dev)
    for i, j, k in zip(language_dev, language_list, language_dev_num):
        i = os.path.join(phone_path, j)
        k = total_quantity('adb', 'txt', i)
        print(k)
        
    # en_dev_dir = os.path.join(phone_path, language_list[0])
    # cn_dev_dir = os.path.join(phone_path, language_list[1])
    # hk_dev_dir = os.path.join(phone_path, language_list[2])
    # sc_dev_dir = os.path.join(phone_path, language_list[3])
    #
    # en_loc_dir = os.path.join(audio_path, project_path, language_list[0])
    # cn_loc_dir = os.path.join(audio_path, project_path, language_list[1])
    # hk_loc_dir = os.path.join(audio_path, project_path, language_list[2])
    # sc_loc_dir = os.path.join(audio_path, project_path, language_list[3])
    #
    # seq['en_dev'] = total_quantity('adb', 'txt', en_dev_dir)
    # seq['cn_dev'] = total_quantity('adb', 'txt', cn_dev_dir)
    # seq['hk_dev'] = total_quantity('adb', 'txt', hk_dev_dir)
    # seq['sc_dev'] = total_quantity('adb', 'txt', sc_dev_dir)
    #
    # seq['en_loc'] = total_quantity('', 'txt', en_loc_dir)
    # seq['cn_loc'] = total_quantity('', 'txt', cn_loc_dir)
    # seq['hk_loc'] = total_quantity('', 'txt', hk_loc_dir)
    # seq['sc_loc'] = total_quantity('', 'txt', sc_loc_dir)
    #
    # print("{str: <{len}}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}".format(seq['en_dev'], seq['en_loc'], seq['cn_dev'],
    #                                                              seq['cn_loc'], seq['hk_dev'], seq['hk_loc'],
    #                                                              seq['sc_dev'], seq['sc_loc'], len=lens, str='txt_num'))
    #

def irun():
    # check_devces_file()         # 此方法用于检查手机是否存在audiowav文件夹，如无则运行create_android_dir();
    # push_file()                 # push本地的wav文件和txt文件到手机;
    # statistics_results_wav()    # push完成后，用于检查wav文件数量是否一致；
    statistics_results_txt()  # push完成后，用于检查txt文件数量是否一致；


if __name__ == "__main__":
    # config = GetConfig.Config()  # 初始化配置文件以及数据
    irun()
