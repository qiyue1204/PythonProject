#coding:utf-8
import os
import time

dir = os.path.abspath(".")
specify_str = '.sql'

def getFile():
    results = []
    folders = [dir]
    for folder in folders:
        folders += [os.path.join(folder, x) for x in os.listdir(folder) \
                    if os.path.isdir(os.path.join(folder, x))]
        results += [os.path.relpath(os.path.join(folder, x), start=dir) \
                    for x in os.listdir(folder) \
                    if os.path.isfile(os.path.join(folder, x)) and specify_str in x]
    FileList = []
    for result in results:
            FileList.append((result, time.mktime(time.localtime(os.stat(result).st_ctime))))
    return FileList

def getExportDbSql(db, sqlname):  # 获取导出一个数据库实例的sql语句
    sql = 'sqlcmd -S 10.50.40.201  -U sa -P 123@abc -i UP_TEST_AnalysisOnlinePeriod_hl.sql'%(db['host'],db['user'], db['pwd'],sqlname)
    return sql

def createDbBackupFile(fname, dbList,FileList,BDate,EDate):  # 生成数据库导出的语句保存到文件
    if not fname or not dbList:
        return False

    f = open(fname, 'w')
    f.write('::设置当前存储过程文件所在路径\n\n')
    f.write('set cur_dir=%cd%\*.sql\n\n')

    for file in FileList:
        if file[1]>=BDate and file[1]<=EDate:
            f.write(getExportDbSql(dbList,file[0]))

    f.write('cd..\n\n')
    f.write('pause "存储过程部署完毕"\n\n')
    f.close()



def initDb(user, pwd, host):  # 生成db字典对象并返回
    db = {}
    db['user'] = user
    db['pwd'] = pwd
    db['host'] = host

    return db

# def displayDb(db):
#     print('user =', db['user'])
#     print('pwd =', db['pwd'])
#     print('host =', db['host'])
#     print('port =', db['port'])
#     print('server =', db['server'])
#     print('indexList =', db['indexList'])
#     print('\n')


def displayList(list):
    for item in list:
        displayDb(item)


if __name__ == '__main__':
    db = initDb('sa', '123@abc', '10.50.40.201')

    dbList = []
    dbList.append(db)
    print dbList

    # BDate = input("请输入开始时间，格式‘yyyy-mm-dd hh:mm:ss'：")
    # EDate = input("请输入结束时间，格式‘yyyy-mm-dd hh:mm:ss'：")
    # BDate= time.mktime(time.strptime(BDate, '%Y-%m-%d'))
    # EDate= time.mktime(time.strptime(EDate, '%Y-%m-%d'))
    # print BDate,EDate
    BDate = time.mktime(time.strptime('2016-12-15 00:00:00', '%Y-%m-%d %X'))
    EDate = time.mktime(time.strptime('2016-12-15 18:20:00', '%Y-%m-%d %X'))
    # displayList(dbList)
    FileList = getFile()
    #print FileList
    createDbBackupFile('export00.bat', dbList, FileList,BDate,EDate)