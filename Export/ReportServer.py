# coding=utf8

import time
import ctypes
import struct
import socket
import Conf
from Support.Log import LogManager
from Support.NetIO import NetServer
from Support.NetIO.NetCommand import *
from Support.ExcelExport import SixBanOverSpeedAndBreakBan
from Support.ExcelExport import NormalOverSpeed
from Support.ExcelExport import HistoryTrace
from Support.ExcelExport.Convert import ConvertFuncVType
from Support.ExcelExport.Convert import VTypeStrSplit

#处理线程
def ReportServerWorker(netServer, linkInfo):
    dataBuf = ctypes.create_string_buffer('\0', 65535)  #建立一个65536字节的buffer，里面存了一个NULL

    while True:
        #获取数据包
        netHeader = netServer.RecvData(linkInfo, dataBuf)
        if None == netHeader:
            netServer.logObj.LogToFile('Quit report server worker thread.\n');
            break
        if True == netServer.CheckHBPackage(linkInfo, netHeader):
            continue
        if True == netServer.ExportExcel(linkInfo, netHeader, dataBuf):
            continue

class ReportServer(NetServer):
    def __init__(self, logObj, hbInterval):
        NetServer.__init__(self, logObj, hbInterval)

    def __del__(self):
        NetServer.__del__()

    def ExportExcel(self, linkInfo, netHeader, paraBuf):
        netHeaderInfo = struct.unpack('HHIHHIhhI', netHeader)  #pack(...) 根据格式字符串，将python值转换为字节流（字节数组）,unpack(...)  与pack() 相反。根据格式字符串，将字节流转换成python 数据类型。共9个数据
        if(mainCmdExcel != socket.ntohs(netHeaderInfo[3])):
            return None
        
        if(socket.ntohs(netHeaderInfo[6])==1):
            structObj = struct.Struct('IIIIII')  #共6个数据,新增一个字符串类型20s
            exportPara = structObj.unpack_from(paraBuf, 0)
            UnitID = socket.ntohl(exportPara[0])
            DeviceID = socket.ntohl(exportPara[1])
            BDate = socket.ntohl(exportPara[2])
            BTime = socket.ntohl(exportPara[3])
            EDate = socket.ntohl(exportPara[4])
            ETime = socket.ntohl(exportPara[5])

            
            #FuncVType = '5,5,0,0||4,4,-1,-1, '
            self.logObj.LogToFile('Start to export excel for user %d.\n' %(socket.ntohl(netHeaderInfo[2])))
            self.logObj.LogToFile('BDate: %d; BTime: %d; EDate: %d; ETime: %d; DeviceID: %d.\n' %(BDate, BTime, EDate, ETime, DeviceID))           
            excelExport = None
            subCmd = socket.ntohs(netHeaderInfo[4])
            excelExport = HistoryTrace.HistoryTrace(self.logObj, UnitID, DeviceID, BDate, BTime, EDate, ETime) 
            
            excelExport.ExportHistoryTrace()
            print('End ExportHistoryTrace')
            fileName = excelExport.CompressData()
            print('End CompressData')

            del excelExport
            return self.__SendExportExcelResponse(linkInfo, fileName, netHeaderInfo) 

        else:
            structObj = struct.Struct('IIIII40s')  #共5个数据,新增一个字符串类型20s
            exportPara = structObj.unpack_from(paraBuf, 0)
            startDate = socket.ntohl(exportPara[0])
            endDate = socket.ntohl(exportPara[1])
            vehicleType = socket.ntohl(exportPara[2])
            platformId = socket.ntohl(exportPara[3])
            govStatus = socket.ntohl(exportPara[4])
            FuncVType = exportPara[5].replace('\x00','')
            FuncVType=FuncVType.replace(' ','')
            FuncVType=FuncVType[:-1]
            print FuncVType
            #govStatus = 0
            if (vehicleType==128 and VTypeStrSplit(FuncVType,1)==0 and VTypeStrSplit(FuncVType,2)==0 and VTypeStrSplit(FuncVType,3)==0 and VTypeStrSplit(FuncVType,4)==0):
                FuncVType = str(vehicleType)+',0,0,0||-1,-1,-1,-1,'
            elif (vehicleType!=128 and VTypeStrSplit(FuncVType,1)==0 and VTypeStrSplit(FuncVType,2)==0 and VTypeStrSplit(FuncVType,3)==0 and VTypeStrSplit(FuncVType,4)==0):
                FuncVType = str(vehicleType)+','+str(vehicleType)+',0,0||-1,-1,-1,-1,'                
            else:
                pass
            print FuncVType
            
            
            #FuncVType = '5,5,0,0||4,4,-1,-1, '
            self.logObj.LogToFile('Start to export excel for user %d.\n' %(socket.ntohl(netHeaderInfo[2])))
            self.logObj.LogToFile('StartDate: %d; EndDate: %d; VehicleType: %d; PlatformId: %d; govStatus: %d; FuncVType: %s.\n' %(startDate, endDate, vehicleType, platformId, govStatus, FuncVType))
            excelExport = None
            subCmd = socket.ntohs(netHeaderInfo[4])
            #if (vehicleType == 128 or (vehicleType == 0 and ConvertFuncVType(FuncVType,1)==128)):
            if (vehicleType == 128 or (vehicleType == 0 and (ConvertFuncVType(FuncVType,1)==128 or ConvertFuncVType(FuncVType,2)==128 or ConvertFuncVType(FuncVType,3)==128 or ConvertFuncVType(FuncVType,4)==128))):
                excelExport = NormalOverSpeed(self.logObj, startDate, endDate, vehicleType, platformId, govStatus, FuncVType)  #加上新的字段
            elif subCmd == exportSixBanRequest:
                excelExport = SixBanOverSpeedAndBreakBan(self.logObj, startDate, endDate, vehicleType, platformId, govStatus, FuncVType)  #加上新的字段
            elif subCmd == exportNormalRequest:
                excelExport = NormalOverSpeed(self.logObj, startDate, endDate, vehicleType, platformId, govStatus, FuncVType)  #加上新的字段
            else:
                return None
            
            excelExport.ExportDetail()
            print('End ExportDetail')
            excelExport.ExportSum()
            print('End ExportSum')
            excelExport.ExportVehicle()
            print('End ExportVehicle')
            fileName = excelExport.CompressData()
            print('End CompressData')
            
            del excelExport
            return self.__SendExportExcelResponse(linkInfo, fileName, netHeaderInfo)           
        

		

    def __SendExportExcelResponse(self, linkInfo, fileName, netHeader):
        exportHeader = struct.pack('HHIHHIhhI', socket.htons(22 + fileName.__len__()), netHeader[1], netHeader[2],
                                   netHeader[3], netHeader[4], netHeader[5], netHeader[6], netHeader[7], netHeader[8])
        exportBody = struct.pack('%ss' %fileName.__len__(), fileName)

        try:
            linkInfo[0].send(exportHeader + exportBody)
        except socket.error as err:
            self.logObj.LogToFile(err.__str__() + ' send HBResponse failed!\n')
            self.DisConnect(linkInfo)
            return False

        return True

if __name__ == '__main__':
    logObj = LogManager(Conf.logFile)
    logObj.Start()

    reportServer = ReportServer(logObj, Conf.hbInterval)
    reportServer.InitNetServer(10, Conf.listenPort)
    reportServer.StartNetServer(ReportServerWorker)

    while 1:
        time.sleep(5)

    time.sleep(2)
    logObj.Stop()





































