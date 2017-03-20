#!/usr/bin/python
#coding = utf-8
import sys
import xlrd
from math import radians, cos, sin, asin, sqrt
# def GetDistance(BLon, BLa, ELon, ELa):
#     BLon, BLa, ELon, ELa = map(radians, [BLon, BLa, ELon, ELa])

#     dlon = ELon - BLon
#     dlat = ELa - BLa
#     a = sin(dlat / 2) ** 2 + cos(BLa) * cos(ELa) * sin(dlon / 2) ** 2
#     c = 2 * asin(sqrt(a))
#     r = 6371.004
#     return c * r
#
# def GetTimeDifference(BDate,BTime,EDate,ETime):
#     if BDate==EDate:
#         s = ETime - BTime
#     else:
#         s = (EDate-BDate)*86400+ETime-BTime
#     return s


for line in sys.stdin:
    line = line.strip()
    data = line.split('\t')
    print data


# def check(m):
#     for i in range(0,len(m)-2):
#         BDate=m[i][5]
#         BTime=m[i][6]
#         EDate=m[i+1][5]
#         ETime=m[i+1][6]
#         BLon=m[i][9]/1000000
#         BLa=m[i][10]/1000000
#         ELon=m[i+1][9]/1000000
#         ELa=m[i+1][10]/1000000
#         BSpeed=m[i][1]
#         BXsily=m[i][2]
#         ESpeed=m[i+1][1]
#         EXsjly=m[i+1][2]
#         s=GetDistance(BLon, BLa, ELon, ELa)
#         t=GetTimeDifference(BDate,BTime,EDate,ETime)
#         if t==0:
#            pass
#             #print str(0)+'--'+str(BSpeed)+'--'+str(BXsily)
#         else:
#             diff=round(s/t*3600,1)
#             #print str(diff)+'--'+str(BSpeed)+'--'+str(BXsily)+'---------'+str(diff-BSpeed)
#             print str(diff-BSpeed)
# check(m)

