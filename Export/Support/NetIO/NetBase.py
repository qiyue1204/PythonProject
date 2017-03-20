# coding=utf8

import socket
import time
import multiprocessing
import struct
import ctypes
import hashlib  #进行hash加密的模块
from NetCommand import *
        
# 网络状态维护
def NetMaintainer(netServer):
    while True:
        time.sleep(netServer.HBInterval / 2)

        #维护链表
        netServer.linkLock.acquire()
        for each in netServer.linkList:
            if True != each[2]:
                netServer.linkList.remove(each)
                continue
            #本端发心跳
            netServer.HBRequest(each)
        netServer.linkLock.release()
    
# 网络服务
class NetBase():       
    def SendData(self, linkInfo, strSendBuf):
        '''
            发送数据，在SendData外打包
        '''
        try:
            linkInfo[0].send(strSendBuf)
        except socket.error as err:
            self.logObj.LogToFile(err.__str__() + '\n')
            self.logObj.LogToFile('Send data from socket ' + linkInfo[0].__str__() + ' failed!\n')
            self.DisConnect(linkInfo)
            return False
            
        return True
        
    def RecvData(self, linkInfo, recvBuf):
        '''
            接收一个整包，数据体存入strRecvBuf，返回包头，包头不经过字节序转换
        '''
        #接收包头，解析完整数据长度
        try:
            netHeader = linkInfo[0].recv(24)
        except socket.error as err:
            self.logObj.LogToFile(err.__str__() + '\n')
            self.logObj.LogToFile('Recv data from socket ' + linkInfo[0].__str__() + ' failed!\n')
            self.DisConnect(linkInfo)
            return None

        if(0 == netHeader.__len__()):
            return None
			
        #读数据长度
        netHeaderInfo = struct.unpack('HHIHHIhhI', netHeader)
        dataLength = socket.ntohs(netHeaderInfo[0]) - 22
        
        if dataLength <= 0:
            return netHeader

        tmpBuf = ''
        dataLengthTmp = dataLength
        while True:
            try:
                netData = linkInfo[0].recv(dataLengthTmp)
                if netData.__len__() == dataLengthTmp:
                    tmpBuf += netData
                    break
                else:
                    tmpBuf += netData
                    dataLengthTmp -= netData.__len__()
            except socket.error as err:
                self.logObj.LogToFile(err.__str__() + '\n')
                self.logObj.LogToFile('Recv data from socket ' + linkInfo[0].__str__() + ' failed!\n')
                self.DisConnect(linkInfo)
                return None
        
        ctypes.memmove(recvBuf, tmpBuf, tmpBuf.__len__())
        return netHeader
    
    def DisConnect(self, linkInfo):
        '''
            断开连接
        '''
        try:
            linkInfo[0].close()
            self.logObj.LogToFile('Socket ' + linkInfo[0].__str__() + ' closed successfully!\n')
        except socket.error as err:
            self.logObj.LogToFile(err.__str__() + '\n')
            self.logObj.LogToFile('Socket ' + linkInfo[0].__str__() + ' closed failed!\n')
            return None
        
        linkInfo[2] = False
        self.logObj.LogToFile(linkInfo[0].__str__() + linkInfo[1].__str__() + ' closed!\n')
    
    def HBRequest(self, linkInfo):
        '''
            主动发送心跳包
        '''
        hbHeader = struct.pack('HHIHHIhhI', socket.htons(22), 0, 0, socket.htons(mainCmd), \
            socket.htons(hbCmdRequest), 0, 0, 0, 0)
        try:
            linkInfo[0].send(hbHeader)
        except socket.error as err:
            self.logObj.LogToFile(err.__str__() + ' send HBRequest failed!\n')
            self.DisConnect(linkInfo)
            return False
        return True
            
    def HBResponse(self, linkInfo):
        '''
            应答心跳包
        '''
        hbHeader = struct.pack('HHIHHIhhI', socket.htons(22), 0, 0, socket.htons(mainCmd), \
            socket.htons(hbCmdResponse), 0, 0, 0, 0)
        try:
            linkInfo[0].send(hbHeader)
        except socket.error as err:
            self.logObj.LogToFile(err.__str__() + ' send HBResponse failed!\n')
            self.DisConnect(linkInfo)
            return False
        return True
            
    def CheckHBPackage(self, linkInfo, netHeader):
        '''
            检查是否心跳包
        '''
        if(None == netHeader):
            return False
        netHeaderInfo = struct.unpack('HHIHHIhhI', netHeader)
        subCmd = socket.ntohs(netHeaderInfo[4])
        if subCmd == hbCmdRequest:
            self.HBResponse(linkInfo)
            return True
        if subCmd == hbCmdResponse:
           return True 
        return False
    
    def SendHook(self, linkInfo):
        '''
            发送Hook（客户端主动，服务端被动）
        '''
        # UINT32_T	    ui32Random1;
        # CHAR_T  	    pchLocalIP[IPV4STRLENGTH];
        # UINT32_T	    tstCurrentTime;
        # CHAR_T     	pchRemoteIP[IPV4STRLENGTH];
        # UINT32_T	    ui32Random2;
        # CHAR_T     	pchMD5[IPV4STRLENGTH];
        #Hook内容打包
        hookBuf = ctypes.create_string_buffer('\0', 84)
        md516 = hashlib.new('md5', '123127.127.127.127123127.127.127.127123').digest()
        hookHeader = struct.pack('HHIHHIhhI', socket.htons(82), 0, 0, \
            socket.htons(mainCmd), socket.htons(hookSubCmd), 0, \
            socket.htons(serverReserve), 0, 0)
        hookStruct = struct.Struct('24s')
        hookStruct.pack_into(hookBuf, 0, hookHeader)
        hookStruct.__init__('I16sI16sI16s')
        hookStruct.pack_into(hookBuf, 24, socket.htonl(123), '127.127.127.127', \
            socket.htonl(123), '127.127.127.127', socket.htonl(123), md516)
        if True == self.SendData(linkInfo, hookBuf.raw):
            self.logObj.LogToFile('Send hook successfully.\n')
            return True
        self.logObj.LogToFile('Send hook failed.\n')
        return False
        
    def CheckLinkHook(self, linkInfo, netHeader):
        '''
            检查数据包是否Hook
        '''
        if(None == netHeader):
            return False
        netHeaderInfo = struct.unpack('HHIHHIhhI', netHeader)
        subCmd = socket.ntohs(netHeaderInfo[4])
        if subCmd == hookSubCmd:
            return True
        return False
    
    def __init__(self, logObj, netHBInterval):
        self.logObj = logObj
        #参数
        self.HBInterval = netHBInterval
        #连接对象
        self.linkList = []      #每个值为[socket, linkInfo, status]的值
        self.linkBufList = []       #连接的buf空间，用于接收和传输数据
        self.linkLock = multiprocessing.Lock()
        #线程
        self.threadList = []
        self.threadLock = multiprocessing.Lock()

    def __del__(self):
        pass
    

    