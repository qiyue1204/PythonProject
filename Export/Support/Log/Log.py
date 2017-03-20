# coding=utf8

import sys
import time
import multiprocessing
import threading

#将日志打印到标准输出
def printLogToShell(Log, File = ''):
    sys.stdout.write(Log)
    if '' != File:
        file = open(File, 'a')
        file.writelines('[ ' + time.ctime() + ' ]' + Log)
        file.close

#将日志打印到日志文件
def printLogToFile(Log, File):
    file = open(File, 'a')
    file.writelines('[ ' + time.ctime() + ' ]' + Log)
    file.close

#处理到标准输出的日志
def OutputToShell(queue):
    while True:
        # lock.acquire()
        try:
            logInfo = queue.get()
        except Exception:
            pass
        sys.stdout.write(logInfo)
        # lock.release()

#处理到日志文件的日志        
def OutputToFile(queue, file):
    try:
        bufFile = open(file, 'a')
    except Exception as err:
        sys.stdout.write(err.__str__() + '\n')
        return False
    while True:
        # lock.acquire()
        try:
            logInfo = queue.get()
        except Exception:
            pass
        bufFile.writelines('[ ' + time.ctime() + ' ]' + logInfo)
        bufFile.flush()
        # lock.release()  
    
#地图日志处理
class LogManager():    
    def initLogFile(self, logFile):
        '''
            初始化或重新设置日志文件
        '''
        self.logFile = logFile
        
    def Start(self):
        '''
            运行日志处理对象
        '''
        # self.shellProcess = multiprocessing.Process( \
            # target = OutputToShell, args = (self.shellQueue, ))
        self.shellProcess = threading.Thread( \
            target = OutputToShell, args = (self.shellQueue, ))
        # self.fileProcess = multiprocessing.Process( \
            # target = OutputToFile, args = (self.fileQueue, self.logFile, ))
        self.fileProcess = threading.Thread( \
            target = OutputToFile, args = (self.fileQueue, self.logFile, ))
        self.shellProcess.daemon = True
        self.fileProcess.daemon = True
        
        self.shellProcess.start()
        self.fileProcess.start()
        # self.shellProcess.join()
        # self.fileProcess.join()
    
    def Stop(self):
        '''
            停止日志处理对象
        '''
        # try:
            # self.shellProcess.terminate() 
            # self.fileProcess.terminate()
        # except Exception as err:
            # print(err)
        
    def LogToShell(self, logInfo, fileFlag = False):
        '''
            日志打印到Shell，也可在输出到Shell的同时输出到日志文件
        '''
        self.shellQueueLock.acquire()
        self.shellQueue.put(logInfo)
        self.shellQueueLock.release()
        if True == fileFlag:
            self.fileQueueLock.acquire()
            self.fileQueue.put(logInfo)
            self.fileQueueLock.release()
    
    def LogToFile(self, logInfo):
        '''
            日志打印到日志文件
        '''
        self.fileQueueLock.acquire()
        self.fileQueue.put(logInfo)
        self.fileQueueLock.release()
    
    def __init__(self):
        self.logFile = ''
        self.queueSize = 1024
        self.shellQueue = multiprocessing.Queue(self.queueSize)
        self.fileQueue = multiprocessing.Queue(self.queueSize)
        self.shellQueueLock = multiprocessing.Lock()
        self.fileQueueLock = multiprocessing.Lock()
        self.shellProcess = ''
        self.fileProcess = ''
        
        
    def __init__(self, logFile):
        self.logFile = logFile
        self.queueSize = 1024
        self.shellQueue = multiprocessing.Queue(self.queueSize)
        self.fileQueue = multiprocessing.Queue(self.queueSize)
        self.shellQueueLock = multiprocessing.Lock()
        self.fileQueueLock = multiprocessing.Lock()
        self.shellProcess = ''
        self.fileProcess = ''
        

    def __del__(self):
        self.Stop()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    