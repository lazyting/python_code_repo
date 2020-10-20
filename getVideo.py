"""
@author : lazyting
@time : 2020-10-20
@desc : 根据.m3u8文件下载ts文件，然后再合并成为MP4文件
"""
import requests
import threading
import os

count = 0;
urlPrefix = '';
cwd = os.getcwd() + "/"  # 获取当前目录即dir目录下
m3u8FilePath = None;
headers = {'Origin': 'https://xdzy.andisk.com', 'Referer': 'https://xdzy.andisk.com/andisk/app/videoviewFrame.html',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}


def Handler(url, index):
    r = requests.get(url, headers=headers, stream=True)
    with open(cwd + "/" + str(index) + ".ts", "wb") as code:
        code.write(r.content)


def download_file():
    f = open(m3u8FilePath, 'r', encoding='utf-8')
    text_list = f.readlines()
    s_list = []
    for i in text_list:
        if i.find('#EX') == -1:
            s_list.append(str(urlPrefix) + str(i).replace("\n", ''))
    f.close()
    for i in range(len(s_list)):
        t = threading.Thread(target=Handler, kwargs={'url': s_list[i], 'index': i})
        t.setDaemon(True)
        t.start()

    # 等待所有线程下载完成
    main_thread = threading.current_thread()
    for t in threading.enumerate():
        if t is main_thread:
            continue
        t.join()


def before_merge():
    f = open(m3u8FilePath, 'r', encoding='utf-8')
    text_list = f.readlines()
    files = []
    for i in text_list:
        if i.find('#EX') == -1:
            files.append(i)
    f.close()
    tmp = []
    for i in range(len(files)):
        tmp.append(str(i) + '.ts ')
        # 合并ts文件
    shell_str = '+'.join(tmp)
    shell_str = 'copy /b ' + shell_str + ' video.mp4' + '\n' + 'del *.ts'
    return shell_str


def wite_to_file(cmdString):
    f = open("combined.cmd", 'w')
    f.write(cmdString)
    f.close()


def getPrefix(url):
    global urlPrefix
    urlPrefix = url[0:url.rfind('/') + 1]


def getM3U8File(url):
    global m3u8FilePath
    r = requests.get(url, headers=headers, stream=True)
    m3u8FilePath = cwd + '/video.m3u8'
    with open(m3u8FilePath, "wb") as file:
        file.write(r.content)


if __name__ == '__main__':
    # 下载：开始下载
    print("输入.m3u8地址")
    url = input()
    if url:
        getPrefix(url)
    if urlPrefix:
        cwd = os.getcwd()  # 获取当前目录即dir目录下
        getM3U8File(url)
        download_file()
        # # 结束下载
        # #合并小文件
        cmd = before_merge();
        # #把合并命令写到文件中
        wite_to_file(cmd);
    else:
        print('地址前缀错误，请重新执行')
