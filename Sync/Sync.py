#!/usr/bin/python
# -*- coding:utf8 -*-

import os
from MSSQL import MSSQL

ms = MSSQL(host="10.50.40.201",user="sa",pwd="123@abc",db="GPS_GOV")

def printPath(level, path):
    global allFileNum
    '''''
    打印一个目录下的所有文件夹和文件
    '''
    # 所有文件夹，第一个字段是次目录的级别
    dirList = []
    # 所有文件
    fileList = []
    # 返回一个列表，其中包含在目录条目的名称(google翻译)
    files = os.listdir(path)
    print files
    for f in files:
        s=open(path+'\\'+f, 'r')
        #print s.read()
        # for eachLine in fopen:
        #     print eachLine
        #fopen.close()
        print path+'\\'+f
        #osql -S"10.50.40.201"  -U"sa" -P"123@abc" -d"GPS_GOV" -i"C:\Users\Administrator.PC-201509091200\Desktop\MySQLServer\Procedures1\dbo.delete_GPSEntReportVehicle.StoredProcedure.sql"
        s='osql -S"10.50.40.201" -U"sa" -P"123@abc" -d"GPS_GOV_Position_Abnormal" -i\"%s\"' %(path+'\\'+f)
        print s
        os.system(s)



if __name__ == '__main__':
    printPath(1, 'C:\Users\Administrator.PC-201509091200\Desktop\MySQLServer\Tables')
    #print '总文件数 =', allFileNum