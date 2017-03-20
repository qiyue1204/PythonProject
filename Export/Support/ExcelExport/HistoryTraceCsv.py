# coding=gb2312

import shutil   #类似于高级API，而且主要强大之处在于其对文件的复制与删除操作更是比较支持好
import uuid    #  UUID是128位的全局唯一标识符，通常由32字节的字符串表示
import xlsxwriter
import os
import pyodbc
import string
import ExcelExportConfig
from Support.ExcelExport.Convert import ConvertFuncVType
from Support.ExcelExport.Convert import VTypeStrSplit
from Support.ExcelExport.Convert import ConvertDirection
from Support.ExcelExport.Convert import ConvertAlarm
from Support.ExcelExport.Convert import ConvertStatus
import zipfile
from Manager.DataManager import LocationAnalyer
import sys
import csv
reload(sys)

sys.setdefaultencoding('gbk')
                
class HistoryTraceCsv(object):
    #存放导出数据的文件夹名
    dataFolder = 'D:\Download'
    detailFolder = '历史轨迹'.encode(ExcelExportConfig.envEncode)
    def __init__(self, UnitID, DeviceID, BDate, BTime, EDate,ETime):

        #self.companyInZone = {}
        #self.vehicleViolate = {}
        #self.analyer = LocationAnalyer(self.logObj, ExcelExportConfig.mapEngineAddress)
        #参数
        self.UnitID = UnitID
        self.DeviceID = DeviceID
        self.BDate = BDate
        self.BTime = BTime
        self.EDate = EDate
        self.ETime = ETime
        #self.sqlconGPS = pyodbc.connect( DSN='GPS_gov', UID=ExcelExportConfig.gpsGovUID, PWD=ExcelExportConfig.gpsGovPWD)
        #self.sqlconGPS = pyodbc.connect('DRIVER={FreeTDS};SERVER=localhost;PORT=1433;DATABASE=testdb;UID=me;PWD=pass;TDS_Version=7.0')
        
        
        self.sqlconGPS = pyodbc.connect( 'DRIVER={SQL Server Native Client 10.0};SERVER=10.50.40.201;DATABASE=GPS_GOV_History;UID=sa; PWD=123@abc')
        if not os.path.exists(HistoryTraceCsv.dataFolder):
            os.makedirs(HistoryTraceCsv.dataFolder)

        self.tmpName = uuid.uuid1().__str__().replace('-', '')
        self.tmpFolder = '%s/%s' %(HistoryTraceCsv.dataFolder, self.tmpName)
        if not os.path.exists(self.tmpFolder):
            os.makedirs(self.tmpFolder)
        
        #self.CreateFolder(HistoryTrace.detailFolder)
        
      
        
    def __del__(self):
        self.sqlconGPS.close()
        #del self.analyer

    #以ExcelExportBase.dataFolder为根目录创建文件夹
    def CreateFolder(self, folderName):
        fullName = '%s\%s' %(self.tmpFolder, folderName)    
        if not os.path.exists(fullName):
            os.makedirs(fullName)
            

    #在self.tmpFolder下创建excel工作表
    def CreateWorkbook(self, wbName):
        return file('%s/%s' %(self.tmpFolder, wbName),'wb')
        
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

        csvfile = self.CreateWorkbook('历史轨迹.csv'.encode(ExcelExportConfig.envEncode))
        #csvfile = file('D:\Download\历史轨迹.csv'.encode(ExcelExportConfig.envEncode),'wb')
        writer = csv.writer(csvfile)


        cursorGPS = self.sqlconGPS.cursor()

        cursorGPS.execute('SET NOCOUNT ON; EXEC UP_GOV_History_Position_Export 0,%d,%d,%d,%d,%d,0,0' % (self.DeviceID, self.BDate, self.EDate ,self.BTime ,self.ETime))

        writer.writerow(['车牌号','GPS时间','速度(km/h)','限速值(km/h)','经度','纬度','方向','报警','状态','接入平台名称','接收时间'])
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
                writer.writerow(row)
                row = cursorGPS.fetchone()
        csvfile.close()

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
        return '%s%s' %(self.tmpName, '.zip')


                 
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
            worksheet.write(startRow + rowIndex, Col, resultList[rowIndex].decode('gbk'), cellFormat)
    
