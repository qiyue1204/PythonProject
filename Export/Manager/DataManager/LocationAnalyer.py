# coding=utf8

import socket
import ctypes
import struct
import Conf
from Support.NetIO import NetClient
from Support.NetIO.NetCommand import *

#解析地址详情子命令
locationSubCmdRequest = 0x1002
locationSubCmdResponse = 0x2002

# UINT16_T        ui16DataLength;         //数据包长度
# UINT16_T        ui16DataSequence;       //数据包序号
# UINT32_T        ui32SourceReserve;      //保留
# UINT16_T        ui16Cmd;                //主命令
# UINT16_T        ui16SubCmd;             //子命令
# UINT32_T        ui32TargetReserve;      //保留
# INT16_T         i16Reserve;             //保留
# INT16_T         i16Result;              //HOOK验证做服务器标志，和主命令功能基本一样
# UINT32_T	      ui32Link;               //链路标记，保留
    
# 从地图接口返回解析调用结果的类
class LocationAnalyer():
    def GetLocationData(self, pointList, out_resultList):
        '''
            输入值为浮点型的坐标点
        '''
        #连接未建立或断开，重连接，失败则退出
        if None == self.connectLink or False == self.connectLink[2]:
            if False == self.__ReConnect():
                del out_resultList[:]
                self.logObj.LogToFile('GetLocationData failed!\n')
                return False
        
        #数据缓存
        dataBuf = ctypes.create_string_buffer('\0', 65535)
        #数据打包
        structObj = struct.Struct('I')
        #打包包头和数据
        dataLength = 22 + 4 + pointList.__len__() * 16
        requestHeader = struct.pack('HHIHHIhhI', socket.htons(dataLength), 0, 0, \
            socket.htons(mainCmd), socket.htons(locationSubCmdRequest), 0, \
            socket.htons(serverReserve), 0, 0)
        sendPointNum = pointList.__len__()
        structObj.pack_into(dataBuf, 0, sendPointNum)
        structObj.__init__('dd')
        for index in range(0, sendPointNum):
            structObj.pack_into(dataBuf, 4 + index * 16, pointList[index][0], pointList[index][1])
        #发送数据
        if (False == self.netClient.SendData(self.connectLink, \
            requestHeader + dataBuf.raw[0:4 + sendPointNum * 16])):
            self.logObj.LogToFile('GetLocationData failed!\n')
            return False  
        #接收数据
        #过滤掉心跳包和Hook
        resultHeader = None
        while True:
            ctypes.memset(dataBuf, 0, 65535)
            resultHeader = self.netClient.RecvData(self.connectLink, dataBuf)
            if None == resultHeader:
                self.logObj.LogToFile('GetLocationData failed!\n')
                return False
                
            if True == self.netClient.CheckHBPackage(self.connectLink, resultHeader) or \
                True == self.netClient.CheckLinkHook(self.connectLink, resultHeader):
                continue
            break

        #读数据
        structObj.__init__('I')
        recvPointNum = structObj.unpack_from(dataBuf, 0)[0]
        if recvPointNum != sendPointNum:
            self.logObj.LogToFile('GetLocationData failed because of send ' + sendPointNum.__str__() \
            + ' points and recv ' + recvPointNum.__str__() + ' points!\n')
            return False
        #读返回数据
        structObj.__init__('150s')
        del out_resultList[:]
        
        for index in range(0, recvPointNum):
            locationStr = structObj.unpack_from(dataBuf, 4 + index * 150)[0]
            locationStr = locationStr[0:locationStr.find('\0')]
            out_resultList.append(locationStr)
            
        return True
        
    
    def TranslatePoint(self, intPointList, out_pointList):
        '''
            转换GPS坐标点，输入值为整形坐标点的队列，输出值为浮点型坐标点队列
        '''
        for point in intPointList:
            out_pointList.append([point[0].__float__() / 1000000.0, point[1].__float__() / 1000000.0])
    
    def __ReConnect(self):
        '''
            私有函数：连接/重连接
        '''
        if None != self.connectLink and False != self.connectLink[2]:
            self.netClient.DisConnect(self.connectLink)
        self.connectLink = self.netClient.Connect(self.connectInfo[0], self.connectInfo[1])
        if None == self.connectLink:
            self.logObj.LogToFile('LocationAnalyer failed to build connection to MapDataInterface!\n')
            return False
        
        #连接后发Hook
        self.netClient.SendHook(self.connectLink)
        self.logObj.LogToFile('LocationAnalyer successfully built connection to MapDataInterface.\n')
        return True
    
    def __init__(self, logObj, connectInfo):
        self.logObj = logObj
        self.netClient = NetClient(logObj, Conf.hbInterval, 10)
        self.netClient.StartNetClient()
        self.connectInfo = connectInfo      #connectInfo应该为(host, port)的tuple
        self.connectLink = None

    def __del__(self):
        self.netClient.StopNetClient()
    

    