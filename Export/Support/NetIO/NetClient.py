# coding=utf8

import socket
import threading
import NetBase

    
# 网络服务
class NetClient(NetBase.NetBase):           
    def StartNetClient(self):
        '''
            运行网络客户端
        '''
        #启动处理线程
        self.threadLock.acquire()
        thread = threading.Thread(target = NetBase.NetMaintainer, args = (self, ))
        self.threadList.append(thread)
        thread.daemon = True
        thread.start()
        self.threadLock.release()
    
    def StopNetClient(self):
        '''
            停止网络客户端
        '''
        try:
            self.linkLock.acquire()
            for linkInfo in self.linkList:
                self.DisConnect(linkInfo)
            self.linkLock.release()
        except socket.error as err:
            pass
        
    def Connect(self, server, port):
        '''
            连接
        '''
        try:
            socketTmp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error as err:
            self.logObj.LogToFile(err.__str__() + '\n')
            self.logObj.LogToFile('Start net client failed!\n')
            return None
        
        try:
            socketTmp.connect((server, port))
            if(self.netTimeout > 0):
                socketTmp.settimeout(self.netTimeout)
        except socket.error as err:
            self.logObj.LogToFile(err.__str__() + '\n')
            self.logObj.LogToFile('socket ' + socketTmp.__str__() + ' connected to ' + \
                server.__str__() + ':' + port.__str__() + ' failed!\n')
            return None
    
        self.linkLock.acquire()
        linkInfo = [socketTmp, (server, port), True]
        self.linkList.append(linkInfo)
        self.linkLock.release()
        return linkInfo
    
    def __init__(self, logObj, hbInterval, netTimeout = 0):
        NetBase.NetBase.__init__(self, logObj, hbInterval)
        self.netTimeout = netTimeout

    def __del__(self):
        self.StopNetClient()
    

    