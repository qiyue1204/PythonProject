# coding=utf8

from datetime import datetime
from ftplib import FTP
import Log
import Conf
import time
import sys
import os
import string

# recvTmp = open('Recive/1.txt', 'ab')
# def RecvFromFTP(block):
    # recvTmp.write(block)

#记录FTP目录下信息
ftpFileList = []
    
def LoginFTP(ftpServer, ftpLogin, ftpPWD):
    ftpObj = FTP(ftpServer)
    try:
        if '' == ftpLogin:
            ftpObj.login(ftpLogin, ftpPWD)
        else:
            ftpObj.login()
        return ftpObj
    except Exception as err:
        Log.printLogToShell('[ ERROR ] LoginFTP with user ' + ftpLogin + ' error!\n', logFile)
        Log.printLogToFile(err.__str__() + '\n', logFile)
        return ''

def LogoutFTP(ftpObj):
    try:
        ftpObj.quit()
    except Exception as err:
        pass

def GetFTPEachFile(strLine):
    tmpList = strLine.split(' ')
    fileName = tmpList[tmpList.__len__() - 1]
    ftpFileList.append(fileName)
        
def GetFTPFileList(ftpObj):
    ftpObj.retrlines('LIST', GetFTPEachFile)
    return ftpFileList
    
def GetTimeStringByReserve(timeNow, dayReserve):
    day = timeNow.day - dayReserve
    month = timeNow.month
    year = timeNow.year
    #跨月
    if (day <= 0):
        #前一个月有31天
        if timeNow.month == 2 or timeNow.month == 4 or timeNow.month == 6 or \
            timeNow.month == 8 or timeNow.month == 9 or timeNow.month == 11:
            day = timeNow.day + 31 - dayReserve
            month = month - 1
        #前一个月有30天
        elif timeNow.month == 5 or timeNow.month == 7 or timeNow.month == 10 or \
            timeNow.month == 12:
            day = timeNow.day + 30 - dayReserve
            month = month - 1
        #前一个月有29天
        elif timeNow.month == 3 and \
            (((0 == year % 100) and (0 == year % 400)) or ((0 != year % 100) and (0 == year % 4))):
            day = timeNow.day + 29 - dayReserve
            month = month - 1
        #前一个月有28天
        elif timeNow.month == 3:
            day = timeNow.day + 28 - dayReserve
            month = month - 1
        #跨年
        else:
            day = timeNow.day + 31 - dayReserve
            month = 12
            year = year - 1
        
    dateString = "%04d"%(year) + "%02d"%(month) + "%02d"%(day)
    return dateString

# 获取最大日期文件夹
def GetLatestDate(list):
    if([] == list):
        return ''
    min = string.atoi(list[0])
    for date in list:
        if min < string.atoi(date):
            min = string.atoi(date)
    return min.__str__()
    
#判断sourceFile代表的日期是否晚于targetFileList中最晚的日期
def JudgeNeedTransfer(sourceFile, targetFileList):
    tmpFileList = targetFileList
    if '.' in tmpFileList:
        tmpFileList.remove('.')
    if '..' in tmpFileList:
        tmpFileList.remove('..')
    fileLatest = GetLatestDate(tmpFileList)
    if '' == fileLatest:
        return True
    if fileLatest >= sourceFile:
        return False
    else:
        return True
    
    
if __name__ == '__main__':
    #参数
    logFile = Conf.logFile
    ftpServer = Conf.ftpServer
    ftpLogin = Conf.ftpLogin
    ftpPWD = Conf.ftpPWD
    sourceDataPath = Conf.sourceDataPath
    secondaryDirList = Conf.secondaryDirList
    targetDataPath = Conf.targetDataPath
    transferInterval = Conf.transferInterval
    checkInterval = Conf.checkInterval
    dayReserve = Conf.dayReserve
    
    timeLastCheck = datetime.now()
    
    Log.printLogToShell('Server started!\n', logFile)
    while True:
        
        Log.printLogToShell(time.ctime() + '\n')
        
        timeLastCheck = datetime.now()
        dateString = GetTimeStringByReserve(timeLastCheck, dayReserve)
        # dateString = "%04d"%(timeLastCheck.year) + "%02d"%(timeLastCheck.month) + "%02d"%(timeLastCheck.day - dayReserve)
        
        for dir1 in secondaryDirList:
            eachSourceDir = sourceDataPath + dir1
            eachTargetDir = targetDataPath + dir1
            #登录ftp
            ftpObj = LoginFTP(ftpServer, ftpLogin, ftpPWD)
            if('' == ftpObj):
                sys.exit(1)
            
            #更换ftp目录
            ftpObj.cwd(eachTargetDir)
            
            #读取FTP上该目录下已经存在的目录
            del ftpFileList[:]
            targetFileList = GetFTPFileList(ftpObj)
            LogoutFTP(ftpObj)
            
            #读取该类本地文件夹
            dirList = os.listdir(eachSourceDir)
            for dir2 in dirList:
                #挨个范围内的判断是否要转储（可能存在问题，如果中断，不能判断该天下的是否已全部转储）
                #存在满足条件的
                # if string.atoi(dir2) <= string.atoi(dateString) and not (dir2 in targetFileList):
                if string.atoi(dir2) <= string.atoi(dateString) and JudgeNeedTransfer(dir2, targetFileList):
                    #登录ftp
                    ftpObj = LoginFTP(ftpServer, ftpLogin, ftpPWD)
                    ftpObj.cwd(eachTargetDir)
                    ftpObj.mkd(dir2)
                    ftpObj.cwd(dir2)
                    dirDay = ''
                    if eachSourceDir[eachSourceDir.__len__() - 1] != '/':
                        dirDay = eachSourceDir + '/' + dir2
                    else:
                        dirDay = eachSourceDir + dir2
                    #获取本地每日下文件信息
                    fileList = os.listdir(dirDay)
                    #依次传输
                    for eachFile in fileList:
                        fileTmp = open(dirDay + '/' + eachFile, 'rb')
                        result = ''
                        try:
                            result = ftpObj.storbinary('STOR ' + eachFile, fileTmp)
                        except Exception as err:
                            #传输失败重试一次
                            if not ('complete' in result):
                                LogoutFTP(ftpObj)
                                ftpObj = LoginFTP(ftpServer, ftpLogin, ftpPWD)
                                ftpObj.cwd(eachTargetDir)
                                ftpObj.cwd(dir2)
                                result = ftpObj.storbinary('STOR ' + eachFile, fileTmp)
                                if not ('complete' in result):
                                    Log.printLogToShell('[ ERROR ] Transfer file ' + dirDay + '/' + eachFile + ' failed!\n', logFile)
                                    LogoutFTP(ftpObj)
                                    ftpObj = LoginFTP(ftpServer, ftpLogin, ftpPWD)
                                    ftpObj.cwd(eachTargetDir)
                                    ftpObj.cwd(dir2)
                                    fileTmp.close()
                                    continue
                            else:
                                Log.printLogToShell('[ ERROR ] Transfer file ' + dirDay + '/' + eachFile + ' failed!\n', logFile)
                                continue
                        Log.printLogToShell('Transfer file ' + dirDay + '/' + eachFile + ' completed!\n', logFile)
                        #一个文件传输完成休息
                        fileTmp.close()
                        time.sleep(transferInterval)
                    #登出ftp
                    LogoutFTP(ftpObj)

        time.sleep(checkInterval)
                       
    











