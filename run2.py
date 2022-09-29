# coding:utf-8
import os
import subprocess
import GetConfig

config = GetConfig.Config()  # 初始化配置文件以及数据。
audio_path = config.audio_path  # 获取本地音频路径
devices_path = config.device_path  # 获取手机目标路径
project_path = config.project  # 获取需要push的项目
language_list = config.language_list  # 获取所有语言的列表
wavtype = config.wavtype  # 获取需要push的音频类型
txttype = config.txttype  # 获取需要push的txt类型
scenes = config.scenes  # 获取需要push的场景


def runadb(commend):
    print(str(commend))
    ret = subprocess.run(commend, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
    if ret.returncode == 0:
        print('Success.', ret.returncode)
        return str(ret.returncode)
    else:
        print('Error:', ret.stderr)


def create_android_dir():
    runadb('adb shell mkdir -p /sdcard/audiowav/')
    for lang in language_list:  # 语言
        for wy in wavtype:  # 音频类型
            for sc in scenes:  # 场景1234
                target_dir = os.path.join(devices_path, lang, (wy + sc[-1]))
                adb_command = 'adb shell mkdir -p ' + target_dir
                runadb(adb_command)


def push_file():
    for lang in language_list:
        for wt in wavtype:
            for sc in scenes:
                local_dir = os.path.join(audio_path, project_path, lang, wt + sc[-1])
                phone_dir = os.path.join(devices_path, lang, wt + sc[-1])
                push_wav_command = 'adb push %s/*.wav %s' % (local_dir, phone_dir)
                runadb(push_wav_command)
                local_sum = total_quantity('other', 'wav', local_dir)
                print('本地音频路径%s,文件数：%s' % (local_dir, local_sum))
                phone_sum = total_quantity('adb', 'wav', phone_dir)
                print('手机音频路径%s,文件数：%s' % (phone_dir, phone_sum))
                if phone_sum == 0 or local_sum == 0:
                    print("ERROR, 本地路径没有文件！\n")
                elif phone_sum >= 1 and phone_sum == local_sum:
                    print("Done, Push完成，数量正确！\n")
                else:
                    print("！！！本地文件和手机文件的数量不一致，请检查！！！\n")
        # push txt
        local_txt_dir = os.path.join(audio_path, project_path, lang)
        phone_txt_dir = os.path.join(devices_path, lang)
        push_txt_command = 'adb push %s/*.txt %s' % (local_txt_dir, phone_txt_dir)
        runadb(push_txt_command)
        local_txt_sum = total_quantity('other', 'txt', local_txt_dir)
        print('本地文本路径%s,文件数：%s' % (local_txt_dir, local_txt_sum))
        phone_txt_sum = total_quantity('adb', 'txt', phone_txt_dir)
        print('手机文本路径%s,文件数：%s' % (phone_txt_dir, phone_txt_sum))
        if phone_txt_sum == 0 or local_txt_sum == 0:
            print("ERROR, 本地路径没有txt文件！\n")
        elif phone_txt_sum >= 1 and phone_txt_sum == local_txt_sum:
            print("Done, Push完成，txt文件数量正确！\n")
        else:
            print("！！！本地文件和手机文件的数量不一致，请检查！！！\n")


def total_quantity(comm_type, filetype, total_path):
    if comm_type == 'adb':
        ad = 'adb shell '
    else:
        ad = ''
    total_command = '%sls -l %s | grep "^-" | grep -c "%s$"' % (ad, total_path, filetype)
    ret = subprocess.Popen(total_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='UTF-8')
    ret.wait()
    numb = int(ret.stdout.read())
    return numb


def statistics_results_wav():
    lens = 12
    titles = ['en_dev', 'en_loc', 'cn_dev', 'cn_loc', 'hk_dev', 'hk_loc', 'sc_dev', 'sc_loc', 'tw_dev', 'tw_loc']
    print('{str: <{len}}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}'.format(titles[0], titles[1], titles[2], titles[3],
                                                                         titles[4], titles[5], titles[6], titles[7],
                                                                         titles[8], titles[9], len=lens,
                                                                         str='Audio_type_wav'))
    language_dev_num = dict.fromkeys(('en_us', 'zh_cn', 'zh_hk', 'zh_sc', 'zh_tw',), 0)
    language_loc_num = dict.fromkeys(('en_us', 'zh_cn', 'zh_hk', 'zh_sc', 'zh_tw',), 0)
    for wt in wavtype:
        for i in scenes:
            for lang in language_list:
                dev_path = os.path.join(devices_path, lang, wt + i[-1])
                loc_path = os.path.join(audio_path, project_path, lang, wt + i[-1])
                language_dev_num[lang] = total_quantity('adb', 'wav', dev_path)
                language_loc_num[lang] = total_quantity('local', 'wav', loc_path)
            print("{str: <{len}}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}".format
                  (language_dev_num['en_us'], language_loc_num['en_us'], language_dev_num['zh_cn'],
                   language_loc_num['zh_cn'], language_dev_num['zh_hk'], language_loc_num['zh_hk'],
                   language_dev_num['zh_sc'], language_loc_num['zh_sc'], language_dev_num['zh_tw'],
                   language_loc_num['zh_tw'], len=lens, str=wt + i[-1]))


def statistics_results_txt():
    lens = 12
    titles = ['en_dev', 'en_loc', 'cn_dev', 'cn_loc', 'hk_dev', 'hk_loc', 'sc_dev', 'sc_loc', 'tw_dev', 'tw_loc']
    print('{str: <{len}}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}'.format
          (titles[0], titles[1], titles[2], titles[3], titles[4], titles[5],
           titles[6], titles[7], titles[8], titles[9], len=lens, str='Test_txt'))
    language_dev = dict.fromkeys(('en_us', 'zh_cn', 'zh_hk', 'zh_sc', 'zh_tw'), 'null')
    language_loc = dict.fromkeys(('en_us', 'zh_cn', 'zh_hk', 'zh_sc', 'zh_tw'), 'null')
    language_dev_num = dict.fromkeys(('en_us', 'zh_cn', 'zh_hk', 'zh_sc', 'zh_tw'), 0)
    language_loc_num = dict.fromkeys(('en_us', 'zh_cn', 'zh_hk', 'zh_sc', 'zh_tw'), 0)
    for i, j, k in zip(language_dev, language_list, language_dev_num):
        i = os.path.join(devices_path, j)
        language_dev_num[j] = total_quantity('adb', 'txt', i)
    for i, j, k in zip(language_loc, language_list, language_loc_num):
        i = os.path.join(audio_path, project_path, j)
        language_loc_num[j] = total_quantity('local', 'txt', i)
    print("{str: <{len}}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}".format
          (language_dev_num['en_us'], language_loc_num['en_us'], language_dev_num['zh_cn'], language_loc_num['zh_cn'],
           language_dev_num['zh_hk'], language_loc_num['zh_hk'], language_dev_num['zh_sc'], language_loc_num['zh_sc'],
           language_dev_num['zh_tw'], language_loc_num['zh_tw'], len=lens, str='txt_num'))


def irun():
    i = input('是否继续？(Y/n)')
    if i == 'Y':
        create_android_dir()        # 创建必须的文件夹
        push_file()                 # push本地的wav文件和txt文件到手机;
        statistics_results_wav()    # push完成后，用于检查wav文件数量是否一致；
        statistics_results_txt()    # push完成后，用于检查txt文件数量是否一致；
    else:
        print('已退出~')
        quit()


if __name__ == "__main__":
    config = GetConfig.Config()  # 初始化配置文件以及数据
    irun()
