# -*- coding: utf-8 -*-
"""
===================================
Demo of DBSCAN clustering algorithm
===================================

Finds core samples of high density and expands clusters from them.

"""
import time
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN
from sklearn import metrics
from sklearn.datasets.samples_generator import make_blobs
from sklearn.preprocessing import StandardScaler
from MSSQL import MSSQL

def main():

##################################################################################
# 连接数据库，查询报警数据
    t0=time.time()
    ms = MSSQL(host="10.50.40.201",user="sa",pwd="123@abc",db="GPS_GOV")
    #sqlstr="select * from OverSpeed"
    # sqlstr='select  BLongtitude,BLatitude,ELongtitude,ELatitude from GOVPositionBreakDetail_NEW_5To30  ' \
    #        'where (BLongtitude/1000000>97.3661 and BLongtitude/1000000<108.5329 and BLatitude/1000000>26.0661 and BLatitude/1000000<34.3203)  ' \
    #        'and (ELongtitude/1000000>97.3661 and ELongtitude/1000000<108.5329 and ELatitude/1000000>26.0661 and ELatitude/1000000<34.3203) ' \
    #        'and dbo.fnGetDistance(BLongtitude,BLatitude,ELongtitude,ELatitude)>0.5 and BreakTime >500 '
    # sqlstr='select top 100000 Longitude,Latitude from POS20161107 where Speed>0 and DeviceID <500'
    sqlstr='select beginLon,beginLat,endLon,endLat from SixBreakTest'
    resList = ms.ExecQuery(sqlstr)
    res=[]
    for (beginLon,beginLat,endLon,endLat) in resList:
        # Lon=(float(BLongtitude)+float(ELongtitude))/2000000
        # Lat=(float(BLatitude)+float(ELatitude))/2000000
        # Lon=float(Longitude)/1000000
        # Lat=float(Latitude)/1000000
        Lon=(float(beginLon)+float(endLon))/2000000
        Lat=(float(beginLat)+float(endLat))/2000000
        opint=[Lon,Lat]
        res.append(opint)
   # res= np.sort(res)
    res=np.array(res)

    sqltime=time.time()-t0
    print '数据库查询时间：',sqltime
##################################################################################
# Compute DBSCAN
    db = DBSCAN(eps=0.005, min_samples=200,n_jobs=-1).fit(res)
    core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
    core_samples_mask[db.core_sample_indices_] = True
    labels = db.labels_
    # Number of clusters in labels, ignoring noise if present.
    n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
##################################################################################
    print('Estimated number of clusters: %d' % n_clusters)
   # print("Silhouette Coefficient: %f" % setlabels[10])
   #  print ("core_samples_mask: %s"% core_samples_mask)
   #  print ("mask_count",len(core_samples_mask))
   #  print ("core_sample_indices:", db.core_sample_indices_)
   #  print ("components:%c" ,db.components_)
    print ("indices_count",len(db.core_sample_indices_))
   #  print ("components_count",len(db.components_))
   #  print ("labels",len(labels))
    print "###################################"
##################################################################################
# Plot result
    fig = plt.figure(figsize=(16, 9))
    fig.subplots_adjust(left=0.02, right=0.98, bottom=0.05, top=0.9)
    cm = plt.get_cmap("nipy_spectral")
    colors = [cm(float(i) / (n_clusters)) for i in xrange(n_clusters)]

    unique_labels = set(labels)
    for k, col in zip(unique_labels, colors):
        if k == -1:
            # Black used for noise.
            col = 'k'

        class_member_mask = (labels == k)

        xy = res[class_member_mask & core_samples_mask]
        plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=col,
                 markeredgecolor='k', markersize=12)
        #print xy
        #print '******',k,'*******',len(xy)
        xy = res[class_member_mask & ~core_samples_mask]
        plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=col,
                 markeredgecolor='k', markersize=6)
        #print xy
        #print k,'******',len(xy)
###############################################################################
# 打印图形
    plt.show()
###################################################################################
if __name__ == '__main__':
    main()