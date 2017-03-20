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
import zipfile
from Manager.DataManager import LocationAnalyer
import sys
reload(sys)

sys.setdefaultencoding('gbk')
                
class ExcelExportBase(object):
    #存放导出数据的文件夹名
    dataFolder = 'D:\GPS_Server\HGov2\Export\Download'
    dataFolderHGov= 'D:\GPS_Server\WebGov_SC\Export\Download'
    def __init__(self, logObj, startDate, endDate, vehicleType, platformId, govStatus, FuncVType):
        self.companyInZone = {}
        self.vehicleViolate = {}
        self.logObj = logObj
        self.analyer = LocationAnalyer(self.logObj, ExcelExportConfig.mapEngineAddress)
        #参数
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

    #以ExcelExportBase.dataFolder为根目录创建文件夹
    def CreateFolder(self, folderName):
        fullName = '%s/%s' %(self.tmpFolder, folderName)
        if not os.path.exists(fullName):
            os.makedirs(fullName)

    #在self.tmpFolder下创建excel工作表
    def CreateWorkbook(self, wbName):
        return xlsxwriter.Workbook('%s/%s' %(self.tmpFolder, wbName))
        
    # 根据ZoneId获取应该在Excel报表中显示的地区名
    def GetZoneName(self, zoneId):
        zoneName = ExcelExportConfig.zoneDic[zoneId]
        if 51000000 == zoneId:
            zoneName += '省'
        elif zoneId > 51300000:
            zoneName += '州'
        else:
            zoneName += '市'
        
        return zoneName
        
    def Log(self, message):
        try:
            self.logObj.LogToFile(message + '\n')
            self.logObj.LogToShell(message.encode(ExcelExportConfig.envEncode) + '\n')
        except Exception, e:
            pass

    #导出超速明细
    def ExportOverSpeedDetail(self, workbook, zoneId, vehicleType, platformId, govStatus, FuncVType,  cellFormat):
        worksheet = workbook.add_worksheet('超速')

        # 表头
        worksheet.write('A1', '所属企业地区', cellFormat)
        worksheet.write('B1', '车牌号', cellFormat)
        worksheet.write('C1', '车辆类型', cellFormat)
        worksheet.write('D1', '所属道路运输企业', cellFormat)
        worksheet.write('E1', '超速开始时间', cellFormat)
        worksheet.write('F1', '超速结束时间', cellFormat)
        worksheet.write('G1', '持续时长', cellFormat)
        worksheet.write('H1', '限速（km/h）', cellFormat)
        worksheet.write('I1', '速度（km/h）', cellFormat)
        worksheet.write('J1', '超速率（%）', cellFormat)
        worksheet.write('K1', '开始位置', cellFormat)
        worksheet.write('L1', '结束位置', cellFormat)
        worksheet.write('M1', '是否高速', cellFormat)
        worksheet.write('N1', '安装服务商', cellFormat)
        worksheet.write('O1', '数据过滤', cellFormat)
        cursorGPS = self.sqlconGPS.cursor()
        CarType = ConvertFuncVType(FuncVType,1)
        Filter = ConvertFuncVType(FuncVType,11)
        cursorGPS.execute('SET NOCOUNT ON; EXEC SP_GOV_Stat_6BanOverSpeedDetail_patch %d,%d,%d,0,%d,0,%d,%d,1'
                          ',\'%s\',1,1,10,400000' % (self.startDate, self.endDate, zoneId, CarType, platformId, govStatus, Filter))
        row = cursorGPS.fetchone()
        # 如果有超速明细，则生成excel，导出数据
        if row:
            posList = []
            #从表头的下一行开始导出数据
            startIndex = 1
            posIndex = 1
            companyDic = self.companyInZone[zoneId]
            while row:
                if((row[20].decode('gbk') == '是' and row[12] >= 20) or row[12] >= 50):
                    if(51000000 != zoneId):
                        vehicleNum = 0
                        if(row[6] in companyDic):
                            vehicleNum = companyDic[row[6]]
                        if(not row[1] in self.vehicleViolate):
                            vehicleNum += 1
                            self.vehicleViolate[row[1]] = True
                        companyDic[row[6]] = vehicleNum
                    self.__WriteOverSpeedDetail(worksheet, startIndex, row, cellFormat)
                    #保存超速开始经纬度坐标和结束经纬度坐标
                    try:
                        posTmp = row[18].__str__().split('|')
                        posList.append([string.atof(posTmp[0]), string.atof(posTmp[1])])
                        posTmp = row[19].__str__().split('|')
                        posList.append([string.atof(posTmp[0]), string.atof(posTmp[1])])
                    except Exception, e:
                        self.Log(e.__str__())
                    #如果达到400个坐标（posBlockSize = 400），则开始解析
                    if(posList.__len__() >= ExcelExportConfig.posBlockSize):
                        self.__PassPos(posList, worksheet, posIndex, 10, 11, cellFormat)
                        posIndex += ExcelExportConfig.posBlockSize / 2
                        del posList[:]
                    startIndex += 1
                row = cursorGPS.fetchone()
            
            #对于不满400个坐标的单独处理
            if(posList.__len__() > 0):
                self.__PassPos(posList, worksheet, posIndex, 10, 11, cellFormat)
                del posList[:]

    #导出异动明细
    def ExportBreakBanDetail(self, workbook, zoneId, vehicleType, platformId, govStatus, FuncVType, cellFormat):
        worksheet = workbook.add_worksheet('异动')

        # 表头
        worksheet.write('A1', '所属企业地区', cellFormat)
        worksheet.write('B1', '车牌号', cellFormat)
        worksheet.write('C1', '车辆类型')
        worksheet.write('D1', '所属道路运输企业', cellFormat)
        worksheet.write('E1', '开始时间', cellFormat)
        worksheet.write('F1', '结束时间', cellFormat)
        worksheet.write('G1', '持续时长', cellFormat)
        worksheet.write('H1', '开始位置', cellFormat)
        worksheet.write('I1', '结束位置', cellFormat)
        worksheet.write('J1', '安装服务商', cellFormat)
        worksheet.write('K1', '数据过滤', cellFormat)

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
        # 如果有异动明细，则生成excel，导出数据
        if row:
            posList = []
            #从表头的下一行开始导出数据
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
                #保存异动开始经纬度坐标和结束经纬度坐标
                posTmp = row[13].__str__().split('|')
                posList.append([string.atof(posTmp[0]) / 1000000.0, string.atof(posTmp[1]) / 1000000.0])
                posTmp = row[14].__str__().split('|')
                posList.append([string.atof(posTmp[0]) / 1000000.0, string.atof(posTmp[1]) / 1000000.0])
                #如果达到400个坐标（posBlockSize = 400），则开始解析
                if(posList.__len__() >= ExcelExportConfig.posBlockSize):
                    self.__PassPos(posList, worksheet, posIndex, 7, 8, cellFormat)
                    posIndex += ExcelExportConfig.posBlockSize / 2
                    del posList[:]
                startIndex += 1
                row = cursorGPS.fetchone()
            
            #对于不满400个坐标的单独处理
            if(posList.__len__() > 0):
                self.__PassPos(posList, worksheet, posIndex, 7, 8, cellFormat)
                del posList[:]

     #导出定位中断明细
    def ExportPositionBreakDetail(self, workbook, zoneId, vehicleType, platformId, govStatus, FuncVType, cellFormat):
        worksheet = workbook.add_worksheet('持续半小时无数据上传')

        # 表头
        worksheet.write('A1', '所属企业地区', cellFormat)
        worksheet.write('B1', '车牌号', cellFormat)
        worksheet.write('C1', '车辆类型', cellFormat)
        worksheet.write('D1', '所属道路运输企业', cellFormat)
        worksheet.write('E1', '中断数据时间', cellFormat)
        worksheet.write('F1', '恢复数据时间', cellFormat)
        worksheet.write('G1', '持续时长', cellFormat)
        worksheet.write('H1', '开始位置', cellFormat)
        worksheet.write('I1', '结束位置', cellFormat)
        worksheet.write('J1', '安装服务商', cellFormat)

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
        # 如果有定位中断明细，则生成excel，导出数据
        if row:
            posList = []
            #从表头的下一行开始导出数据
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
                #保存异动开始经纬度坐标和结束经纬度坐标
                posTmp = row[13].__str__().split('|')
                posList.append([string.atof(posTmp[0]) / 1000000.0, string.atof(posTmp[1]) / 1000000.0])
                posTmp = row[14].__str__().split('|')
                posList.append([string.atof(posTmp[0]) / 1000000.0, string.atof(posTmp[1]) / 1000000.0])
                #如果达到400个坐标（posBlockSize = 400），则开始解析
                if(posList.__len__() >= ExcelExportConfig.posBlockSize):
                    self.__PassPos(posList, worksheet, posIndex, 7, 8, cellFormat)
                    posIndex += ExcelExportConfig.posBlockSize / 2
                    del posList[:]
                startIndex += 1
                row = cursorGPS.fetchone()
            
            #对于不满400个坐标的单独处理
            if(posList.__len__() > 0):
                self.__PassPos(posList, worksheet, posIndex, 7, 8, cellFormat)
                del posList[:]

    #导出超4小时运行明细
    def ExportFatigueDriveDetail(self, workbook, zoneId, vehicleType, platformId, govStatus, FuncVType, cellFormat):
        worksheet = workbook.add_worksheet('超4小时运行')

        # 表头
        worksheet.write('A1', '所属企业地区', cellFormat)
        worksheet.write('B1', '车牌号', cellFormat)
        worksheet.write('C1', '车辆类型', cellFormat)
        worksheet.write('D1', '所属道路运输企业', cellFormat)
        worksheet.write('E1', '超4小时运行开始时间', cellFormat)
        worksheet.write('F1', '结束时间', cellFormat)
        worksheet.write('G1', '持续时长', cellFormat)
        worksheet.write('H1', '开始位置', cellFormat)
        worksheet.write('I1', '结束位置', cellFormat)
        worksheet.write('J1', '安装服务商', cellFormat)

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
        # 如果有超4小时明细，则生成excel，导出数据
        if row:
            posList = []
            #从表头的下一行开始导出数据
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
                #保存异动开始经纬度坐标和结束经纬度坐标
                posTmp = row[13].__str__().split('|')
                posList.append([string.atof(posTmp[0]) / 1000000.0, string.atof(posTmp[1]) / 1000000.0])
                posTmp = row[14].__str__().split('|')
                posList.append([string.atof(posTmp[0]) / 1000000.0, string.atof(posTmp[1]) / 1000000.0])
                #如果达到400个坐标（posBlockSize = 400），则开始解析
                if(posList.__len__() >= ExcelExportConfig.posBlockSize):
                    self.__PassPos(posList, worksheet, posIndex, 7, 8, cellFormat)
                    posIndex += ExcelExportConfig.posBlockSize / 2
                    del posList[:]
                startIndex += 1
                row = cursorGPS.fetchone()
            
            #对于不满400个坐标的单独处理
            if(posList.__len__() > 0):
                self.__PassPos(posList, worksheet, posIndex, 7, 8, cellFormat)
                del posList[:]
                
                
    def UpdateOverSpeedDetail(self, speedLimit0, speedLimit1, topSpeed0, topSpeed1, distance0, distance1, duration):
        cursorGPS = self.sqlconGPS.cursor()
        cursorGPS.execute('SET NOCOUNT ON; EXEC UP_INSERT_OverspeedDetail_For6Ban %d,%d,%d,%d,%d,%d,%d,%d,%d'
                          %(self.startDate, self.endDate, speedLimit0, speedLimit1, topSpeed0,
                            topSpeed1, distance0, distance1, duration))

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
    def __WriteOverSpeedDetail(self, worksheet, rowIndex, rowData, cellFormat):
        try:
            #所属企业地区
            worksheet.write(rowIndex, 0, rowData[3].decode('gbk', 'ignore'), cellFormat)
            #车牌号
            worksheet.write(rowIndex, 1, rowData[4].decode('gbk', 'ignore'), cellFormat)
            #车辆类型
            worksheet.write(rowIndex, 2, rowData[5].decode('gbk', 'ignore'), cellFormat)
            #所属道路运输企业
            worksheet.write(rowIndex, 3, rowData[7].decode('gbk', 'ignore'), cellFormat)
            #超速开始时间
            worksheet.write(rowIndex, 4, rowData[13], cellFormat)
            #超速结束时间
            worksheet.write(rowIndex, 5, rowData[14], cellFormat)
            #持续时长
            worksheet.write(rowIndex, 6, rowData[15], cellFormat)
            #限速（km/h）
            worksheet.write(rowIndex, 7, rowData[11], cellFormat)
            #速度（km/h）
            worksheet.write(rowIndex, 8, rowData[10], cellFormat)
            #超速率（%）
            worksheet.write(rowIndex, 9, rowData[12], cellFormat)
            #开始位置
            worksheet.write(rowIndex, 10, rowData[18], cellFormat)
            #结束位置
            worksheet.write(rowIndex, 11, rowData[19], cellFormat)
            #是否高速
            worksheet.write(rowIndex, 12, rowData[20].decode('gbk'), cellFormat)
            #安装服务商
            worksheet.write(rowIndex, 13, rowData[9].decode('gbk'), cellFormat)
            #数据过滤	
            worksheet.write(rowIndex, 14, rowData[24], cellFormat)
        except Exception, e:
            self.Log(e.__str__())
        
    # 导出异动数据
    def __WriteBreakBanDetail(self, worksheet, rowIndex, rowData, cellFormat):
        try:
            #所属企业地区
            worksheet.write(rowIndex, 0, rowData[3].decode('gbk', 'ignore'), cellFormat)
            #车牌号
            worksheet.write(rowIndex, 1, rowData[4].decode('gbk', 'ignore'), cellFormat)
            #车辆类型
            worksheet.write(rowIndex, 2, rowData[5].decode('gbk', 'ignore'), cellFormat)
            #所属道路运输企业
            worksheet.write(rowIndex, 3, rowData[7].decode('gbk', 'ignore'), cellFormat)
            #开始时间
            worksheet.write(rowIndex, 4, rowData[10], cellFormat)
            #结束时间
            worksheet.write(rowIndex, 5, rowData[11], cellFormat)
            #持续时长
            worksheet.write(rowIndex, 6, rowData[12], cellFormat)
            #开始位置
            worksheet.write(rowIndex, 7, rowData[13], cellFormat)
            #结束位置
            worksheet.write(rowIndex, 8, rowData[14], cellFormat)
            #安装服务商
            worksheet.write(rowIndex, 9, rowData[9].decode('gbk'), cellFormat)
            #数据过滤	
            worksheet.write(rowIndex, 10, rowData[18], cellFormat)
        except Exception, e:
            self.Log(e.__str__())
            
    # 导出定位中断数据
    def __WritePositionBreakDetail(self, worksheet, rowIndex, rowData, cellFormat):
        try:
            #所属企业地区
            worksheet.write(rowIndex, 0, rowData[3].decode('gbk', 'ignore'), cellFormat)
            #车牌号
            worksheet.write(rowIndex, 1, rowData[4].decode('gbk', 'ignore'), cellFormat)
            #车辆类型
            worksheet.write(rowIndex, 2, rowData[5].decode('gbk', 'ignore'), cellFormat)
            #所属道路运输企业
            worksheet.write(rowIndex, 3, rowData[7].decode('gbk', 'ignore'), cellFormat)
            #中断数据时间
            worksheet.write(rowIndex, 4, rowData[10], cellFormat)
            #恢复数据时间
            worksheet.write(rowIndex, 5, rowData[11], cellFormat)
            #持续时长
            worksheet.write(rowIndex, 6, rowData[12], cellFormat)
            #开始位置
            worksheet.write(rowIndex, 7, rowData[13], cellFormat)
            #结束位置
            worksheet.write(rowIndex, 8, rowData[14], cellFormat)
            #安装服务商
            worksheet.write(rowIndex, 9, rowData[9].decode('gbk'), cellFormat)
        except Exception, e:
            self.Log(e.__str__())
            
            
    # 导出超4小时运行数据
    def __WriteFatigueDriveDetail(self, worksheet, rowIndex, rowData, cellFormat):
        try:
            #所属企业地区
            worksheet.write(rowIndex, 0, rowData[3].decode('gbk', 'ignore'), cellFormat)
            #车牌号
            worksheet.write(rowIndex, 1, rowData[4].decode('gbk', 'ignore'), cellFormat)
            #车辆类型
            worksheet.write(rowIndex, 2, rowData[5].decode('gbk', 'ignore'), cellFormat)
            #所属道路运输企业
            worksheet.write(rowIndex, 3, rowData[7].decode('gbk', 'ignore'), cellFormat)
            #超4小时运行开始时间
            worksheet.write(rowIndex, 4, rowData[10], cellFormat)
            #结束时间
            worksheet.write(rowIndex, 5, rowData[11], cellFormat)
            #持续时长
            worksheet.write(rowIndex, 6, rowData[12], cellFormat)
            #开始位置
            worksheet.write(rowIndex, 7, rowData[13], cellFormat)
            #结束位置
            worksheet.write(rowIndex, 8, rowData[14], cellFormat)
            #安装服务商
            worksheet.write(rowIndex, 9, rowData[9].decode('gbk'), cellFormat)
        except Exception, e:
            self.Log(e.__str__())
            
     
    # 对传入的经纬度坐标列表进行解析，并将解析后的地址写入到对应的单元格中。
    def __PassPos(self, posList, worksheet, startRow, startCol, endCol, cellFormat):
        resultList = []
        self.analyer.GetLocationData(posList, resultList)
        #将解析后的地址保存到excel导出表中，200个开始位置，200个结束位置
        for rowIndex in range(0, resultList.__len__()):
            #偶数为开始位置
            if 0 == rowIndex % 2:
                worksheet.write(startRow + rowIndex / 2, startCol, resultList[rowIndex].decode('gbk'), cellFormat)
            #奇数为结束位置
            else:
                worksheet.write(startRow + rowIndex / 2, endCol, resultList[rowIndex].decode('gbk'), cellFormat)
    
