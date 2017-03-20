using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Web;

namespace K_means
{
    public class Kmeans
    {
        double[,] inPut;//数据
        int k;//类别数
        int Num;//文件数
        int sub;//特征值数
        /// <summary>
        /// Kmeans聚类后各质心对应的数目
        /// </summary>
        public int[] groupNum;//各组数目
        /// <summary>
        /// Kmeans聚类后的质心
        /// </summary>
        public double[,] preCenter;
        /// <summary>
        /// 实例化类的方法-K值为数组的十分之一
        /// </summary>
        /// <param name="input">kmeans的聚类数据组</param>
        public Kmeans(double[,] input)
        {
            inPut = input;
            Num = input.GetLength(0);
            sub = input.GetLength(1);
            //k = (int)Math.Sqrt(Num) + 1;
            k = Num / 10;
            groupNum = new int[k];
        }
        /// <summary>
        /// 实例化类的方法-K值输入
        /// </summary>
        /// <param name="input"></param>
        /// <param name="K"></param>
        public Kmeans(double[,] input, int K)
        {
            inPut = input;
            Num = input.GetLength(0);
            sub = input.GetLength(1);
            k = K;
            groupNum = new int[k];
        }
        /// <summary>
        /// 执行Kmeans聚类
        /// </summary>
        /// <returns></returns>
        public int[,] GetProcess()
        {
            #region 采用Kmeans++的方式选取质心
            double[,] tmpCenter = new double[k, sub];
            for (int j = 0; j < sub; j++)
            {
                Random random = new Random();
                int i = random.Next(0, k);
                tmpCenter[0, j] = inPut[i, j];
            }
            for (int m = 1; m < k; m++)//选取剩下的K-1个质心
            {
                double sum = 0.0;
                double[] Di = new double[Num];//每一个数据点到质心的距离

                for (int i = 0; i < Num; i++)//循环取所有的数据点
                {
                    for (int j = 0; j < sub; j++)//循环计算特征值的距离
                    {
                        Di[i] += Math.Pow((inPut[i, j] - tmpCenter[m - 1, j]), 2);
                    }
                    sum += Di[i];
                }
                Random ran = new Random();
                double a = ran.Next(100) * 0.01;
                sum *= a;
                for (int i = 0; i < Num; i++)
                {
                    sum -= Di[i];
                    if (sum > 0)
                        continue;
                    else
                    {
                        for (int j = 0; j < sub; j++)//循环将选出的点作为质心赋值
                        {
                            tmpCenter[m, j] = inPut[i, j];
                        }
                        break;
                    }
                }
            }
            /*这是原来选取前K个点作为质心
                        for (int i = 0; i < k; i++)
                            for (int j = 0; j < sub; j++)
                                tmpCenter[i, j] = inPut[i, j];
                        //double[,] preCenter = new double[k, sub];
             * */
            preCenter = new double[k, sub];
            #endregion
            int[,] resultP;//= new int[k, Num];
            while (true)
            {
                resultP = new int[k, Num];//没组质心对应有哪些点落在该质心内

                #region //清空各组的数目
                for (int i = 0; i < k; i++)
                {
                    groupNum[i] = 0;
                }
                #endregion

                #region //根据点到质心的距离，将点放到不同的组中

                for (int i = 0; i < Num; i++)
                {
                    double tmpDis = 0.0;
                    int index = 0;
                    for (int j = 0; j < k; j++)
                    {
                        double tmpIn = 0.0;
                        for (int m = 0; m < sub; m++)
                        {
                            tmpIn += Math.Pow((inPut[i, m] - tmpCenter[j, m]), 2);
                        }
                        if (j == 0)
                        {
                            tmpDis = tmpIn;
                            index = 0;
                        }
                        else
                        {
                            if (tmpDis > tmpIn)
                            {
                                tmpDis = tmpIn;
                                index = j;
                            }
                        }
                    }
                    int groupKnum = groupNum[index];
                    resultP[index, groupKnum] = i + 1;
                    groupNum[index]++;
                }
                #endregion

                #region //保存质心
                for (int i = 0; i < k; i++)
                    for (int j = 0; j < sub; j++)
                        preCenter[i, j] = tmpCenter[i, j];
                #endregion

                #region //确定新质心
                for (int i = 0; i < k; i++)
                {
                    int kNum = groupNum[i];
                    if (kNum > 0)
                    {
                        for (int j = 0; j < sub; j++)
                        {
                            double tmp = 0.0;
                            for (int m = 0; m < kNum; m++)
                            {
                                int groupIndex = resultP[i, m] - 1;
                                tmp += inPut[groupIndex, j];
                            }
                            tmpCenter[i, j] = tmp / kNum;
                        }
                    }
                }
                #endregion

                #region //判断质心是否变化
                bool judge = true;
                for (int i = 0; i < k; i++)
                {
                    for (int j = 0; j < sub; j++)
                    {
                        judge = judge && (preCenter[i, j] == tmpCenter[i, j]);
                    }
                }
                if (judge)
                {
                    break;
                }
                #endregion

            }
            return resultP;
        }
    }
    public class GetPreCenter
    {
        /// <summary>
        /// 返回Kmeans聚类后的质心点及所属数目
        /// </summary>
        public double[,] PreCenter;
        /// <summary>
        /// 创建通过Kmeans聚类后的质心类,可选择K的取值方式,返回质心信息和所属数目
        /// </summary>
        /// <param name="InPut"></param>
        /// <param name="TypeK">1:取平均值;2:取一半;3:取十分之一</param>
        public GetPreCenter(double[,] InPut, int TypeK)
        {
            int K = new int();
            int num = InPut.GetLength(0);
            int col = InPut.GetLength(1);
            bool err = new bool();
            switch (TypeK)
            {
                default:
                    err = false;
                    break;
                case 1:
                    K = (int)Math.Sqrt(num) + 1;
                    break;
                case 2:
                    K = num / 2;
                    break;
                case 3:
                    K = num / 10;
                    break;
            }
            while (err)
            {
                Kmeans Km = new Kmeans(InPut, K);
                int[,] Repp = Km.GetProcess();
                PreCenter = new double[K, col + 1];
                for (int i = 0; i < K; i++)
                {
                    for (int j = 0; j < col; j++)
                    {
                        PreCenter[i, j] = Km.preCenter[i, j];
                    }
                    PreCenter[i, col] = Km.groupNum[i];
                }
            }
        }
        /// <summary>
        /// 创建通过Kmeans聚类后的质心类，返回质心信息以及结果和所属数目
        /// </summary>
        /// <param name="InPut"></param>
        public GetPreCenter(double[,] InPut)
        {
            int num = InPut.GetLength(0);
            int col = InPut.GetLength(1);
            double[,] input = new double[num, col - 1];
            int[] res=new int[num];//记录每个数据的结果值
            for (int i = 0; i < num; i++)
            {
                for (int j = 0; j < col-1; j++)
                {
                    input[i, j] = InPut[i, j+1];
                }
                res[i] =(int)InPut[i, 0];
            }
            int[,] result=new int[DelRepeatData(res).GetLength(0),2];//结果对应数目的int数组
            for (int i = 0; i < DelRepeatData(res).GetLength(0); i++)//把每个结果的数据至为零
            {
                result[i, 0] = DelRepeatData(res)[i];
                result[i, 1] = 0;
            }
            Kmeans km = new Kmeans(input);
            int[,] repp = km.GetProcess();
            int rk = km.preCenter.GetLength(0);
            int pc = repp.GetLength(1);
            PreCenter = new double[rk, col + 1];
            for (int i = 0; i < rk; i++)//km的k值
            {
                //分析判断哪个结果最后,并赋值给对应质心
                #region 建立一个结果数组，把每种结果的数量计算存储下来
                for (int m = 0; m < repp.GetLength(1); m++)//km返回质心所属数组的结果数据列
                {
                    if (0 != repp[i, m])
                    {
                        for (int j = 0; j < result.GetLength(0); j++)
                        {
                            int inputvalue=(int)InPut[repp[i, m]-1, 0];
                            if (inputvalue == result[j, 0])
                            {
                                result[j, 1]++;
                                break;
                            }
                        }
                    }
                }
                #endregion
                #region 判断结果数组中哪个结果的数量为最多，则用该结果
                int Res = 0;//返回的结果
                int numres=0;
                for (int x = 0; x < result.GetLength(0); x++)
                {
                    if (0 == x)
                    {
                        numres=result[x,1];
                        Res = result[x, 0];
                    }
                    else
                    {
                        if (result[x, 1] > numres)
                        {
                            numres = result[x, 1];
                            Res = result[x, 0];
                        }
                    }
                }
                #endregion
                PreCenter[i, 0] = (double)Res;
                //存储质点的相关信息，不包括结果和数目
                for (int j = 1; j < col-1; j++)
                {
                    PreCenter[i, j] = km.preCenter[i, j];
                }
                PreCenter[i, col] = km.groupNum[i];//存储质点的数目
            }
        }

        #region 去掉double数组中的重复项
        static int[] DelRepeatData(int[] a)
        {
            int len = 0;
            int[] b = new int[a.Length];
            for (int i = 0; i < a.Length; i++, len++)
            {
                b[len] = a[i];
                for (int j = i + 1; j < a.Length; j++)
                {
                    if (a[i] == a[j])
                    {
                        len--; break;
                    }
                }
            }
            int[] new_a = new int[len];
            for (int k = 0; k < len; k++)
            {
                new_a[k] = b[k];
            }
            return new_a;
        }
        #endregion
    }
}
