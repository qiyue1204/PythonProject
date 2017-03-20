# -*- coding: utf-8 -*-
import sys
reload(sys)

# array=[]
# for line in sys.stdin:
#     line = line.decode("gb2312")
#     line = line.strip()
#     words = line.split()
#     for word in words:
#         array.append({word[2], word[6], word[7][0:9]})
#
# print array

array=[]
array1=[]

f=open("test1.txt","r")
f.readline()#第一行是列，可以将文件移到第二行开始处
for line in f:
    line = line.decode("gb2312")
    line = line.strip()
    word = line.split()
    #print word
    #word[2], word[6], word[7][:10]
    array.append([word[7][:10],word[2],word[6]])

array.sort(key=lambda x:(x[0],x[1]))

# for a in array:
#     print a[0],a[1],a[2]

b=[array[0][2]]
for i in range(1,len(array)-1):
    if array[i][0]==array[i-1][0] and array[i][1]==array[i-1][1]:
        if array[i][2] not in b:
            b.append(array[i][2])
        else:
            pass
    else:
        #print b
        array1.append(b)
        b=[]
        b=[array[i][2]]

# print len(array1)
# print array1

print str(array1).encode('utf-8')

# for a1 in array1:
#     # print '--------------------'
#     #print len(a1)
#     #print a1
#     for i in range(0,len(a1)):
#         print a1[i],
#     print '\t'



