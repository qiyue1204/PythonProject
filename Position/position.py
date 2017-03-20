#coding:utf-8
import xlrd
from math import radians, cos, sin, asin, sqrt

def generate_position(filename):
    fname = filename
    bk = xlrd.open_workbook(fname)
    shxrange = range(bk.nsheets)
    try:
        sh = bk.sheet_by_name("Sheet1")
    except:
        print "no sheet in %s named Sheet1" % fname

    nrows = sh.nrows
    ncols = sh.ncols
    print "nrows %d, ncols %d" % (nrows, ncols)

    row_list = []
    for i in range(1, nrows):
        row_data = sh.row_values(i)
        row_list.append(row_data)    #points = [Point() for _ in xrange(len(row_list))]

    return row_list


def GetDistance(BLon, BLa, ELon, ELa):  # 经度1，纬度1，经度2，纬度2 （十进制度数）
    #"""
    #Calculate the great circle distance between two points
    #on the earth (specified in decimal degrees)
    #"""
    # 将十进制度数转化为弧度  
    BLon, BLa, ELon, ELa = map(radians, [BLon, BLa, ELon, ELa])

    # haversine公式  
    dlon = ELon - BLon
    dlat = ELa - BLa
    a = sin(dlat / 2) ** 2 + cos(BLa) * cos(ELa) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371.004  # 地球平均半径，单位为公里
    return c * r



def GetTimeDifference(BDate,BTime,EDate,ETime):
    if BDate==EDate:
        s = ETime - BTime
    else:
        s = (EDate-BDate)*86400+ETime-BTime
    return s


m=generate_position("position.xlsx")
#print m


s=GetDistance(103.858215,30.703078,103.558817,30.703065)
print s

t=GetTimeDifference(20160925,35960,20160925,35962)
#print t

#print s/t*3600

def check(m):
    for i in range(0,len(m)-2):
        BDate=m[i][5]
        BTime=m[i][6]
        EDate=m[i+1][5]
        ETime=m[i+1][6]
        BLon=m[i][9]/1000000
        BLa=m[i][10]/1000000
        ELon=m[i+1][9]/1000000
        ELa=m[i+1][10]/1000000
        BSpeed=m[i][1]
        BXsily=m[i][2]
        ESpeed=m[i+1][1]
        EXsjly=m[i+1][2]
        s=GetDistance(BLon, BLa, ELon, ELa)
        t=GetTimeDifference(BDate,BTime,EDate,ETime)
        if t==0:
           pass
            #print str(0)+'--'+str(BSpeed)+'--'+str(BXsily)
        else:
            diff=round(s/t*3600,1)
            #print str(diff)+'--'+str(BSpeed)+'--'+str(BXsily)+'---------'+str(diff-BSpeed)
            print str(diff-BSpeed)
check(m)
