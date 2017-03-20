# coding=utf8

import os
import time
import ctypes
import struct
import socket
import Conf
from Support.Log import LogManager
from Support.NetIO import NetClient
from Support.NetIO.NetCommand import *

if __name__ == '__main__':
    logObj = LogManager('ExcelExport.txt')
    logObj.Start()

    totalTestTime = 10000
    serverIp = '10.50.75.111'
    if(Conf.isProdEnv):
        totalTestTime = 10000
        serverIp = '192.168.100.206'

    for testTime in range(0, totalTestTime):
        print 'Run test time %d' %(testTime + 1) + '\n'

        netClient = NetClient(logObj, Conf.hbInterval)
        netClient.StartNetClient()
        connectLink = netClient.Connect(serverIp, Conf.listenPort)
        #打包包头和数据
        #dataLength = 22 + 16
        dataLength = 22 +144   #取决于数据结构中的长度

        subCmd = exportSixBanRequest
        if(0 == testTime % 2):
            subCmd = exportNormalRequest
        requestHeader = struct.pack('HHIHHIhhI', socket.htons(dataLength), 0, socket.htonl(123), \
            socket.htons(mainCmdExcel), socket.htons(subCmd), 0, \
            socket.htons(serverReserve), 0, 0)
        requestBody = struct.pack('IIII', socket.htonl(20151101), socket.htonl(20151130), socket.htonl(0),
                                                 socket.htonl(0))                             #把32位正整数从主机字节序转换成网络序。
        requestBody = requestBody+'1,2,3,4||1,2,3,4'
        netClient.SendData(connectLink, requestHeader + requestBody);

        #接收数据
        #过滤掉心跳包和Hook
        resultHeader = None
        dataBuf = ctypes.create_string_buffer('\0', 65535)
        while True:
            ctypes.memset(dataBuf, 0, 65535)
            resultHeader = netClient.RecvData(connectLink, dataBuf)

            if True == netClient.CheckHBPackage(connectLink, resultHeader) or \
                True == netClient.CheckLinkHook(connectLink, resultHeader):
                continue
            break

        structObj = struct.Struct('150s')
        fileName = structObj.unpack_from(dataBuf)[0]
        fileName = fileName[0:fileName.find('\0')]

        logObj.LogToFile("Start to delete %s" %(fileName) + '\n')
        logObj.LogToShell("Start to delete %s" %(fileName) + '\n')
        netClient.StopNetClient()

    time.sleep(2)
    logObj.Stop()
