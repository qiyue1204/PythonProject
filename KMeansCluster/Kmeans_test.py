#coding=utf-8
#!/usr/bin/env python
#-------------------------------------------------------------------------------
# Name: Kmeans_test.py
# Purpose: 测试 使用Python的sklearn库中的Kmeans聚类
#
# Author: scott
#
# Created: 11/11/2016
#-------------------------------------------------------------------------------
import time

import numpy as np
import matplotlib.pyplot as plt

from sklearn.cluster import MiniBatchKMeans, KMeans
from sklearn.metrics.pairwise import pairwise_distances_argmin
from sklearn.datasets.samples_generator import make_blobs
from MSSQL import MSSQL

def main():

##################################################################################
# 连接数据库，查询报警数据

    ms = MSSQL(host="10.50.40.201",user="sa",pwd="123@abc",db="GPS_GOV")
    resList = ms.ExecQuery("select beginLon*1.0/1000000,beginLat*1.0/1000000 from SixBreakTest")
    res=[]
    for (Lng) in resList:
        #print list(Lng)
        res.append(list(Lng))

    #res= list(resList)
    #print res
    res = np.array(res)
    cm = plt.get_cmap("nipy_spectral")
##############################################################################
# Compute clustering with Means
    n_clusters=100
    k_means = KMeans(init='k-means++', n_clusters=n_clusters, n_init=10)
    t0 = time.time() #当前时间
    k_means.fit(res)
#使用K-Means 对 3000数据集训练算法的时间消耗
    t_batch = time.time() - t0

##################################################################################
# Compute clustering with MiniBatchKMeans

    mbk = MiniBatchKMeans(init='k-means++', n_clusters=n_clusters, batch_size=45,init_size=1500,
                      n_init=10, max_no_improvement=10, verbose=0)
    t0 = time.time()
    mbk.fit(res)
#使用MiniBatchKMeans 对 3000数据集训练算法的时间消耗
    t_mini_batch = time.time() - t0
##################################################################################
# Plot result
    fig = plt.figure(figsize=(12, 10))
    fig.subplots_adjust(left=0.02, right=0.98, bottom=0.05, top=0.9)

    colors = [cm(float(i) / (n_clusters)) for i in xrange(n_clusters)]
# We want to have the same colors for the same cluster from the
# MiniBatchKMeans and the KMeans algorithm. Let's pair the cluster centers per
# closest one.
    k_means_cluster_centers = np.sort(k_means.cluster_centers_, axis=0)  #对每列进行排序
    mbk_means_cluster_centers = np.sort(mbk.cluster_centers_, axis=0) #对每列进行排序
    k_means_labels = pairwise_distances_argmin(res, k_means_cluster_centers)
    mbk_means_labels = pairwise_distances_argmin(res, mbk_means_cluster_centers)
    order = pairwise_distances_argmin(k_means_cluster_centers,
                                  mbk_means_cluster_centers)



# KMeans
    ax = fig.add_subplot(111) #add_subplot  图像分给为 一行三列，第一块
    for k, col in zip(range(n_clusters), colors):  #zip函数接受任意多个（包括0个和1个）序列作为参数，返回一个tuple列表
        my_members = k_means_labels == k
        cluster_center = k_means_cluster_centers[k]
        for i in range(0,len(res[my_members])):
            ax.scatter(res[my_members][i][0], res[my_members][i][1],s= 10,color=col, marker='.')
            #ms.ExecNonQuery("Update PositionBreakDetail set cluster = '%d' where BLon = '%s' and BLa = '%s' "%(k,str(res[my_members][i][0]),str(res[my_members][i][1])))
        ax.scatter(cluster_center[0], cluster_center[1],s= 50,color=col, marker=(6,2))
    ax.set_title('KMeans')
    ax.set_xticks(())
    ax.set_yticks(())
    plt.text(-3.5, 1.8,  'train time: %.2fs\ninertia: %f' % (
        t_batch, k_means.inertia_))

# MiniBatchKMeans
#     ax = fig.add_subplot(1, 3, 2)#add_subplot  图像分给为 一行三列，第二块
#     for k, col in zip(range(n_clusters), colors):
#         my_members = mbk_means_labels == order[k]
#         cluster_center = mbk_means_cluster_centers[order[k]]
#         for i in range(0,len(res[my_members])):
#             ax.scatter(res[my_members][i][0], res[my_members][i][1],s=10, color=col,marker='.')
#         ax.scatter(cluster_center[0], cluster_center[1],s=50, color=col,marker=(6,2))
#     ax.set_title('MiniBatchKMeans')
#     ax.set_xticks(())
#     ax.set_yticks(())
#     plt.text(-3.5, 1.8, 'train time: %.2fs\ninertia: %f' %
#              (t_mini_batch, mbk.inertia_))

    #Initialise the different array to all False
    # different = (mbk_means_labels == 4)
    # ax = fig.add_subplot(1, 3, 3)#add_subplot  图像分给为 一行三列，第三块
    #
    # for k in range(n_clusters):
    #     different += ((k_means_labels == k) != (mbk_means_labels == order[k]))
    #
    # identic = np.logical_not(different)
    # ax.scatter(res[identic][0], res[identic][1], 'w',
    #         markerfacecolor='#bbbbbb', marker='.')
    # ax.scatter(res[different, 0], res[different, 1], 'w',
    #         markerfacecolor='m', marker='.')
    # ax.set_title('Difference')
    # ax.set_xticks(())
    # ax.set_yticks(())

    plt.show()

###################################################################################
if __name__ == '__main__':
    main()