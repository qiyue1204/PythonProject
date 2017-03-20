# coding=gb2312

import string
import ExcelExportConfig
from ExcelExportBase import ExcelExportBase
from Support.ExcelExport.Convert import ConvertFuncVType
from Support.ExcelExport.Convert import VTypeStrSplit
from HistoryTrace import HistoryTrace
import Conf
import sys
reload(sys)

sys.setdefaultencoding('gbk')

class SixBanOverSpeedAndBreakBan(ExcelExportBase):
    #����Υ����ϸ
    detailFolder = 'Υ����ϸ'.encode(ExcelExportConfig.envEncode)
    def __init__(self, logObj, startDate, endDate, vehicleType, platformId, govStatus, FuncVType):
        super(SixBanOverSpeedAndBreakBan, self).__init__(logObj, startDate, endDate, vehicleType, platformId, govStatus, FuncVType) #super�̳�
        self.CreateFolder(SixBanOverSpeedAndBreakBan.detailFolder)

    def __del__(self):
        super(SixBanOverSpeedAndBreakBan, self).__del__()

    def ExportSum(self):
        self.Log('Start to export six ban over speed and break ban summary for all')
        timeSpan = 'ͳ��ʱ�Σ�%d��%d' % (self.startDate, self.endDate)
        #print timeSpan
        s=''
        if (VTypeStrSplit(self.FuncVType,1)!=0):
            s=s+'����'
        if (VTypeStrSplit(self.FuncVType,2)!=0):
            s=s+'�춯' 
        if (VTypeStrSplit(self.FuncVType,3)!=0):
            s=s+'������Сʱ�������ϴ�'
        if (VTypeStrSplit(self.FuncVType,4)!=0):
            s=s+'��4Сʱ����'
        #s=s[:-1]
        #print s
        workbook = self.CreateWorkbook('ȫʡ���Ƕ�λϵͳ������̬ͳ�Ʊ���(%d-%d_����%s).xlsx'.encode(ExcelExportConfig.envEncode) %(self.startDate, self.endDate, s))
        #print 'ȫʡ���Ƕ�λϵͳ������̬ͳ�Ʊ���(%d-%d_����%s).xlsx'%(self.startDate, self.endDate, s)
        #�����ʽ
        self.titleFormat = workbook.add_format({
                                            'bold': True,
                                            'align': 'center',
                                            'valign': 'vcenter',
                                            'font_size': 14
                                            })
        #���и�ʽ
        self.centerFormat = workbook.add_format({
                                            'align': 'center',
                                            'valign': 'vcenter',
                                            'text_wrap': True,
                                            'border': 1,
                                            'font_size': 10
                                            })

        #�����ޱ߿��ʽ
        self.centerNoBorder = workbook.add_format({
                                            'align': 'center',
                                            'valign': 'vcenter',
                                            'font_size': 10
                                            })

        #�ٷ�����ʽ
        self.percentageFormat = workbook.add_format({
                                            'align': 'center',
                                            'valign': 'vcenter',
                                            'text_wrap': True,
                                            'border': 1,
                                            'font_size': 10,
                                            'num_format': '0.00%'
                                            })

        #�߿��ʽ
        self.borderFormat = workbook.add_format({
                                            'border': 1,
                                            'font_size': 10,
                                            'text_wrap': True
                                            })

        #������ʽ
        self.descriptionFormat = workbook.add_format({
                                            'text_wrap': True,
                                            'font_size': 10
                                            })

        wsAll = workbook.add_worksheet('ȫʡͳ�Ʊ�')
        # wsAll.set_row(1, 28.5)
        i=0
        if (VTypeStrSplit(self.FuncVType,1)!=0):
            wsAll.set_column(3, 4, 7)
            wsAll.set_column(5, 5, 9)
            wsAll.set_column(6, 6, 11)
            wsAll.set_column(7, 7, 9)
            wsAll.set_column(8, 8, 11)
            wsAll.merge_range(3, 3, 3, 8, '����', self.centerFormat)
            wsAll.merge_range(4, 3, 5, 3, 'Υ�³�����', self.centerFormat)
            wsAll.merge_range(4, 4, 5, 4, 'Υ�³�������', self.centerFormat)
            wsAll.merge_range(4, 5, 4, 6, '����', self.centerFormat)
            wsAll.merge_range(4, 7, 4, 8, 'ҹ��(�������ռ��80%)', self.centerFormat)
            wsAll.write(5, 5, '���١�20%', self.centerFormat)
            wsAll.write(5, 6, '�Ǹ��١�50%', self.centerFormat)
            wsAll.write(5, 7, '���١�20%', self.centerFormat)
            wsAll.write(5, 8, '�Ǹ��١�50%', self.centerFormat)
        else:
            i=i+6
        if (VTypeStrSplit(self.FuncVType,2)!=0):
            wsAll.set_column(10-i, 10-i, 6)
            wsAll.set_column(11-i, 11-i, 10)
            wsAll.merge_range(3, 9-i, 4, 11-i, '�賿2-5��Υ������', self.centerFormat)
            wsAll.write(5, 9-i, 'Υ�³�����', self.centerFormat)
            wsAll.write(5, 10-i, '����', self.centerFormat)
            wsAll.write(5, 11-i, 'Υ�³�������', self.centerFormat)
        else:
            i=i+3
        if (VTypeStrSplit(self.FuncVType,3)!=0):
            wsAll.set_column(13-i, 13-i, 6)
            wsAll.set_column(14-i, 14-i, 10)
            wsAll.merge_range(3, 12-i, 4, 14-i, '������Сʱ�������ϴ�', self.centerFormat)
            wsAll.write(5, 12-i, 'Υ�³�����', self.centerFormat)
            wsAll.write(5, 13-i, '����', self.centerFormat)
            wsAll.write(5, 14-i, 'Υ�³�������', self.centerFormat)
        else:
            i=i+3
        if (VTypeStrSplit(self.FuncVType,4)!=0):
            wsAll.set_column(16-i, 16-i, 6)
            wsAll.set_column(17-i, 17-i, 10)
            wsAll.merge_range(3, 15-i, 4, 17-i, '��4Сʱ����', self.centerFormat)
            wsAll.write(5, 15-i, 'Υ�³�����', self.centerFormat)
            wsAll.write(5, 16-i, '����', self.centerFormat)
            wsAll.write(5, 17-i, 'Υ�³�������', self.centerFormat)
        else:
            i=i+3
        # print i
        wsAll.set_row(1, 24)
        wsAll.set_column(0, 0, 8)
        wsAll.set_column(1, 2, 7)
        wsAll.set_column(18-i, 19-i, 8)
        wsAll.write('A1', '������')
        wsAll.merge_range(1, 0, 1, 19-i, 'ȫʡ���Ƕ�λϵͳ���˳�����̬ͳ�Ʊ���', self.titleFormat)
        wsAll.write('A3', timeSpan)
        wsAll.merge_range(2, 18-i, 2, 19-i, '��λ����/��', self.centerNoBorder)
        wsAll.merge_range(3, 0, 5, 0, '����', self.centerFormat)
        wsAll.merge_range(3, 1, 5, 1, '������װ����', self.centerFormat)
        wsAll.merge_range(3, 2, 5, 2, '������', self.centerFormat)
        wsAll.merge_range(3, 18-i, 5, 18-i, 'Υ����Ϊ�������ϼ�', self.centerFormat)
        wsAll.merge_range(3, 19-i, 5, 19-i, 'Υ����Ϊ�����ϼ�', self.centerFormat)
        wsAll.freeze_panes(6, 0)
        wsAll.set_tab_color('red')


        # �ӱ�ͷ����һ�п�ʼ��������
        startRow = ExcelExportConfig.headerLineNumber
        zoneIdList = []

        cursorGPS = self.sqlconGPS.cursor()
        # if (self.vehicleType!=0): 
            # self.logObj.LogToFile('SET NOCOUNT ON; exec SP_GOV_Stat_6BanZone_patch %d, %d, 51000000,\'\', %d, 0, %d, 0, 1, 1,0, 0, 0, 0' % (self.startDate, self.endDate,self.vehicleType, self.platformId)) 
            # cursorGPS.execute('SET NOCOUNT ON; exec SP_GOV_Stat_6BanZone_patch %d, %d, 51000000, \'\', %d, 0, %d, 0, 1, 1,'
                            # '0, 0, 0, 0' % (self.startDate, self.endDate,self.vehicleType, self.platformId))
        # else: 
            # cursorGPS.execute('SET NOCOUNT ON; exec SP_GOV_Stat_6BanZone_patch %d, %d, 51000000,\'%s\', %d, 0, %d, 0, 1, 1,'
                            # '0, 0, 0, 0' %(self.startDate,self.endDate,self.FuncVType,self.vehicleType,self.platformId)) 
        cursorGPS.execute('SET NOCOUNT ON; exec SP_GOV_Stat_6BanZone_patch %d, %d, 51000000,\'%s\', %d, 0, %d,%d, 0, 1, 1,'
                            '0, 0, 0, 0' %(self.startDate,self.endDate,self.FuncVType,self.vehicleType,self.platformId,self.govStatus))                         
        row = cursorGPS.fetchone()
        while row:
                self.__WriteDataAll(wsAll, startRow, row)
                zoneIdList.append(row[0])
                startRow += 1;
                row = cursorGPS.fetchone()

        # �����ϼ�����
        cursorGPS.nextset()
        cursorGPS.nextset()
        row = cursorGPS.fetchone()
        self.__WriteSumAll(wsAll, startRow, row)

        # �������ű��˵��
        description = '˵����1.������װ������ʡ�����ƽ̨������ҵ��ϵͳ��Ҫ��Ϣ��ȫ�ĳ���ƥ��һ�µĳ�������' \
                      '2.��ҵ������ֻͳ����Υ��Υ�³�������ҵ'
        wsAll.merge_range(startRow + 1, 0, startRow + 1, 19-i, description, self.descriptionFormat)

        # ��ÿһ������������ (ʡ������)���Ƕ�λϵͳ������̬ͳ�Ʊ��� ������
        for zoneId in zoneIdList:
            self.Log('Start to export six ban over speed and break ban summary for %s, zoneID: %d.'
                     %(ExcelExportConfig.zoneDic[zoneId], zoneId))
            wsZone = workbook.add_worksheet(ExcelExportConfig.zoneDic[zoneId])
            # ���Ʊ�ͷ
            j=0
            if (VTypeStrSplit(self.FuncVType,1)!=0):
                wsZone.set_column(4, 4, 4.5)
                wsZone.set_column(5, 5, 6.5)
                wsZone.set_column(6, 9, 6)
                wsZone.merge_range(3, 4, 3, 9, '����', self.centerFormat)
                wsZone.merge_range(4, 4, 5, 4, 'Υ�³�����', self.centerFormat)
                wsZone.merge_range(4, 5, 5, 5, 'Υ�³�������', self.centerFormat)
                wsZone.merge_range(4, 6, 4, 7, '����', self.centerFormat)
                wsZone.merge_range(4, 8, 4, 9, 'ҹ��(�������ռ��80%)', self.centerFormat)
                wsZone.write(5, 6, '���١�20%', self.centerFormat)
                wsZone.write(5, 7, '�Ǹ��١�50%', self.centerFormat)
                wsZone.write(5, 8, '���١�20%', self.centerFormat)
                wsZone.write(5, 9, '�Ǹ��١�50%', self.centerFormat)
            else:
                j=j+6
            if (VTypeStrSplit(self.FuncVType,2)!=0):
                wsZone.set_column(10-j, 10-j, 5.5)
                wsZone.set_column(11-j, 11-j, 4.5)
                wsZone.set_column(12-j, 12-j, 6.5)
                wsZone.merge_range(3, 10-j, 4, 12-j, '�賿2-5��Υ������', self.centerFormat)
                wsZone.write(5, 10-j, 'Υ�³�����', self.centerFormat)
                wsZone.write(5, 11-j, '����', self.centerFormat)
                wsZone.write(5, 12-j, 'Υ�³�������', self.centerFormat)    
            else:
                j=j+3
            if (VTypeStrSplit(self.FuncVType,3)!=0):
                wsZone.set_column(13-j, 13-j, 5.5)
                wsZone.set_column(14-j, 14-j, 4.5)
                wsZone.set_column(15-j, 15-j, 6.5)
                wsZone.merge_range(3, 13-j, 4, 15-j, '������Сʱ�������ϴ�', self.centerFormat)
                wsZone.write(5, 13-j, 'Υ�³�����', self.centerFormat)
                wsZone.write(5, 14-j, '����', self.centerFormat)
                wsZone.write(5, 15-j, 'Υ�³�������', self.centerFormat)
            else:
                j=j+3
            if (VTypeStrSplit(self.FuncVType,4)!=0):
                wsZone.set_column(16-j, 16-j, 5.5)
                wsZone.set_column(17-j, 17-j, 4.5)
                wsZone.set_column(18-j, 18-j, 6.5)
                wsZone.merge_range(3, 16-j, 4, 18-j, '��4Сʱ����', self.centerFormat)
                wsZone.write(5, 16-j, 'Υ�³�����', self.centerFormat)
                wsZone.write(5, 17-j, '����', self.centerFormat)
                wsZone.write(5, 18-j, 'Υ�³�������', self.centerFormat)
            else:
                j=j+3
    
            wsZone.set_row(1, 25.5)
            wsZone.set_row(4, 24)
            wsZone.set_column(0, 0, 4)
            wsZone.set_column(1, 1, 44)
            wsZone.set_column(2, 2, 5.5)
            wsZone.set_column(3, 3, 6.5)
            wsZone.set_column(19-j, 20-j, 5)
            wsZone.write('A1', '������')
            wsZone.merge_range(1, 0, 1, 20-j, '%s ���Ƕ�λϵͳ���˳�����̬ͳ�Ʊ���'
                               %self.GetZoneName(zoneId), self.titleFormat)
            wsZone.write('A3', timeSpan)
            wsZone.merge_range(2, 19-j, 2, 20-j, '��λ����/��', self.centerNoBorder)
            wsZone.merge_range(3, 0, 5, 0, '���', self.centerFormat)
            wsZone.merge_range(3, 1, 5, 1, '������ҵ', self.centerFormat)
            wsZone.merge_range(3, 2, 5, 2, '������װ����', self.centerFormat)
            wsZone.merge_range(3, 3, 5, 3, '������', self.centerFormat)
            wsZone.merge_range(3, 19-j, 5, 19-j, 'Υ����Ϊ�������ϼ�', self.centerFormat)
            wsZone.merge_range(3, 20-j, 5, 20-j, 'Υ����Ϊ�����ϼ�', self.centerFormat)
            wsZone.freeze_panes(6, 0)
            wsZone.set_tab_color('yellow')
    

            # �ӱ�ͷ����һ�п�ʼ����
            startRow = ExcelExportConfig.headerLineNumber
            # if (self.vehicleType!=0):
                # cursorGPS.execute('SET NOCOUNT ON; EXEC SP_GOV_Stat_6BanCompany_patch %d,%d,%d,\'\',%d,0,%d,0,1,1,'
                              # '\'AND 1=1\',0,0,0,0' % (self.startDate, self.endDate, zoneId,self.vehicleType, self.platformId))
            # else:
                 # cursorGPS.execute('SET NOCOUNT ON; EXEC SP_GOV_Stat_6BanCompany_patch %d,%d,%d,\'%s\',%d,0,%d,0,1,1,'
                              # '\'AND 1=1\',0,0,0,0' % (self.startDate, self.endDate, zoneId,self.FuncVType,self.vehicleType, self.platformId))   
            cursorGPS.execute('SET NOCOUNT ON; EXEC SP_GOV_Stat_6BanCompany_patch %d,%d,%d,\'%s\',%d,0,%d,%d,0,1,1,'
                              '\'AND 1=1\',0,0,0,0' % (self.startDate, self.endDate, zoneId,self.FuncVType,self.vehicleType, self.platformId, self.govStatus)) 
                             
            row = cursorGPS.fetchone()
            while row:
                #ֻ�������ٺ��춯��Υ��
                t1=row[8]
                t2=row[9]
                t3=row[10]
                t4=row[11]
                t5=row[13]
                t6=row[16]
                t7=row[19]
                if (VTypeStrSplit(self.FuncVType,1)==0):                  
                   row[8]=0
                   row[9]=0
                   row[10]=0
                   row[11]=0
                if (VTypeStrSplit(self.FuncVType,2)==0):                   
                   row[13]=0
                if (VTypeStrSplit(self.FuncVType,3)==0):                   
                   row[16]=0
                if (VTypeStrSplit(self.FuncVType,4)==0):                  
                   row[19]=0
                if (row[8] > 0 or row[9] > 0 or row[10] > 0 or row[11] > 0 or row[13] > 0 or row[16] > 0 or row[19] > 0):
                    row[8]=t1
                    row[9]=t2
                    row[10]=t3
                    row[11]=t4
                    row[13]=t5
                    row[16]=t6
                    row[19]=t7
                    self.__WriteDataZone(wsZone, startRow, row)
                    startRow += 1;
                row = cursorGPS.fetchone()

            if startRow > ExcelExportConfig.headerLineNumber:
                # �����ϼ�����
                cursorGPS.nextset()
                if(Conf.isProdEnv):
                    cursorGPS.nextset()
                row = cursorGPS.fetchone()
                self.__WriteSumZone(wsZone, startRow, row)
        workbook.close()
        
    def ExportVehicle(self):
        self.Log('Export vehicle.\n')
        workbook = self.CreateWorkbook('���˳���Υ�����Ͻ����ܱ�.xlsx'.encode(ExcelExportConfig.envEncode))

        #�����ʽ
        titleFormat = workbook.add_format({
                                            'bold': True,
                                            'align': 'center',
                                            'valign': 'vcenter',
                                            'font_size': 16
                                            })
        #���и�ʽ
        centerFormat = workbook.add_format({
                                            'align': 'center',
                                            'valign': 'vcenter',
                                            'text_wrap': True,
                                            'border': 1,
                                            'font_size': 10
                                            })
        wsVehicle = workbook.add_worksheet('�������ܱ�')
              
        m=0
        if (VTypeStrSplit(self.FuncVType,1)!=0):
            wsVehicle.set_column(4, 7, 6)
            wsVehicle.merge_range(1, 4, 1, 7, '����', centerFormat)
            wsVehicle.merge_range(2, 4, 2, 5, '����', centerFormat)
            wsVehicle.merge_range(2, 6, 2, 7, 'ҹ��(�������ռ��80%)', centerFormat)
            wsVehicle.write(3, 4, '���١�20%', centerFormat)
            wsVehicle.write(3, 5, '�Ǹ��١�50%', centerFormat)
            wsVehicle.write(3, 6, '���١�20%', centerFormat)
            wsVehicle.write(3, 7, '�Ǹ��١�50%', centerFormat)
        else:
            m=m+4
        if (VTypeStrSplit(self.FuncVType,2)!=0):
            wsVehicle.set_column(8-m, 8-m, 6)
            wsVehicle.merge_range(1, 8-m, 2, 8-m, '�賿2-5��Υ������', centerFormat)
            wsVehicle.write(3, 8-m, '����', centerFormat)
        else:
            m=m+1
        if (VTypeStrSplit(self.FuncVType,3)!=0):
            wsVehicle.set_column(9-m, 9-m, 6)
            wsVehicle.merge_range(1, 9-m, 2, 9-m, '������Сʱ�������ϴ�', centerFormat)
            wsVehicle.write(3, 9-m, '����', centerFormat)
        else:
            m=m+1
        if (VTypeStrSplit(self.FuncVType,4)!=0):
            wsVehicle.set_column(10-m, 10-m, 6)
            wsVehicle.merge_range(1, 10-m, 2, 10-m, '��4Сʱ����', centerFormat)
            wsVehicle.write(3, 10-m, '����', centerFormat)
        else:
            m=m+1
        # print i
        wsVehicle.set_row(0, 35)
        wsVehicle.set_row(2, 24)
        wsVehicle.set_row(3, 24)
        wsVehicle.set_column(0, 0, 15)
        wsVehicle.set_column(1, 1, 11)
        wsVehicle.set_column(2, 2, 50)
        wsVehicle.set_column(3, 3, 8.5)
        wsVehicle.merge_range(0, 0, 0, 11-m, '���˳���Υ�����Ͻ����ܱ�', titleFormat)
        wsVehicle.merge_range(1, 0, 3, 0, '����', centerFormat)
        wsVehicle.merge_range(1, 1, 3, 1, '����', centerFormat)
        wsVehicle.merge_range(1, 2, 3, 2, '������ҵ', centerFormat)
        wsVehicle.merge_range(1, 3, 3, 3, '������', centerFormat)      
        wsVehicle.merge_range(1, 11-m, 3, 11-m, 'Υ����Ϊ�����ϼ�', centerFormat)
        wsVehicle.freeze_panes(4, 0)
        
        
        cursorGPS = self.sqlconGPS.cursor()
        #cursorGPS.execute('SET NOCOUNT ON; EXEC SP_GOV_Stat_6BanVehicle_Re %d,%d,51000000,0,%d,0,%d,1,0,0,0,0'
        #                  % (self.startDate, self.endDate, self.vehicleType, self.platformId))
        # if (self.vehicleType!=0):
            # cursorGPS.execute('SET NOCOUNT ON; EXEC SP_GOV_Stat_6BanVehicle_patch %d,%d,51000000,\'\',0,%d,0,%d,0,1,0,0,0,0'
                          # % (self.startDate, self.endDate,self.vehicleType, self.platformId)) 
        # else:
            # cursorGPS.execute('SET NOCOUNT ON; EXEC SP_GOV_Stat_6BanVehicle_patch %d,%d,51000000,\'%s\',0,%d,0,%d,0,1,0,0,0,0'
                          # % (self.startDate, self.endDate,self.FuncVType,self.vehicleType, self.platformId))    
        cursorGPS.execute('SET NOCOUNT ON; EXEC SP_GOV_Stat_6BanVehicle_patch %d,%d,51000000,\'%s\',0,%d,0,%d,%d,0,1,0,0,0,0'
                          % (self.startDate, self.endDate,self.FuncVType,self.vehicleType, self.platformId, self.govStatus))                         
        row = cursorGPS.fetchone()

        rowIndex = 4
        # �������ϸ��������excel����������
        #singlevehicletotal1=0
        #singlevehicletotal2=0
        #singlevehicletotal3=0
        #singlevehicletotal4=0
        #singlevehicletotal5=0
        #singlevehicletotal6=0
        #singlevehicletotal7=0
        #singlevehicletotal8=0
        if row:
            while row:
                t8=row[6]
                t9=row[7]
                t10=row[8]
                t11=row[9]
                t12=row[10]
                t13=row[11]
                t14=row[12]
                if (VTypeStrSplit(self.FuncVType,1)==0):                  
                   row[6]=0
                   row[7]=0
                   row[8]=0
                   row[9]=0
                if (VTypeStrSplit(self.FuncVType,2)==0):                   
                   row[10]=0
                if (VTypeStrSplit(self.FuncVType,3)==0):                   
                   row[11]=0
                if (VTypeStrSplit(self.FuncVType,4)==0):                  
                   row[12]=0
                if(row[6] > 0 or row[7] > 0 or row[8] > 0 or row[9] > 0 or row[10] > 0 or row[11] > 0 or row[12] > 0):
                    row[6]=t8
                    row[7]=t9
                    row[8]=t10
                    row[9]=t11
                    row[10]=t12
                    row[11]=t13
                    row[12]=t14
                    #����
                    wsVehicle.write(rowIndex, 0, row[1].decode('gbk', 'ignore'), centerFormat)
                    #����
                    wsVehicle.write(rowIndex, 1, row[3].decode('gbk', 'ignore'), centerFormat)
                    #������ҵ
                    wsVehicle.write(rowIndex, 2, row[5].decode('gbk', 'ignore'), centerFormat)
                    #������
                    wsVehicle.write(rowIndex, 3, row[14], centerFormat)
                    m=0
                    vehicletotal=0
                    if (VTypeStrSplit(self.FuncVType,1)!=0):
                        #���� ���� ���١�20%
                        wsVehicle.write(rowIndex, 4, row[6], centerFormat)
                        #���� ���� �Ǹ��١�50%
                        wsVehicle.write(rowIndex, 5, row[7], centerFormat)
                        #���� ҹ�� ���١�20%
                        wsVehicle.write(rowIndex, 6, row[8], centerFormat)
                        #���� ҹ�� �Ǹ��١�50%
                        wsVehicle.write(rowIndex, 7, row[9], centerFormat)
                        vehicletotal=vehicletotal+row[6]+row[7]+row[8]+row[9]
                        #singlevehicletotal1=singlevehicletotal1+row[6]
                        #singlevehicletotal2=singlevehicletotal2+row[7]
                        #singlevehicletotal3=singlevehicletotal3+row[8]
                        #singlevehicletotal4=singlevehicletotal4+row[9]
                    else:
                        m=m+4
                    if (VTypeStrSplit(self.FuncVType,2)!=0):
                        #�춯 ����
                        wsVehicle.write(rowIndex, 8-m, row[10], centerFormat)
                        vehicletotal=vehicletotal+row[10]
                        #singlevehicletotal5=singlevehicletotal5+row[10]
                    else:
                        m=m+1
                    if (VTypeStrSplit(self.FuncVType,3)!=0):
                        #������Сʱ�������ϴ� ����
                        wsVehicle.write(rowIndex, 9-m, row[11], centerFormat)
                        vehicletotal=vehicletotal+row[11]
                        #singlevehicletotal6=singlevehicletotal6+row[11]
                    else:
                        m=m+1
                    if (VTypeStrSplit(self.FuncVType,4)!=0):                    
                        #��4Сʱ���� ����
                        wsVehicle.write(rowIndex, 10-m, row[12], centerFormat)
                        vehicletotal=vehicletotal+row[12]
                        #singlevehicletotal7=singlevehicletotal7+row[12]
                    else:
                        m=m+1
                    #Υ����Ϊ�����ϼ�
                    wsVehicle.write(rowIndex, 11-m, '=SUM(E%d:%s%d)' %(rowIndex+1,chr(ord('K')-m),rowIndex+1), centerFormat)
                    #singlevehicletotal8=singlevehicletotal8+vehicletotal
                    #�����и�Ϊ20
                    wsVehicle.set_row(rowIndex, 20)
                    rowIndex += 1
                row = cursorGPS.fetchone()

        wsVehicle.merge_range(rowIndex, 0, rowIndex, 1, '�ϼ�', centerFormat)
        wsVehicle.write(rowIndex, 2, '', centerFormat)
        wsVehicle.write(rowIndex, 3, '', centerFormat)
        m=0
        if (VTypeStrSplit(self.FuncVType,1)!=0):
            wsVehicle.write(rowIndex, 4, '=SUM(E5:E%d)' %(rowIndex), centerFormat)
            wsVehicle.write(rowIndex, 5, '=SUM(F5:F%d)' %(rowIndex), centerFormat)
            wsVehicle.write(rowIndex, 6, '=SUM(G5:G%d)' %(rowIndex), centerFormat)
            wsVehicle.write(rowIndex, 7, '=SUM(H5:H%d)' %(rowIndex), centerFormat)
        else:
            m=m+4
        if (VTypeStrSplit(self.FuncVType,2)!=0):
            wsVehicle.write(rowIndex, 8-m, '=SUM(%s5:%s%d)' %(chr(ord('I')-m),chr(ord('I')-m),rowIndex), centerFormat)
        else:
            m=m+1
        if (VTypeStrSplit(self.FuncVType,3)!=0):
            wsVehicle.write(rowIndex, 9-m, '=SUM(%s5:%s%d)' %(chr(ord('J')-m),chr(ord('J')-m),rowIndex), centerFormat)
        else:
            m=m+1
        if (VTypeStrSplit(self.FuncVType,4)!=0):
            wsVehicle.write(rowIndex, 10-m,'=SUM(%s5:%s%d)' %(chr(ord('K')-m),chr(ord('K')-m),rowIndex), centerFormat)
        else:
            m=m+1

        wsVehicle.write(rowIndex, 11-m, '=SUM(E%d:%s%d)' %(rowIndex + 1,chr(ord('K')-m),rowIndex + 1), centerFormat)
        wsVehicle.set_row(rowIndex, 20)
        workbook.close()

    def ExportDetail(self):
        self.vehicleViolate.clear()
        self.companyInZone.clear()
        # ��ÿһ������������Υ����ϸ
        for zoneId in ExcelExportConfig.zoneDic:
            try:
                self.Log('Start to export six ban over speed and break ban detail for %s, zoneID: %d.'
                         %(ExcelExportConfig.zoneDic[zoneId], zoneId))
                workbook = self.CreateWorkbook('%s/%s.xlsx' %(SixBanOverSpeedAndBreakBan.detailFolder,
                                                        self.GetZoneName(zoneId).encode(ExcelExportConfig.envEncode)))
                #���и�ʽ
                centerFormat = workbook.add_format({
                                            'align': 'center',
                                            'valign': 'vcenter',
                                            'border': 1,
                                            'font_size': 10
                                            })
                self.companyInZone[zoneId] = {}
                #����������ϸ
                if (VTypeStrSplit(self.FuncVType,1)!=0):
                    self.ExportOverSpeedDetail(workbook, zoneId, self.vehicleType, self.platformId, self.govStatus, self.FuncVType, centerFormat)				
                #�����춯��ϸ
                if (VTypeStrSplit(self.FuncVType,2)!=0):
                    self.ExportBreakBanDetail(workbook, zoneId, self.vehicleType, self.platformId, self.govStatus, self.FuncVType, centerFormat)
                #����������Сʱ�������ϴ���ϸ 
                if (VTypeStrSplit(self.FuncVType,3)!=0):
                    self.ExportPositionBreakDetail(workbook, zoneId, self.vehicleType, self.platformId, self.govStatus, self.FuncVType, centerFormat)
                #������4Сʱ������ϸ
                if (VTypeStrSplit(self.FuncVType,4)!=0):
                    self.ExportFatigueDriveDetail(workbook, zoneId, self.vehicleType, self.platformId, self.govStatus, self.FuncVType, centerFormat)
                workbook.close()
            except Exception, e:
                self.Log(e.__str__())

    # �����ݵ�����  ȫʡ���Ƕ�λϵͳΣ�ջ������䳵����̬ͳ�Ʊ���
    def __WriteDataAll(self, worksheet, rowIndex, rowData):
        zonetotal=0
        allvehicletotal=0
        try:
            i=0           
            #����
            worksheet.write(rowIndex, 0, self.GetZoneName(rowData[0]), self.centerFormat)
            #������װ����
            worksheet.write(rowIndex, 1, rowData[2], self.centerFormat)
            #������
            worksheet.write(rowIndex, 2, rowData[3], self.centerFormat)
            if (VTypeStrSplit(self.FuncVType,1)!=0):
                #���� Υ�³�����
                worksheet.write(rowIndex, 3, rowData[4], self.centerFormat)
                #���� Υ�³�������
                worksheet.write(rowIndex, 4, rowData[5], self.centerFormat)
                #���� ���� ���١�20%
                worksheet.write(rowIndex, 5, rowData[6], self.centerFormat)
                #���� ���� �Ǹ��١�50%
                worksheet.write(rowIndex, 6, rowData[7], self.centerFormat)
                #���� ҹ�� ���١�20%
                worksheet.write(rowIndex, 7, rowData[8], self.centerFormat)
                #���� ҹ�� �Ǹ��١�50%
                worksheet.write(rowIndex, 8, rowData[9], self.centerFormat)
                zonetotal=zonetotal+rowData[6]+rowData[7]+rowData[8]+rowData[9]
            else:
                i=i+6
            if (VTypeStrSplit(self.FuncVType,2)!=0):
                #�춯 Υ�³�����
                worksheet.write(rowIndex, 9-i, rowData[10], self.centerFormat)
                #�춯 ����
                worksheet.write(rowIndex, 10-i, rowData[11], self.centerFormat)
                #�춯 Υ�³�������
                worksheet.write(rowIndex, 11-i, rowData[12], self.centerFormat)
                zonetotal=zonetotal+rowData[11]
            else:
                i=i+3
            if (VTypeStrSplit(self.FuncVType,3)!=0):
                #������Сʱ�������ϴ� Υ�³�����        
                worksheet.write(rowIndex, 12-i, rowData[13], self.centerFormat)
                #������Сʱ�������ϴ� ����
                worksheet.write(rowIndex, 13-i, rowData[14], self.centerFormat)
                #������Сʱ�������ϴ� Υ�³�������
                worksheet.write(rowIndex, 14-i, rowData[15], self.centerFormat)     
                zonetotal=zonetotal+rowData[14]
            else:
                i=i+3
            if (VTypeStrSplit(self.FuncVType,4)!=0):
                #��4Сʱ���� Υ�³�����        
                worksheet.write(rowIndex, 15-i, rowData[16], self.centerFormat)
                #��4Сʱ���� ����
                worksheet.write(rowIndex, 16-i, rowData[17], self.centerFormat)
                #��4Сʱ���� Υ�³�������
                worksheet.write(rowIndex, 17-i, rowData[18], self.centerFormat)
                zonetotal=zonetotal+rowData[17]
            else:
                i=i+3                                               
            #Υ����Ϊ�������ϼ�
            viloateAll = 0
            companyViloate = self.companyInZone[rowData[0]]
            for companyId in companyViloate:
                viloateAll += companyViloate[companyId]
            worksheet.write(rowIndex, 18-i, viloateAll, self.centerFormat)
            allvehicletotal=allvehicletotal+viloateAll
            #Υ����Ϊ�����ϼ�
            worksheet.write(rowIndex, 19-i, zonetotal, self.centerFormat)
            #�����и�Ϊ20
            worksheet.set_row(rowIndex, 20)
        except Exception, e:
            self.Log(e.__str__())

    # ���� ȫʡ���Ƕ�λϵͳΣ�ջ������䳵����̬ͳ�Ʊ��� �ĺϼ�����
    def __WriteSumAll(self, worksheet, rowIndex, rowData):
        try:
            i=0
            alltotal=0
            #����
            worksheet.write(rowIndex, 0, rowData[0].strip().decode('gbk', 'ignore'), self.centerFormat)
            #������װ����
            worksheet.write(rowIndex, 1, rowData[1], self.centerFormat)
            #������
            worksheet.write(rowIndex, 2, rowData[2], self.centerFormat)
            if (VTypeStrSplit(self.FuncVType,1)!=0):
                #���� Υ�³�����
                worksheet.write(rowIndex, 3, rowData[3], self.centerFormat)
                #���� Υ�³�������
                worksheet.write(rowIndex, 4, rowData[4], self.centerFormat)
                #���� ���� ���١�20%
                worksheet.write(rowIndex, 5, rowData[5], self.centerFormat)
                #���� ���� �Ǹ��١�50%
                worksheet.write(rowIndex, 6, rowData[6], self.centerFormat)
                #���� ҹ�� ���١�20%
                worksheet.write(rowIndex, 7, rowData[7], self.centerFormat)
                #���� ҹ�� �Ǹ��١�50%
                worksheet.write(rowIndex, 8, rowData[8], self.centerFormat)
                alltotal=alltotal+rowData[5]+rowData[6]+rowData[7]+rowData[8]
            else:
                i=i+6
            if (VTypeStrSplit(self.FuncVType,2)!=0):
                #�춯 Υ�³�����
                worksheet.write(rowIndex, 9-i, rowData[9], self.centerFormat)
                #�춯 ����
                worksheet.write(rowIndex, 10-i, rowData[10], self.centerFormat)
                #�춯 Υ�³�������
                worksheet.write(rowIndex, 11-i, rowData[11], self.centerFormat)
                alltotal=alltotal+rowData[10]
            else:
                i=i+3
            if (VTypeStrSplit(self.FuncVType,3)!=0):
                #������Сʱ�������ϴ� Υ�³�����        
                worksheet.write(rowIndex, 12-i, rowData[12], self.centerFormat)
                #������Сʱ�������ϴ� ����
                worksheet.write(rowIndex, 13-i, rowData[13], self.centerFormat)
                #������Сʱ�������ϴ� Υ�³�������
                worksheet.write(rowIndex, 14-i, rowData[14], self.centerFormat)     
                alltotal=alltotal+rowData[13]
            else:
                i=i+3
            if (VTypeStrSplit(self.FuncVType,4)!=0):
                #��4Сʱ���� Υ�³�����        
                worksheet.write(rowIndex, 15-i, rowData[15], self.centerFormat)
                #��4Сʱ���� ����
                worksheet.write(rowIndex, 16-i, rowData[16], self.centerFormat)
                #��4Сʱ���� Υ�³�������
                worksheet.write(rowIndex, 17-i, rowData[17], self.centerFormat)
                alltotal=alltotal+rowData[16]
            else:
                i=i+3                                               
            #Υ����Ϊ�������ϼ�
            worksheet.write(rowIndex, 18-i, '=SUM(%s%d:%s%d)' %(chr(ord('S')-i),ExcelExportConfig.headerLineNumber + 1,chr(ord('S')-i),rowIndex), self.centerFormat)
            #Υ����Ϊ�����ϼ�
            worksheet.write(rowIndex, 19-i, '=SUM(%s%d:%s%d)' %(chr(ord('T')-i),ExcelExportConfig.headerLineNumber + 1,chr(ord('T')-i),rowIndex), self.centerFormat)
            #�����и�Ϊ20
            worksheet.set_row(rowIndex, 20)
        except Exception, e:
            self.Log(e.__str__())

    # �����ݵ����� (ʡ������ )���Ƕ�λϵͳ������̬ͳ�Ʊ���
    def __WriteDataZone(self, worksheet, rowIndex, rowData):
        try:
            j=0
            zonetotal=0
            #���
            worksheet.write(rowIndex, 0, rowIndex - ExcelExportConfig.headerLineNumber + 1, self.centerFormat)
            #������ҵ
            stripData = rowData[3].strip()
            worksheet.write(rowIndex, 1, stripData.decode('gbk', 'ignore'), self.centerFormat)
            #������װ����
            worksheet.write(rowIndex, 2, rowData[4], self.centerFormat)
            #������
            onlineRate = rowData[5].strip('%')
            worksheet.write(rowIndex, 3, string.atof(onlineRate) / 100.0, self.percentageFormat)
            if (VTypeStrSplit(self.FuncVType,1)!=0):
                #���� Υ�³�����
                worksheet.write(rowIndex, 4, rowData[6], self.centerFormat)
                #���� Υ�³�������
                worksheet.write(rowIndex, 5, rowData[7], self.centerFormat)
                #���� ���� ���١�20%
                worksheet.write(rowIndex, 6, rowData[8], self.centerFormat)
                #���� ���� �Ǹ��١�50%
                worksheet.write(rowIndex, 7, rowData[9], self.centerFormat)
                #���� ҹ�� ���١�20%
                worksheet.write(rowIndex, 8, rowData[10], self.centerFormat)
                #���� ҹ�� �Ǹ��١�50%
                worksheet.write(rowIndex, 9, rowData[11], self.centerFormat)
                zonetotal=zonetotal+rowData[8]+rowData[9]+rowData[10]+rowData[11]
            else:
                j=j+6
            if (VTypeStrSplit(self.FuncVType,2)!=0):                
                #�춯 Υ�³�����
                worksheet.write(rowIndex, 10-j, rowData[12], self.centerFormat)
                #�춯 ����
                worksheet.write(rowIndex, 11-j, rowData[13], self.centerFormat)
                #�춯 Υ�³�������
                worksheet.write(rowIndex, 12-j, rowData[14], self.centerFormat)
                zonetotal=zonetotal+rowData[13]
            else:
                j=j+3
            if (VTypeStrSplit(self.FuncVType,3)!=0):
                #������Сʱ�������ϴ� Υ�³�����
                worksheet.write(rowIndex, 13-j, rowData[15], self.centerFormat)
                #������Сʱ�������ϴ� ����
                worksheet.write(rowIndex, 14-j, rowData[16], self.centerFormat)
                #������Сʱ�������ϴ� Υ�³�������
                worksheet.write(rowIndex, 15-j, rowData[17], self.centerFormat)
                zonetotal=zonetotal+rowData[16]
            else:
                j=j+3
            if (VTypeStrSplit(self.FuncVType,4)!=0):
                #��4Сʱ���� Υ�³�����
                worksheet.write(rowIndex, 16-j, rowData[18], self.centerFormat)
                #��4Сʱ���� ����
                worksheet.write(rowIndex, 17-j, rowData[19], self.centerFormat)
                #��4Сʱ���� Υ�³�������
                worksheet.write(rowIndex, 18-j, rowData[20], self.centerFormat)
                zonetotal=zonetotal+rowData[19]
            else:
                j=j+3            
            
            #Υ����Ϊ�������ϼ�
            zoneId = rowData[0] - rowData[0] % 10000
            worksheet.write(rowIndex, 19-j, self.companyInZone[zoneId][rowData[2]], self.centerFormat)
            #Υ����Ϊ�����ϼ�
            worksheet.write(rowIndex, 20-j, zonetotal,self.centerFormat)
            #�����и�Ϊ20
            worksheet.set_row(rowIndex, 20)
        except Exception, e:
            self.Log(e.__str__())

    # ���ϼ����ݵ����� (ʡ������ )���Ƕ�λϵͳ������̬ͳ�Ʊ���
    def __WriteSumZone(self, worksheet, rowIndex, rowData):
        try:
            j=0
            alltotal=0
            #���
            worksheet.write(rowIndex, 0, rowData[0].decode('gbk', 'ignore'), self.centerFormat)
            #������ҵ
            worksheet.write(rowIndex, 1, '', self.borderFormat)
            #������װ����
            worksheet.write(rowIndex, 2, '=SUM(C%d:C%d)' %(ExcelExportConfig.headerLineNumber + 1, rowIndex), self.centerFormat)
            #������
            worksheet.write(rowIndex, 3, '=AVERAGE(D%d:D%d)' %(ExcelExportConfig.headerLineNumber + 1, rowIndex), self.percentageFormat)
            if (VTypeStrSplit(self.FuncVType,1)!=0):
                #���� Υ�³�����
                worksheet.write(rowIndex, 4, rowData[4], self.centerFormat)
                #���� Υ�³�������
                worksheet.write(rowIndex, 5, '=E%d/C%d' %(rowIndex + 1, rowIndex + 1), self.percentageFormat)
                #���� ���� ���١�20%
                worksheet.write(rowIndex, 6, rowData[6], self.centerFormat)
                #���� ���� �Ǹ��١�50%
                worksheet.write(rowIndex, 7, rowData[7], self.centerFormat)
                #���� ҹ�� ���١�20%
                worksheet.write(rowIndex, 8, rowData[8], self.centerFormat)
                #���� ҹ�� �Ǹ��١�50%
                worksheet.write(rowIndex, 9, rowData[9], self.centerFormat)
                alltotal=alltotal+rowData[6]+rowData[7]+rowData[8]+rowData[9]
            else:
                j=j+6
            if (VTypeStrSplit(self.FuncVType,2)!=0):                
                #�춯 Υ�³�����
                worksheet.write(rowIndex, 10-j, rowData[10], self.centerFormat)
                #�춯 ����
                worksheet.write(rowIndex, 11-j, rowData[11], self.centerFormat)
                #�춯 Υ�³�������
                worksheet.write(rowIndex, 12-j, '=%s%d/C%d' %(chr(ord('K')-j),rowIndex + 1, rowIndex + 1), self.percentageFormat)
                alltotal=alltotal+rowData[11]
            else:
                j=j+3
            if (VTypeStrSplit(self.FuncVType,3)!=0):
                #������Сʱ�������ϴ� Υ�³�����
                worksheet.write(rowIndex, 13-j, rowData[13], self.centerFormat)
                #������Сʱ�������ϴ� ����
                worksheet.write(rowIndex, 14-j, rowData[14], self.centerFormat)
                #������Сʱ�������ϴ� Υ�³�������
                worksheet.write(rowIndex, 15-j, '=%s%d/C%d' %(chr(ord('N')-j),rowIndex + 1, rowIndex + 1), self.percentageFormat)
                alltotal=alltotal+rowData[14]
            else:
                j=j+3
            if (VTypeStrSplit(self.FuncVType,4)!=0):
                #��4Сʱ���� Υ�³�����
                worksheet.write(rowIndex, 16-j, rowData[16], self.centerFormat)
                #��4Сʱ���� ����
                worksheet.write(rowIndex, 17-j, rowData[17], self.centerFormat)
                #��4Сʱ���� Υ�³�������
                worksheet.write(rowIndex, 18-j, '=%s%d/C%d' %(chr(ord('Q')-j),rowIndex + 1, rowIndex + 1), self.percentageFormat)
                alltotal=alltotal+rowData[17]
            else:
                j=j+3            
                                
            #Υ����Ϊ�������ϼ�
            worksheet.write(rowIndex, 19-j, '=SUM(%s%d:%s%d)' %(chr(ord('T')-j),ExcelExportConfig.headerLineNumber +1,chr(ord('T')-j), rowIndex), self.centerFormat)
            #Υ����Ϊ�����ϼ�
            worksheet.write(rowIndex, 20-j, '=SUM(%s%d:%s%d)' %(chr(ord('U')-j),ExcelExportConfig.headerLineNumber +1,chr(ord('U')-j), rowIndex), self.centerFormat)
            #�����и�Ϊ20
            worksheet.set_row(rowIndex, 20)
        except Exception, e:
            self.Log(e.__str__())
