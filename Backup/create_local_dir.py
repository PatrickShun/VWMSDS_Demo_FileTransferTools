import GetConfig
import subprocess
import os


config = GetConfig.Config()         # 初始化配置文件以及数据。
audio_path = config.audio_path      # 获取本地音频路径
project_path = config.project       # 获取需要push的项目
language_list = config.language_list  # 获取所有语言的列表
wavtype = config.wavtype            # 获取需要push的音频类型


def runadb(commend):  # 用于执行adb命令，只需要传入命令即可执行。
    ret = subprocess.Popen(commend, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
    ret.wait()
    if ret.returncode == 0:
        print('Success.', ret.stdout.read())
        return str(ret.returncode)
    else:
        print('error:', ret.stderr.read())


def create_local_dir():
    for lang in language_list:          # 语言
        for wy in wavtype:              # 音频类型
            for scenes in range(1, 5):  # 场景1234
                target_dir = os.path.join(audio_path, project_path, lang, (wy + str(scenes)))
                adb_command = 'mkdir -p ' + target_dir
                print(adb_command)
                runadb(adb_command)


if __name__ == "__main__":
    create_local_dir()
    print("创建完毕，请把音频文件移动到需要相应的位置！")
