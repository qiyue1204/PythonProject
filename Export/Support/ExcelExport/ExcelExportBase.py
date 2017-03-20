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
import zipfile
from Manager.DataManager import LocationAnalyer
import sys
reload(sys)

sys.setdefaultencoding('gbk')
                
class ExcelExportBase(object):
    #��ŵ������ݵ��ļ�����
    dataFolder = 'D:\GPS_Server\HGov2\Export\Download'
    dataFolderHGov= 'D:\GPS_Server\WebGov_SC\Export\Download'
    def __init__(self, logObj, startDate, endDate, vehicleType, platformId, govStatus, FuncVType):
        self.companyInZone = {}
        self.vehicleViolate = {}
        self.logObj = logObj
        self.analyer = LocationAnalyer(self.logObj, ExcelExportConfig.mapEngineAddress)
        #����
        self.startDate = startDate
        self.endDate = endDate
        self.vehicleType = vehicleType
        self.platformId = platformId
        self.govStatus = govStatus
        self.FuncVType = FuncVType
        self.sqlconGPS = pyodbc.connect( DSN='GPS_gov', UID=ExcelExportConfig.gpsGovUID, PWD=ExcelExportConfig.gpsGovPWD)
 
        if not os.path.exists(ExcelExportBase.dataFolder):
            os.makedirs(ExcelExportBase.dataFolder)

        self.tmpName = uuid.uuid1().__str__().replace('-', '')
        self.tmpFolder = '%s/%s' %(ExcelExportBase.dataFolder, self.tmpName)
        if not os.path.exists(self.tmpFolder):
            os.makedirs(self.tmpFolder)

    def __del__(self):
        self.sqlconGPS.close()
        del self.analyer

    #��ExcelExportBase.dataFolderΪ��Ŀ¼�����ļ���
    def CreateFolder(self, folderName):
        fullName = '%s/%s' %(self.tmpFolder, folderName)
        if not os.path.exists(fullName):
            os.makedirs(fullName)

    #��self.tmpFolder�´���excel������
    def CreateWorkbook(self, wbName):
        return xlsxwriter.Workbook('%s/%s' %(self.tmpFolder, wbName))
        
    # ����ZoneId��ȡӦ����Excel��������ʾ�ĵ�����
    def GetZoneName(self, zoneId):
        zoneName = ExcelExportConfig.zoneDic[zoneId]
        if 51000000 == zoneId:
            zoneName += 'ʡ'
        elif zoneId > 51300000:
            zoneName += '��'
        else:
            zoneName += '��'
        
        return zoneName
        
    def Log(self, message):
        try:
            self.logObj.LogToFile(message + '\n')
            self.logObj.LogToShell(message.encode(ExcelExportConfig.envEncode) + '\n')
        except Exception, e:
            pass

    #����������ϸ
    def ExportOverSpeedDetail(self, workbook, zoneId, vehicleType, platformId, govStatus, FuncVType,  cellFormat):
        worksheet = workbook.add_worksheet('����')

        # ��ͷ
        worksheet.write('A1', '������ҵ����', cellFormat)
        worksheet.write('B1', '���ƺ�', cellFormat)
        worksheet.write('C1', '��������', cellFormat)
        worksheet.write('D1', '������·������ҵ', cellFormat)
        worksheet.write('E1', '���ٿ�ʼʱ��', cellFormat)
        worksheet.write('F1', '���ٽ���ʱ��', cellFormat)
        worksheet.write('G1', '����ʱ��', cellFormat)
        worksheet.write('H1', '���٣�km/h��', cellFormat)
        worksheet.write('I1', '�ٶȣ�km/h��', cellFormat)
        worksheet.write('J1', '�����ʣ�%��', cellFormat)
        worksheet.write('K1', '��ʼλ��', cellFormat)
        worksheet.write('L1', '����λ��', cellFormat)
        worksheet.write('M1', '�Ƿ����', cellFormat)
        worksheet.write('N1', '��װ������', cellFormat)
        worksheet.write('O1', '���ݹ���', cellFormat)
        cursorGPS = self.sqlconGPS.cursor()
        CarType = ConvertFuncVType(FuncVType,1)
        Filter = ConvertFuncVType(FuncVType,11)
        cursorGPS.execute('SET NOCOUNT ON; EXEC SP_GOV_Stat_6BanOverSpeedDetail_patch %d,%d,%d,0,%d,0,%d,%d,1'
                          ',\'%s\',1,1,10,400000' % (self.startDate, self.endDate, zoneId, CarType, platformId, govStatus, Filter))
        row = cursorGPS.fetchone()
        # ����г�����ϸ��������excel����������
        if row:
            posList = []
            #�ӱ�ͷ����һ�п�ʼ��������
            startIndex = 1
            posIndex = 1
            companyDic = self.companyInZone[zoneId]
            while row:
                if((row[20].decode('gbk') == '��' and row[12] >= 20) or row[12] >= 50):
                    if(51000000 != zoneId):
                        vehicleNum = 0
                        if(row[6] in companyDic):
                            vehicleNum = companyDic[row[6]]
                        if(not row[1] in self.vehicleViolate):
                            vehicleNum += 1
                            self.vehicleViolate[row[1]] = True
                        companyDic[row[6]] = vehicleNum
                    self.__WriteOverSpeedDetail(worksheet, startIndex, row, cellFormat)
                    #���泬�ٿ�ʼ��γ������ͽ�����γ������
                    try:
                        posTmp = row[18].__str__().split('|')
                        posList.append([string.atof(posTmp[0]), string.atof(posTmp[1])])
                        posTmp = row[19].__str__().split('|')
                        posList.append([string.atof(posTmp[0]), string.atof(posTmp[1])])
                    except Exception, e:
                        self.Log(e.__str__())
                    #����ﵽ400�����꣨posBlockSize = 400������ʼ����
                    if(posList.__len__() >= ExcelExportConfig.posBlockSize):
                        self.__PassPos(posList, worksheet, posIndex, 10, 11, cellFormat)
                        posIndex += ExcelExportConfig.posBlockSize / 2
                        del posList[:]
                    startIndex += 1
                row = cursorGPS.fetchone()
            
            #���ڲ���400������ĵ�������
            if(posList.__len__() > 0):
                self.__PassPos(posList, worksheet, posIndex, 10, 11, cellFormat)
                del posList[:]

    #�����춯��ϸ
    def ExportBreakBanDetail(self, workbook, zoneId, vehicleType, platformId, govStatus, FuncVType, cellFormat):
        worksheet = workbook.add_worksheet('�춯')

        # ��ͷ
        worksheet.write('A1', '������ҵ����', cellFormat)
        worksheet.write('B1', '���ƺ�', cellFormat)
        worksheet.write('C1', '��������')
        worksheet.write('D1', '������·������ҵ', cellFormat)
        worksheet.write('E1', '��ʼʱ��', cellFormat)
        worksheet.write('F1', '����ʱ��', cellFormat)
        worksheet.write('G1', '����ʱ��', cellFormat)
        worksheet.write('H1', '��ʼλ��', cellFormat)
        worksheet.write('I1', '����λ��', cellFormat)
        worksheet.write('J1', '��װ������', cellFormat)
        worksheet.write('K1', '���ݹ���', cellFormat)

        cursorGPS = self.sqlconGPS.cursor()

        # if (self.vehicleType!=0):
            # cursorGPS.execute('SET NOCOUNT ON; EXEC SP_GOV_Stat_6BanNightBanDetail_patch %d,%d,%d,0,%d,0,%d,1'
                          # ',\'AND 1=1\',1,1,10,400000' % (self.startDate, self.endDate, zoneId, self.vehicleType, platformId))
        # else:
        CarType = ConvertFuncVType(FuncVType,2)
        Filter = ConvertFuncVType(FuncVType,22)
        cursorGPS.execute('SET NOCOUNT ON; EXEC SP_GOV_Stat_6BanNightBanDetail_patch %d,%d,%d,0,%d,0,%d,%d,1'
                          ',\'%s\',1,1,10,400000' % (self.startDate, self.endDate, zoneId, CarType, platformId, govStatus, Filter))            
        row = cursorGPS.fetchone()
        # ������춯��ϸ��������excel����������
        if row:
            posList = []
            #�ӱ�ͷ����һ�п�ʼ��������
            startIndex = 1
            posIndex = 1
            companyDic = self.companyInZone[zoneId]
            while row:
                if(51000000 != zoneId):
                    vehicleNum = 0
                    if(row[6] in companyDic):
                        vehicleNum = companyDic[row[6]]
                    if(not row[1] in self.vehicleViolate):
                        vehicleNum += 1
                        self.vehicleViolate[row[1]] = True
                    companyDic[row[6]] = vehicleNum
                self.__WriteBreakBanDetail(worksheet, startIndex, row, cellFormat)
                #�����춯��ʼ��γ������ͽ�����γ������
                posTmp = row[13].__str__().split('|')
                posList.append([string.atof(posTmp[0]) / 1000000.0, string.atof(posTmp[1]) / 1000000.0])
                posTmp = row[14].__str__().split('|')
                posList.append([string.atof(posTmp[0]) / 1000000.0, string.atof(posTmp[1]) / 1000000.0])
                #����ﵽ400�����꣨posBlockSize = 400������ʼ����
                if(posList.__len__() >= ExcelExportConfig.posBlockSize):
                    self.__PassPos(posList, worksheet, posIndex, 7, 8, cellFormat)
                    posIndex += ExcelExportConfig.posBlockSize / 2
                    del posList[:]
                startIndex += 1
                row = cursorGPS.fetchone()
            
            #���ڲ���400������ĵ�������
            if(posList.__len__() > 0):
                self.__PassPos(posList, worksheet, posIndex, 7, 8, cellFormat)
                del posList[:]

     #������λ�ж���ϸ
    def ExportPositionBreakDetail(self, workbook, zoneId, vehicleType, platformId, govStatus, FuncVType, cellFormat):
        worksheet = workbook.add_worksheet('������Сʱ�������ϴ�')

        # ��ͷ
        worksheet.write('A1', '������ҵ����', cellFormat)
        worksheet.write('B1', '���ƺ�', cellFormat)
        worksheet.write('C1', '��������', cellFormat)
        worksheet.write('D1', '������·������ҵ', cellFormat)
        worksheet.write('E1', '�ж�����ʱ��', cellFormat)
        worksheet.write('F1', '�ָ�����ʱ��', cellFormat)
        worksheet.write('G1', '����ʱ��', cellFormat)
        worksheet.write('H1', '��ʼλ��', cellFormat)
        worksheet.write('I1', '����λ��', cellFormat)
        worksheet.write('J1', '��װ������', cellFormat)

        cursorGPS = self.sqlconGPS.cursor()
        # if (self.vehicleType!=0):
            # cursorGPS.execute('SET NOCOUNT ON; EXEC SP_GOV_Stat_6BanPositionBreakDetail_patch %d,%d,%d,0,%d,0,%d,1'
                          # ',\'AND 1=1\',1,1,10,400000' % (self.startDate, self.endDate, zoneId, self.vehicleType, platformId))       
        # else:
        CarType = ConvertFuncVType(FuncVType,3)
        Filter = ConvertFuncVType(FuncVType,33)
        cursorGPS.execute('SET NOCOUNT ON; EXEC SP_GOV_Stat_6BanPositionBreakDetail_patch %d,%d,%d,0,%d,0,%d,%d,1'
                          ',\'%s\',1,1,10,400000' % (self.startDate, self.endDate, zoneId, CarType, platformId,govStatus, Filter))
        row = cursorGPS.fetchone()
        # ����ж�λ�ж���ϸ��������excel����������
        if row:
            posList = []
            #�ӱ�ͷ����һ�п�ʼ��������
            startIndex = 1
            posIndex = 1
            companyDic = self.companyInZone[zoneId]
            while row:
                if(51000000 != zoneId):
                    vehicleNum = 0
                    if(row[6] in companyDic):
                        vehicleNum = companyDic[row[6]]
                    if(not row[1] in self.vehicleViolate):
                        vehicleNum += 1
                        self.vehicleViolate[row[1]] = True
                    companyDic[row[6]] = vehicleNum
                self.__WritePositionBreakDetail(worksheet, startIndex, row, cellFormat)
                #�����춯��ʼ��γ������ͽ�����γ������
                posTmp = row[13].__str__().split('|')
                posList.append([string.atof(posTmp[0]) / 1000000.0, string.atof(posTmp[1]) / 1000000.0])
                posTmp = row[14].__str__().split('|')
                posList.append([string.atof(posTmp[0]) / 1000000.0, string.atof(posTmp[1]) / 1000000.0])
                #����ﵽ400�����꣨posBlockSize = 400������ʼ����
                if(posList.__len__() >= ExcelExportConfig.posBlockSize):
                    self.__PassPos(posList, worksheet, posIndex, 7, 8, cellFormat)
                    posIndex += ExcelExportConfig.posBlockSize / 2
                    del posList[:]
                startIndex += 1
                row = cursorGPS.fetchone()
            
            #���ڲ���400������ĵ�������
            if(posList.__len__() > 0):
                self.__PassPos(posList, worksheet, posIndex, 7, 8, cellFormat)
                del posList[:]

    #������4Сʱ������ϸ
    def ExportFatigueDriveDetail(self, workbook, zoneId, vehicleType, platformId, govStatus, FuncVType, cellFormat):
        worksheet = workbook.add_worksheet('��4Сʱ����')

        # ��ͷ
        worksheet.write('A1', '������ҵ����', cellFormat)
        worksheet.write('B1', '���ƺ�', cellFormat)
        worksheet.write('C1', '��������', cellFormat)
        worksheet.write('D1', '������·������ҵ', cellFormat)
        worksheet.write('E1', '��4Сʱ���п�ʼʱ��', cellFormat)
        worksheet.write('F1', '����ʱ��', cellFormat)
        worksheet.write('G1', '����ʱ��', cellFormat)
        worksheet.write('H1', '��ʼλ��', cellFormat)
        worksheet.write('I1', '����λ��', cellFormat)
        worksheet.write('J1', '��װ������', cellFormat)

        cursorGPS = self.sqlconGPS.cursor()
        # if (self.vehicleType!=0):
            # cursorGPS.execute('SET NOCOUNT ON; EXEC SP_GOV_Stat_6BanFatigueDriveDetail_patch %d,%d,%d,0,%d,0,%d,1'
                          # ',\'AND 1=1\',1,1,10,400000' % (self.startDate, self.endDate, zoneId, self.vehicleType, platformId))
        # else:
        CarType = ConvertFuncVType(FuncVType,4)
        Filter = ConvertFuncVType(FuncVType,44)
        cursorGPS.execute('SET NOCOUNT ON; EXEC SP_GOV_Stat_6BanFatigueDriveDetail_patch %d,%d,%d,0,%d,0,%d,%d,1'
                          ',\'%s\',1,1,10,400000' % (self.startDate, self.endDate, zoneId, CarType, platformId, govStatus, Filter))
        row = cursorGPS.fetchone()
        # ����г�4Сʱ��ϸ��������excel����������
        if row:
            posList = []
            #�ӱ�ͷ����һ�п�ʼ��������
            startIndex = 1
            posIndex = 1
            companyDic = self.companyInZone[zoneId]
            while row:
                if(51000000 != zoneId):
                    vehicleNum = 0
                    if(row[6] in companyDic):
                        vehicleNum = companyDic[row[6]]
                    if(not row[1] in self.vehicleViolate):
                        vehicleNum += 1
                        self.vehicleViolate[row[1]] = True
                    companyDic[row[6]] = vehicleNum
                self.__WriteFatigueDriveDetail(worksheet, startIndex, row, cellFormat)
                #�����춯��ʼ��γ������ͽ�����γ������
                posTmp = row[13].__str__().split('|')
                posList.append([string.atof(posTmp[0]) / 1000000.0, string.atof(posTmp[1]) / 1000000.0])
                posTmp = row[14].__str__().split('|')
                posList.append([string.atof(posTmp[0]) / 1000000.0, string.atof(posTmp[1]) / 1000000.0])
                #����ﵽ400�����꣨posBlockSize = 400������ʼ����
                if(posList.__len__() >= ExcelExportConfig.posBlockSize):
                    self.__PassPos(posList, worksheet, posIndex, 7, 8, cellFormat)
                    posIndex += ExcelExportConfig.posBlockSize / 2
                    del posList[:]
                startIndex += 1
                row = cursorGPS.fetchone()
            
            #���ڲ���400������ĵ�������
            if(posList.__len__() > 0):
                self.__PassPos(posList, worksheet, posIndex, 7, 8, cellFormat)
                del posList[:]
                
                
    def UpdateOverSpeedDetail(self, speedLimit0, speedLimit1, topSpeed0, topSpeed1, distance0, distance1, duration):
        cursorGPS = self.sqlconGPS.cursor()
        cursorGPS.execute('SET NOCOUNT ON; EXEC UP_INSERT_OverspeedDetail_For6Ban %d,%d,%d,%d,%d,%d,%d,%d,%d'
                          %(self.startDate, self.endDate, speedLimit0, speedLimit1, topSpeed0,
                            topSpeed1, distance0, distance1, duration))

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
        shutil.copyfile(self.dataFolder+'\\'+self.tmpName+'.zip',self.dataFolderHGov+'\\'+self.tmpName+'.zip')
        return '%s%s' %(self.tmpName, '.zip')

    # ������������
    def __WriteOverSpeedDetail(self, worksheet, rowIndex, rowData, cellFormat):
        try:
            #������ҵ����
            worksheet.write(rowIndex, 0, rowData[3].decode('gbk', 'ignore'), cellFormat)
            #���ƺ�
            worksheet.write(rowIndex, 1, rowData[4].decode('gbk', 'ignore'), cellFormat)
            #��������
            worksheet.write(rowIndex, 2, rowData[5].decode('gbk', 'ignore'), cellFormat)
            #������·������ҵ
            worksheet.write(rowIndex, 3, rowData[7].decode('gbk', 'ignore'), cellFormat)
            #���ٿ�ʼʱ��
            worksheet.write(rowIndex, 4, rowData[13], cellFormat)
            #���ٽ���ʱ��
            worksheet.write(rowIndex, 5, rowData[14], cellFormat)
            #����ʱ��
            worksheet.write(rowIndex, 6, rowData[15], cellFormat)
            #���٣�km/h��
            worksheet.write(rowIndex, 7, rowData[11], cellFormat)
            #�ٶȣ�km/h��
            worksheet.write(rowIndex, 8, rowData[10], cellFormat)
            #�����ʣ�%��
            worksheet.write(rowIndex, 9, rowData[12], cellFormat)
            #��ʼλ��
            worksheet.write(rowIndex, 10, rowData[18], cellFormat)
            #����λ��
            worksheet.write(rowIndex, 11, rowData[19], cellFormat)
            #�Ƿ����
            worksheet.write(rowIndex, 12, rowData[20].decode('gbk'), cellFormat)
            #��װ������
            worksheet.write(rowIndex, 13, rowData[9].decode('gbk'), cellFormat)
            #���ݹ���	
            worksheet.write(rowIndex, 14, rowData[24], cellFormat)
        except Exception, e:
            self.Log(e.__str__())
        
    # �����춯����
    def __WriteBreakBanDetail(self, worksheet, rowIndex, rowData, cellFormat):
        try:
            #������ҵ����
            worksheet.write(rowIndex, 0, rowData[3].decode('gbk', 'ignore'), cellFormat)
            #���ƺ�
            worksheet.write(rowIndex, 1, rowData[4].decode('gbk', 'ignore'), cellFormat)
            #��������
            worksheet.write(rowIndex, 2, rowData[5].decode('gbk', 'ignore'), cellFormat)
            #������·������ҵ
            worksheet.write(rowIndex, 3, rowData[7].decode('gbk', 'ignore'), cellFormat)
            #��ʼʱ��
            worksheet.write(rowIndex, 4, rowData[10], cellFormat)
            #����ʱ��
            worksheet.write(rowIndex, 5, rowData[11], cellFormat)
            #����ʱ��
            worksheet.write(rowIndex, 6, rowData[12], cellFormat)
            #��ʼλ��
            worksheet.write(rowIndex, 7, rowData[13], cellFormat)
            #����λ��
            worksheet.write(rowIndex, 8, rowData[14], cellFormat)
            #��װ������
            worksheet.write(rowIndex, 9, rowData[9].decode('gbk'), cellFormat)
            #���ݹ���	
            worksheet.write(rowIndex, 10, rowData[18], cellFormat)
        except Exception, e:
            self.Log(e.__str__())
            
    # ������λ�ж�����
    def __WritePositionBreakDetail(self, worksheet, rowIndex, rowData, cellFormat):
        try:
            #������ҵ����
            worksheet.write(rowIndex, 0, rowData[3].decode('gbk', 'ignore'), cellFormat)
            #���ƺ�
            worksheet.write(rowIndex, 1, rowData[4].decode('gbk', 'ignore'), cellFormat)
            #��������
            worksheet.write(rowIndex, 2, rowData[5].decode('gbk', 'ignore'), cellFormat)
            #������·������ҵ
            worksheet.write(rowIndex, 3, rowData[7].decode('gbk', 'ignore'), cellFormat)
            #�ж�����ʱ��
            worksheet.write(rowIndex, 4, rowData[10], cellFormat)
            #�ָ�����ʱ��
            worksheet.write(rowIndex, 5, rowData[11], cellFormat)
            #����ʱ��
            worksheet.write(rowIndex, 6, rowData[12], cellFormat)
            #��ʼλ��
            worksheet.write(rowIndex, 7, rowData[13], cellFormat)
            #����λ��
            worksheet.write(rowIndex, 8, rowData[14], cellFormat)
            #��װ������
            worksheet.write(rowIndex, 9, rowData[9].decode('gbk'), cellFormat)
        except Exception, e:
            self.Log(e.__str__())
            
            
    # ������4Сʱ��������
    def __WriteFatigueDriveDetail(self, worksheet, rowIndex, rowData, cellFormat):
        try:
            #������ҵ����
            worksheet.write(rowIndex, 0, rowData[3].decode('gbk', 'ignore'), cellFormat)
            #���ƺ�
            worksheet.write(rowIndex, 1, rowData[4].decode('gbk', 'ignore'), cellFormat)
            #��������
            worksheet.write(rowIndex, 2, rowData[5].decode('gbk', 'ignore'), cellFormat)
            #������·������ҵ
            worksheet.write(rowIndex, 3, rowData[7].decode('gbk', 'ignore'), cellFormat)
            #��4Сʱ���п�ʼʱ��
            worksheet.write(rowIndex, 4, rowData[10], cellFormat)
            #����ʱ��
            worksheet.write(rowIndex, 5, rowData[11], cellFormat)
            #����ʱ��
            worksheet.write(rowIndex, 6, rowData[12], cellFormat)
            #��ʼλ��
            worksheet.write(rowIndex, 7, rowData[13], cellFormat)
            #����λ��
            worksheet.write(rowIndex, 8, rowData[14], cellFormat)
            #��װ������
            worksheet.write(rowIndex, 9, rowData[9].decode('gbk'), cellFormat)
        except Exception, e:
            self.Log(e.__str__())
            
     
    # �Դ���ľ�γ�������б���н���������������ĵ�ַд�뵽��Ӧ�ĵ�Ԫ���С�
    def __PassPos(self, posList, worksheet, startRow, startCol, endCol, cellFormat):
        resultList = []
        self.analyer.GetLocationData(posList, resultList)
        #��������ĵ�ַ���浽excel�������У�200����ʼλ�ã�200������λ��
        for rowIndex in range(0, resultList.__len__()):
            #ż��Ϊ��ʼλ��
            if 0 == rowIndex % 2:
                worksheet.write(startRow + rowIndex / 2, startCol, resultList[rowIndex].decode('gbk'), cellFormat)
            #����Ϊ����λ��
            else:
                worksheet.write(startRow + rowIndex / 2, endCol, resultList[rowIndex].decode('gbk'), cellFormat)
    
