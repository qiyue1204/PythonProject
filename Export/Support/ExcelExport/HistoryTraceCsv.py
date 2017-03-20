# coding=gb2312

import shutil   #�����ڸ߼�API��������Ҫǿ��֮����������ļ��ĸ�����ɾ���������ǱȽ�֧�ֺ�
import uuid    #  UUID��128λ��ȫ��Ψһ��ʶ����ͨ����32�ֽڵ��ַ�����ʾ
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
    #��ŵ������ݵ��ļ�����
    dataFolder = 'D:\Download'
    detailFolder = '��ʷ�켣'.encode(ExcelExportConfig.envEncode)
    def __init__(self, UnitID, DeviceID, BDate, BTime, EDate,ETime):

        #self.companyInZone = {}
        #self.vehicleViolate = {}
        #self.analyer = LocationAnalyer(self.logObj, ExcelExportConfig.mapEngineAddress)
        #����
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

    #��ExcelExportBase.dataFolderΪ��Ŀ¼�����ļ���
    def CreateFolder(self, folderName):
        fullName = '%s\%s' %(self.tmpFolder, folderName)    
        if not os.path.exists(fullName):
            os.makedirs(fullName)
            

    #��self.tmpFolder�´���excel������
    def CreateWorkbook(self, wbName):
        return file('%s/%s' %(self.tmpFolder, wbName),'wb')
        
    # ����ZoneId��ȡӦ����Excel��������ʾ�ĵ�����
    #def GetZoneName(self, zoneId):
    #    zoneName = ExcelExportConfig.zoneDic[zoneId]
    #    if 51000000 == zoneId:
    #        zoneName += 'ʡ'
    #    elif zoneId > 51300000:
    #        zoneName += '��'
    #    else:
    #        zoneName += '��'
    #    
    #    return zoneName
        
    def Log(self, message):
        try:
            self.logObj.LogToFile(message + '\n')
            self.logObj.LogToShell(message.encode(ExcelExportConfig.envEncode) + '\n')
        except Exception, e:
            pass

    #����������ϸ
    def ExportHistoryTrace(self):

        csvfile = self.CreateWorkbook('��ʷ�켣.csv'.encode(ExcelExportConfig.envEncode))
        #csvfile = file('D:\Download\��ʷ�켣.csv'.encode(ExcelExportConfig.envEncode),'wb')
        writer = csv.writer(csvfile)


        cursorGPS = self.sqlconGPS.cursor()

        cursorGPS.execute('SET NOCOUNT ON; EXEC UP_GOV_History_Position_Export 0,%d,%d,%d,%d,%d,0,0' % (self.DeviceID, self.BDate, self.EDate ,self.BTime ,self.ETime))

        writer.writerow(['���ƺ�','GPSʱ��','�ٶ�(km/h)','����ֵ(km/h)','����','γ��','����','����','״̬','����ƽ̨����','����ʱ��'])
        #cursorGPS.execute('select top 1 * from dbo.GPSVehicle')
        row = cursorGPS.fetchone()
        # ����г�����ϸ��������excel����������
        if row:
            posList = []
            #�ӱ�ͷ����һ�п�ʼ��������
            startIndex = 1
            posIndex = 1                      
            #companyDic = self.companyInZone[zoneId]
            while row:
                writer.writerow(row)
                row = cursorGPS.fetchone()
        csvfile.close()

    #ѹ��self.tmpFolder�����ڽ�ѹ������ļ����ؿͻ���
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


                 
    # �Դ���ľ�γ�������б���н���������������ĵ�ַд�뵽��Ӧ�ĵ�Ԫ���С�
    def __PassPos(self, posList, worksheet, startRow, Col, cellFormat):
        resultList = []
        self.analyer.GetLocationData(posList, resultList)
        #��������ĵ�ַ���浽excel�������У�200����ʼλ�ã�200������λ��
        for rowIndex in range(0, resultList.__len__()):
            #ż��Ϊ��ʼλ��
            #if 0 == rowIndex % 2:
                #worksheet.write(startRow + rowIndex / 2, startCol, resultList[rowIndex].decode('gbk'), cellFormat)
            #����Ϊ����λ��
            #else:
                #worksheet.write(startRow + rowIndex / 2, endCol, resultList[rowIndex].decode('gbk'), cellFormat)
            worksheet.write(startRow + rowIndex, Col, resultList[rowIndex].decode('gbk'), cellFormat)
    
