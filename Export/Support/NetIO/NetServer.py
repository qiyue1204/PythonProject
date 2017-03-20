# coding=utf8

import socket
import threading
import ctypes
import NetBase


#处理线程
def NetServerWorker(netServer, linkInfo):
    dataBuf = ctypes.create_string_buffer('\0', 65535)
    
    while True:
        #获取数据包
        netHeader = netServer.RecvData(linkInfo, dataBuf)
        if None == netHeader:
            break
        if True == netServer.CheckHBPackage(linkInfo, netHeader):
            continue

# 网络服务监听
def NetServerListener(netServer, worker):
    while True:
        try:
            sktAccept = netServer.socketMain.accept()
        except socket.error as err:
            netServer.logObj.LogToFile(err.__str__() + '\n')
            continue
        
        #创建一个线程来处理
        netServer.linkLock.acquire()
        bufIO = ctypes.create_string_buffer('\0', 65535)
        linkInfo = [sktAccept[0], sktAccept[1], True]
        netServer.linkList.append(linkInfo)
        netServer.linkLock.release()
        netServer.threadLock.acquire()
        thread = threading.Thread(target = worker, args = (netServer, linkInfo, ))
        netServer.threadList.append(thread)
        thread.daemon = True
        thread.start()
        netServer.threadLock.release()
        netServer.logObj.LogToFile('Built a connector on ' + sktAccept[1].__str__()+ '!\n')
        print(thread)
    
# 网络服务
class NetServer(NetBase.NetBase):       
    def InitNetServer(self, concurrentNum, port):
        '''
            初始化网络服务，参数为连接并发数、心跳时长、端口号
        '''
        self.concurrentNum = concurrentNum
        self.port = port
    
    def StartNetServer(self, worker):
        '''
            运行网络服务
        '''
        try:
            self.socketMain = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socketMain.bind(('', self.port))
            self.socketMain.listen(5)
        except socket.error as err:
            self.logObj.LogToFile(err.__str__() + '\n')
            self.logObj.LogToFile('Start net server failed!\n')
            return None
        
        #启动处理线程
        self.threadLock.acquire()
        if(None == worker):
            worker = NetServerWorker
        thread = threading.Thread(target = NetServerListener, args = (self, worker))
        self.threadList.append(thread)
        thread.daemon = True
        thread.start()
        thread = threading.Thread(target = NetBase.NetMaintainer, args = (self, ))
        self.threadList.append(thread)
        thread.daemon = True
        thread.start()
        self.threadLock.release()
    
    def StopNetServer(self):
        '''
            停止网络服务
        '''
        try:
            self.socketMain.close()
            self.linkLock.acquire()
            for linkInfo in self.linkList:
                self.DisConnect(linkInfo)
            self.linkLock.release()
        except socket.error as err:
            pass
    
    def __init__(self, logObj, hbInterval):
        NetBase.NetBase.__init__(self, logObj, hbInterval)
        #参数
        self.concurrentNum = 0
        self.port = 0
        #连接对象
        self.socketMain = 0

    def __del__(self):
        self.StopNetServer()
    

    