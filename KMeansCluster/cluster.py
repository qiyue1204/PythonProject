#coding=utf-8

from math import pi, sin, cos
from collections import namedtuple
from random import random, choice
from copy import copy
import matplotlib.pyplot as plt
import numpy as np
import xlrd

try:
    import psyco
    psyco.full()
except ImportError:
    pass



FLOAT_MAX = 1e100
fig1 = plt.figure('fig1',figsize=(12,10))
ax1 = fig1.add_subplot(111)

cm = plt.get_cmap("nipy_spectral")


class Point:
    __slots__ = ["x", "y", "group"]
    def __init__(self, x=0.0, y=0.0, group=0):
        self.x, self.y, self.group = x, y, group

    def __str__(self):
        return "%r,%r,%r" % (self.x,self.y,self.group)

def generate_points(filename):
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
    for i in range(0, nrows):
        row_data = sh.row_values(i)
        row_list.append(row_data)
    points = [Point() for _ in xrange(len(row_list))]
    i=0
    for p in points:
        p.x = row_list[i][0]
        p.y = row_list[i][1]
        i=i+1
    return points

def generate_points_ran(npoints, radius):
    points = [Point() for _ in xrange(npoints)]
    for p in points:
        r = random() * radius
        ang = random() * 2 * pi
        p.x = r * cos(ang)
        p.y = r * sin(ang)
    return points


def nearest_cluster_center(point, cluster_centers):
    """Distance and index of the closest cluster center"""
    def sqr_distance_2D(a, b):
        return (a.x - b.x) ** 2  +  (a.y - b.y) ** 2    #求两个最标点之间的距离

    min_index = point.group
    min_dist = FLOAT_MAX

    for i, cc in enumerate(cluster_centers):
        d = sqr_distance_2D(cc, point)
        if min_dist > d:
            min_dist = d
            min_index = i

    return (min_index, min_dist)


#points是数据点，nclusters是给定的簇类数目
#cluster_centers包含初始化的nclusters个中心点，开始都是对象->(0,0,0)


def kpp(points, cluster_centers):
    cluster_centers[0] = copy(choice(points)) #随机选取第一个中心点
    d = [0.0 for _ in xrange(len(points))]  #列表，长度为len(points)，保存每个点离最近的中心点的距离

    for i in xrange(1, len(cluster_centers)):  # i=1...len(c_c)-1
        sum = 0
        for j, p in enumerate(points):
            d[j] = nearest_cluster_center(p, cluster_centers[:i])[1] #第j个数据点p与各个中心点距离的最小值
            sum += d[j]

        sum *= random()

        for j, di in enumerate(d):
            sum -= di
            if sum > 0:
                continue
            cluster_centers[i] = copy(points[j])
            break

    for p in points:
        p.group = nearest_cluster_center(p, cluster_centers)[0]


#points是数据点，nclusters是给定的簇类数目

def lloyd(points, nclusters):
    cluster_centers = [Point() for _ in xrange(nclusters)]  #根据指定的中心点个数，初始化中心点，均为(0,0,0)
    #print cluster_centers

    # call k++ init
    kpp(points, cluster_centers)   #选择初始种子点

    # 下面是kmeans
    lenpts10 = len(points) >> 10  #除以2的10次方（这个数据值得推敲）

    changed = 0
    while True:
        # group element for centroids are used as counters
        for cc in cluster_centers:
            cc.x = 0
            cc.y = 0
            cc.group = 0

        for p in points:
            cluster_centers[p.group].group += 1  #与该种子点在同一簇的数据点的个数
            cluster_centers[p.group].x += p.x
            cluster_centers[p.group].y += p.y

        for cc in cluster_centers:    #生成新的中心点
            cc.x /= cc.group
            cc.y /= cc.group

        # find closest centroid of each PointPtr
        changed = 0  #记录所属簇发生变化的数据点的个数
        for p in points:
            min_i = nearest_cluster_center(p, cluster_centers)[0]
            if min_i != p.group:
                changed += 1
                p.group = min_i

        # stop when 99.9% of points are good
        if changed <= lenpts10:
            break


    for i, cc in enumerate(cluster_centers):
        cc.group = i

    return cluster_centers

def print_eps(points, cluster_centers,k):
    #plt.gca().set_color_cycle([colormap(m) for m in np.linspace(0, 0.9, k)])
    col = [cm(float(i) / (k)) for i in xrange(k)]
    #print col
    print '--------------------------------------------------------'
    for m in range(0, k):
        s1=[]
        s2=[]
        s3=[]
        for p in points:
            # print points[i]
            if (p.group == m):
                s1.append(p.x)
                s2.append(p.y)
        s3.append(str(len(s1)))
        ax1.scatter(s1, s2, s= 10,color=col[m], marker='.')
        print str(m)+' : '+str(len(s1))
    for m in range(0,k):
        s1=[]
        s2=[]
        s3=[]
        for cc in cluster_centers:
            if(cc.group==m):
                s1.append(cc.x)
                s2.append(cc.y)
        s3.append(str(len(s1)))
        ax1.scatter(s1, s2, color=col[m],marker=(6,2))
    print '--------------------------------------------------------'
    for cc in cluster_centers:
        print cc.x, cc.y, cc.group

def cut_apart(filename):
    #npoints = 10000
    #k = 2 # # clusters
    npoints=10000
    #points = generate_points_ran(npoints, 10)
    points = generate_points(filename)
    #print points  #s
    print len(points)
    k=len(points)/250
    print k
    #k=200
    while True:
        r=0
        cluster_centers = lloyd(points, k)
        for m in range(0, k):
            s1=[]
            s2=[]
            for p in points:
                # print points[i]
                if (p.group == m):
                    s1.append(p.x)
                    s2.append(p.y)
            #print str(m) + ' : ' + str(len(s1))
            if len(s1)<=1:
                r=r+1
        print r
        if k==k-r:
            break
        else:
            k=k-r


    print_eps(points, cluster_centers, k)
    plt.show()


cut_apart("test824.xls")