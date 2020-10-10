'''
@Author         : Sp4ce
@Date           : 2020-07-13 15:56:43
LastEditors    : Sp4ce
LastEditTime   : 2020-10-10 10:20:23
@Description    : Challenge Everything.
'''
import os
import shutil
import time
import datetime
import requests
from bs4 import BeautifulSoup


class IC_Decrypt:
    def __init__(self, options):
        self.sourceFolder = options.sourceFolder
        self.ez2uURL = options.ez2uURL
        self.reqHeader = options.reqHeader
        self.errorLogPath = options.errorLogPath
        self.dstFolder = options.dstFolder
        self.FileList = self.dstFolder + "\\FileList.txt"
        self.timeZone=options.timeZone
        self.reqTimeout=options.reqTimeout

    # Load Folders
    def get_all_path(self):
        if os.path.exists(self.FileList):
            pass
        else:
            postfix = set(['php'])  # 设置要记录的文件格式
            for maindir, subdir, file_name_list in os.walk(self.dstFolder):
                for filename in file_name_list:
                    apath = os.path.join(maindir, filename)
                    if True:  # 保存全部文件名。若要保留指定文件格式的文件名则注释该句
                        # 匹配后缀，只保存所选的文件格式。若要保存全部文件，则注释该句
                        if apath.split('.')[-1] in postfix:
                            try:
                                self.success('GET ' + str(apath))
                                with open(self.FileList, 'a+') as fo:
                                    fo.writelines(apath)
                                    fo.write('\n')
                            except:
                                pass  # 所有异常全部忽略即可

    # Load Files
    def decrypt_FilesList(self):
        self.success('Loading Need Decrpyt File List.')
        startTime = time.process_time()
        with open(self.FileList, 'r') as needDecryptFile:
            DecryptFileList = needDecryptFile.read().splitlines()
        endTime = time.process_time()
        self.success('Load {0} File(s) in {1} s, \nNow start Decrypt.'.format(
            len(DecryptFileList), endTime - startTime))
        return DecryptFileList

    # Decode_Files
    def decode_Files(self, DecryptFileList):
        for files in DecryptFileList:
            self.info('Load ' + files + ', filename ' + files.split("\\")[-1])
            file_content = open(files, 'rb+').read()
            if b'ionCube Loader' in file_content:
                file_name = files.split("\\")[-1]
                keyParam = (datetime.datetime.now() +
                            datetime.timedelta(hours=self.timeZone)).strftime("%H")
                file = {
                    str(keyParam) + '[]':
                    (file_name, file_content, 'application/octet-stream')
                }
                self.info("Upload " + files)
                try:
                    res = requests.post(self.ez2uURL,
                                        files=file,
                                        headers=self.reqHeader,
                                        timeout=self.reqTimeout)
                    if '403 Forbidden' not in res.text:
                        #print(res.content)
                        soup = BeautifulSoup(res.text, "lxml")
                        htmlATag = soup.select(
                            'div.container > div.alert.alert-success.fade.in > a'
                        )
                        if len(htmlATag) == 0:
                            self.errorLog(
                                '[!] File {0} maybe already decrypt'.format(
                                    files))
                        else:
                            self.success("Get received link " +
                                         htmlATag[0].string +
                                         " Downloading...")
                            res2 = requests.get(htmlATag[0].string,
                                                headers=self.reqHeader,
                                                timeout=self.reqTimeout)
                            with open(files, 'wb+') as df:
                                df.write(res2.content)
                    else:
                        self.errorLog(
                            '[!] Maybe Network Error? File {0} Decrypt FAILED 1'
                            .format(files))
                except:
                    self.errorLog(
                        '[!] Maybe Network Error? File {0} Decrypt FAILED 2'.
                        format(files))

    # Copy source dir to dest dir
    def copy_search_file(self, srcDir, desDir):
        self.info('Copy files to ' + desDir)
        if os.path.exists(self.FileList):
            pass
        else:
            if not os.path.isdir(desDir):
                os.makedirs(desDir)
            for files in os.listdir(srcDir):
                name = os.path.join(srcDir, files)
                back_name = os.path.join(desDir, files)
                if os.path.isfile(name):
                    shutil.copy(name, back_name)
                else:
                    if not os.path.isdir(back_name):
                        os.makedirs(back_name)
                    self.copy_search_file(name, back_name)

    # Log
    def errorLog(self, content):
        print(content)
        with open(self.errorLogPath, 'a+') as err:
            err.write('[' +
                      datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") +
                      '] ' + content + ' \n')

    def info(self, content):
        print('[' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") +
              '] [*] ' + content)

    def success(self, content):
        print('[' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") +
              '] [+] ' + content)

    # run
    def run(self):
        self.copy_search_file(self.sourceFolder, self.dstFolder)
        self.get_all_path()
        self.DecryptFileList = self.decrypt_FilesList()
        self.decode_Files(self.DecryptFileList)


if __name__ == '__main__':

    class options:
        sourceFolder = "" # need decode path
        dstFolder = '' # save path
        ez2uURL = 'https://easytoyou.eu/decoder/ic10php56/'
        reqHeader = {}
        reqHeader['Cookie'] = ''
        reqHeader['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'
        errorLogPath = dstFolder + 'error.log' # errorlog path
        timeZone=-7 #CN to EU 
        reqTimeout=20 #request timeout

    deIC = IC_Decrypt(options)
    deIC.run()
