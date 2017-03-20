# coding=gb2312

import shutil   #类似于高级API，而且主要强大之处在于其对文件的复制与删除操作更是比较支持好
import uuid    #  UUID是128位的全局唯一标识符，通常由32字节的字符串表示
import xlsxwriter
import os
import pyodbc
import string
import datetime,time
import ExcelExportConfig
from Support.ExcelExport.Convert import ConvertFuncVType
from Support.ExcelExport.Convert import VTypeStrSplit
from Support.ExcelExport.Convert import ConvertDirection
from Support.ExcelExport.Convert import ConvertAlarm
from Support.ExcelExport.Convert import ConvertStatus
import zipfile
from Manager.DataManager import LocationAnalyer
import sys
reload(sys)

sys.setdefaultencoding('gbk')
                
class HistoryTrace(object):
    #存放导出数据的文件夹名
    dataFolder = 'D:\GPS_Server\HGov2\Export\Download'
    dataFolderHGov= 'D:\GPS_Server\WebGov_SC\Export\Download'
    detailFolder = '历史轨迹'.encode(ExcelExportConfig.envEncode)
    def __init__(self, logObj, UnitID, DeviceID, BDate, BTime, EDate,ETime):

        self.companyInZone = {}
        self.vehicleViolate = {}
        self.logObj = logObj
        self.analyer = LocationAnalyer(self.logObj, ExcelExportConfig.mapEngineAddress)
        #参数
        self.UnitID = UnitID
        self.DeviceID = DeviceID
        self.BDate = BDate
        self.BTime = BTime
        self.EDate = EDate
        self.ETime = ETime
        #self.sqlconGPS = pyodbc.connect( DSN='GPS_gov', UID=ExcelExportConfig.gpsGovUID, PWD=ExcelExportConfig.gpsGovPWD)
        #self.sqlconGPS = pyodbc.connect('DRIVER={FreeTDS};SERVER=localhost;PORT=1433;DATABASE=testdb;UID=me;PWD=pass;TDS_Version=7.0')
        
        
        self.sqlconGPS = pyodbc.connect( 'DRIVER={SQL Server Native Client 10.0};SERVER=192.168.100.201,3433;DATABASE=GPS_GOV_History;UID=webgov; PWD=1*fl@1,G-0,F')
        if not os.path.exists(HistoryTrace.dataFolder):
            os.makedirs(HistoryTrace.dataFolder)

        self.tmpName = uuid.uuid1().__str__().replace('-', '')
        self.tmpFolder = '%s/%s' %(HistoryTrace.dataFolder, self.tmpName)
        if not os.path.exists(self.tmpFolder):
            os.makedirs(self.tmpFolder)
        
        self.CreateFolder(HistoryTrace.detailFolder)
        
      
        
    def __del__(self):
        self.sqlconGPS.close()
        del self.analyer

    #以ExcelExportBase.dataFolder为根目录创建文件夹
    def CreateFolder(self, folderName):
        fullName = '%s\%s' %(self.tmpFolder, folderName)    
        if not os.path.exists(fullName):
            os.makedirs(fullName)
            

    #在self.tmpFolder下创建excel工作表
    def CreateWorkbook(self, wbName):
        return xlsxwriter.Workbook('%s/%s' %(self.tmpFolder, wbName))
        
    # 根据ZoneId获取应该在Excel报表中显示的地区名
    #def GetZoneName(self, zoneId):
    #    zoneName = ExcelExportConfig.zoneDic[zoneId]
    #    if 51000000 == zoneId:
    #        zoneName += '省'
    #    elif zoneId > 51300000:
    #        zoneName += '州'
    #    else:
    #        zoneName += '市'
    #    
    #    return zoneName
        
    def Log(self, message):
        try:
            self.logObj.LogToFile(message + '\n')
            self.logObj.LogToShell(message.encode(ExcelExportConfig.envEncode) + '\n')
        except Exception, e:
            pass

    #导出超速明细
    def ExportHistoryTrace(self):
        self.Log('Start to export HistoryTrace')
        workbook = self.CreateWorkbook('历史轨迹.xlsx'.encode(ExcelExportConfig.envEncode))
        cellFormat = workbook.add_format({
                                            'align': 'center',
                                            'valign': 'vcenter',
                                            'border': 1,
                                            'font_size': 10
                                            })
        
        
        

        beginDate = datetime.datetime.strptime(str(self.BDate),"%Y%m%d")
        print beginDate

        endDate = datetime.datetime.strptime(str(self.EDate),"%Y%m%d")
        print endDate

        t=(endDate-beginDate).days
        print t

        bt=beginDate
        if t>10:
            et = beginDate+datetime.timedelta(9)
        else:
            et = endDate
        
        beginTime = self.BTime
        print beginTime
        endTime = self.ETime
        print endTime

        while (t>=0):
            print bt.strftime("%Y%m%d") + '-' + et.strftime("%Y%m%d")
            self.BDate = int(bt.strftime("%Y%m%d"))
            self.EDate = int(et.strftime("%Y%m%d"))
            bt = bt+datetime.timedelta(10)
            et = et + datetime.timedelta(10)
            if et>endDate:
                et = endDate
            else:
                et = et

            if self.BDate==int(beginDate.strftime("%Y%m%d")):
                self.BTime = beginTime
            else:
                self.BTime = 0

            if self.EDate==int(endDate.strftime("%Y%m%d")):
                self.ETime = endTime
            else:
                self.ETime = 86399
                
            print self.BTime
            print self.ETime

            t=t-10
            worksheet = workbook.add_worksheet(str(self.BDate)+'--'+str(self.EDate))

            # 表头
            worksheet.write('A1', '车牌号', cellFormat)
            worksheet.write('B1', 'GPS时间', cellFormat)
            worksheet.write('C1', '速度(km/h)', cellFormat)
            worksheet.write('D1', '限速值(km/h)', cellFormat)
            worksheet.write('E1', '经度', cellFormat)
            worksheet.write('F1', '纬度', cellFormat)
            worksheet.write('G1', '方向', cellFormat)
            worksheet.write('H1', '报警', cellFormat)
            worksheet.write('I1', '状态', cellFormat)
            worksheet.write('J1', '位置信息', cellFormat)
            worksheet.write('K1', '接入平台名称', cellFormat)
            worksheet.write('L1', '接收时间', cellFormat)

            cursorGPS = self.sqlconGPS.cursor()

            cursorGPS.execute('SET NOCOUNT ON; EXEC UP_GOV_History_Position_Export 0,%d,%d,%d,%d,%d,0,0' % (self.DeviceID, self.BDate, self.EDate ,self.BTime ,self.ETime))

        
            #cursorGPS.execute('select top 1 * from dbo.GPSVehicle')
            row = cursorGPS.fetchone()
            # 如果有超速明细，则生成excel，导出数据
            if row:
                posList = []
                #从表头的下一行开始导出数据
                startIndex = 1
                posIndex = 1                      
                #companyDic = self.companyInZone[zoneId]
                while row:
                    self.__WriteHistoryTrace(worksheet, startIndex, row, cellFormat)
                    #保存超速开始经纬度坐标和结束经纬度坐标
                    try:
                        #Lon = str(row[5])[0:3]+'.'+str(row[5])[3:]
                        #La = str(row[6])[0:2]+'.'+str(row[6])[2:]                               
                        posList.append([string.atof(row[4]),string.atof(row[5])])
                    except Exception, e:
                        self.Log(e.__str__())
                        #如果达到400个坐标（posBlockSize = 400），则开始解析
                    if(posList.__len__() >= ExcelExportConfig.posBlockSize):
                        self.__PassPos(posList, worksheet, posIndex, 9, cellFormat)
                        posIndex += ExcelExportConfig.posBlockSize
                        del posList[:]
                    startIndex += 1
                    row = cursorGPS.fetchone()
            
                #对于不满400个坐标的单独处理
                if(posList.__len__() > 0):
                    self.__PassPos(posList, worksheet, posIndex, 9, cellFormat)
                    del posList[:]              
        workbook.close()

    #压缩self.tmpFolder，用于将压缩后的文件返回客户端
    def CompressData(self):
        filelist = []
        fullTmpFolder = os.path.abspath(self.tmpFolder)
        fullZipName = '%s%s' %(fullTmpFolder, '.zip')
        for root, dirlist, files in os.walk(fullTmpFolder):
            for filename in files:
                filelist.append(os.path.join(root, filename))
        destZip = zipfile.ZipFile(fullZipName, "w")
        try:
            for eachfile in filelist:
                destfile = eachfile[fullTmpFolder.__len__():]
                destZip.write(eachfile, destfile)

            shutil.rmtree(self.tmpFolder)
        except Exception, e:
            self.Log(e.__str__())

        destZip.close()
        shutil.copyfile(self.dataFolder+'\\'+self.tmpName+'.zip',self.dataFolderHGov+'\\'+self.tmpName+'.zip')
        return '%s%s' %(self.tmpName, '.zip')

    # 导出超速数据
    def __WriteHistoryTrace(self, worksheet, rowIndex, rowData, cellFormat):
        try:
            #车牌号
            worksheet.write(rowIndex, 0, rowData[0].decode('gbk', 'ignore'), cellFormat)
            #GPS时间
            worksheet.write(rowIndex, 1, rowData[1], cellFormat)            
            #速度
            worksheet.write(rowIndex, 2, rowData[2].decode('gbk', 'ignore'), cellFormat)
            #限速值
            worksheet.write(rowIndex, 3, rowData[3]&0xFF, cellFormat)     
            #经度
            worksheet.write(rowIndex, 4, rowData[4], cellFormat)
            #纬度
            worksheet.write(rowIndex, 5, rowData[5], cellFormat)            
            #方向
            worksheet.write(rowIndex, 6, ConvertDirection(rowData[6]).encode('gbk'), cellFormat)
            #报警
            worksheet.write(rowIndex, 7, ConvertAlarm(rowData[7]).encode('gbk'), cellFormat)
            #状态
            worksheet.write(rowIndex, 8, ConvertStatus(rowData[7]).encode('gbk'), cellFormat)
            #开始位置
            #worksheet.write(rowIndex, 9, rowData[9], cellFormat)
            #接入平台名称
            worksheet.write(rowIndex, 10, rowData[9].decode('gbk'), cellFormat)            
            #接收时间
            worksheet.write(rowIndex, 11, rowData[10], cellFormat)      
        except Exception, e:
            self.Log(e.__str__())
        
                 
    # 对传入的经纬度坐标列表进行解析，并将解析后的地址写入到对应的单元格中。
    def __PassPos(self, posList, worksheet, startRow, Col, cellFormat):
        resultList = []
        self.analyer.GetLocationData(posList, resultList)
        #将解析后的地址保存到excel导出表中，200个开始位置，200个结束位置
        for rowIndex in range(0, resultList.__len__()):
            #偶数为开始位置
            #if 0 == rowIndex % 2:
                #worksheet.write(startRow + rowIndex / 2, startCol, resultList[rowIndex].decode('gbk'), cellFormat)
            #奇数为结束位置
            #else:
                #worksheet.write(startRow + rowIndex / 2, endCol, resultList[rowIndex].decode('gbk'), cellFormat)
            try:
                worksheet.write(startRow + rowIndex, Col, resultList[rowIndex].decode('gbk'), cellFormat)
            except UnicodeDecodeError:
                worksheet.write(startRow + rowIndex, Col, '', cellFormat)
                continue
    
