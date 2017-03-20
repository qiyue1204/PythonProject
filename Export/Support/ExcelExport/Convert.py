# coding=utf-8



def isnull(x,y):
    if (x is ''):
        return y
    else: 
        return x+' or '
    
def ConvertVehicleType(Value,VehicleType):
    result=''
    if((Value&0x0001)==0x0001):
        result=isnull(result,'')+'('+VehicleType+'&0x20080000)=0x20080000'
    if((Value&0x1000)==0x1000):
        result=isnull(result,'')+'('+VehicleType+'&0x08080000)=0x08080000'
    if((Value&0x0004)==0x0004):
        result=isnull(result,'')+'('+VehicleType+'&0x10080000)=0x10080000'  +' or (' + VehicleType + '&0x02080000)=0x02080000' 
    if((Value&0x0002)==0x0002):
        result=isnull(result,'')+'('+VehicleType+'&0x01080000)=0x01080000'
    if((Value&0x0080)==0x0080):
        result=isnull(result,'')+'('+VehicleType+'&0x00100000)=0x00100000'
    if((Value&0x0010)==0x0010):
        result=isnull(result,'')+'('+VehicleType+'&0x00040001)=0x00040001'
    if((Value&0x0020)==0x0020):
        result=isnull(result,'')+'('+VehicleType+'&0x00040020)=0x00040020'
    if(result is ''):
        result='1=0'
        
    return result
    
def VTypeStrSplit(FuncVType,Func):
    if (FuncVType==''):
        return 0
    else:
        array=[]
        array=(FuncVType.split("||"))
        VtypeStr=array[0]
        Configstr=array[1]
        array1=[]
        array1=(VtypeStr.split(","))
        FirstVtypeStr=array1[0]
        SecondVtypeStr=array1[1]
        ThirdVtypeStr=array1[2]
        FourthVtypeStr=array1[3]
        if(Func==1):
            return int(FirstVtypeStr)
        if(Func==2):
            return int(SecondVtypeStr)
        if(Func==3):
            return int(ThirdVtypeStr)
        if(Func==4):
            return int(FourthVtypeStr)
        
    
def ConvertFuncVType(FuncVType,Func):
    if (FuncVType==''):
        return 0
    else:
        array=[]
        array=(FuncVType.split("||"))
        VtypeStr=array[0]
        Configstr=array[1]
        array1=[]
        array1=(VtypeStr.split(","))
        FirstVtypeStr=array1[0]
        SecondVtypeStr=array1[1]
        ThirdVtypeStr=array1[2]
        FourthVtypeStr=array1[3]
    
        array2=[]
        array2=(Configstr.split(","))
        FirstConfigstr=array2[0]
        SecondConfigstr=array2[1]
        ThirdConfigstr=array2[2]
        FourthConfigstr=array2[3]


        if (FirstVtypeStr == 0):
            where1 = '0'
        else:
            where1 = int(FirstVtypeStr)
        if (int(FirstConfigstr)!= -1 ):
            where11 = ' AND configstatus  = '+FirstConfigstr
        else:
            where11 = ' AND 1=1 '
            
        if (SecondVtypeStr == 0):
            where2 = '0'
        else:
            where2 = int(SecondVtypeStr)
        if (int(SecondConfigstr)!= -1 ):
            where22 = ' AND configstatus  = '+SecondConfigstr
        else:
            where22=' AND 1=1 '    

        if (ThirdVtypeStr == 0):
            where3 = '0'
        else:
            where3 = int(ThirdVtypeStr)
        # if (int(ThirdConfigstr)!= -1 ):
            # where33 = ' AND configstatus  = '+ThirdConfigstr
        # else:
        where33=' AND 1=1 ' 

        if (FourthVtypeStr == 0):
            where4 = '0'
        else:
            where4 = int(FourthVtypeStr)
        # if (int(FourthConfigstr)!= -1 ):
            # where44 = ' AND configstatus  = '+FourthConfigstr
        # else:
        where44=' AND 1=1 '             
            
        if (Func==1):
            return where1
        if (Func==2):
            return where2
        if (Func==3):
            return where3
        if (Func==4):
            return where4
        if (Func==11):
            return where11
        if (Func==22):
            return where22
        if (Func==33):
            return where33
        if (Func==44):
            return where44          
        
        else:
            return 0
            
            
def ConvertDirection(direc):
    direction = (u'正北方向', u'东北方向', u'正东方向', u'东南方向', u'正南方向', u'西南方向', u'正西方向', u'西北方向')
    return direction[((direc + 23) / 45) % 8]
    
def ConvertAlarm(alarm): 
        s=''
        if (alarm & 0x80000000 == 0x80000000): # 紧急报警-大类
            if ((alarm & 0x01) == 0x01):
                s += u'|劫警(无图像)'
            if ((alarm & 0x02) == 0x02):
                s += u'|盗警'
            if ((alarm & 0x04) == 0x04):
                s += u'|超速报警'
            if ((alarm & 0x08) == 0x08):
                s += u'|接收机故障报警'
            if ((alarm & 0x10) == 0x10):
                s += u'|非法点火或非法开门'
        elif (alarm & 0x20000000 == 0x20000000 ): #生成报警-大类
            if ((alarm & 0x10000000) == 0x10000000):
                s += u'|分段线路越界)'
            if ((alarm & 0x08000000) == 0x08000000):
                s += u'|分段超速'
            if ((alarm & 0x04000000) == 0x04000000):
                s += u'|分段低速'
            if ((alarm & 0x02000000) == 0x02000000):
                s += u'|提前进入指定区域'
            if ((alarm & 0x01000000) == 0x01000000):
                s += u'|延迟进入指定区域'
            if ((alarm & 0x00800000) == 0x00800000):
                s += u'|在任意时间进入区域'
            if ((alarm & 0x00400000) == 0x00400000):
                s += u'|提前离开指定区域'
            if ((alarm & 0x00200000) == 0x00200000):
                s += u'|延迟离开指定区域'
            if ((alarm & 0x00100000) == 0x00100000):
                s += u'|在任意时间离开指定区域'
            if ((alarm & 0x00080000) == 0x00080000):
                s += u'|停留区域过长'
            if ((alarm & 0x00040000) == 0x00040000):
                s += u'|停留区域过短'
        if (s != ""):
            s = s[1:]
        return s
    
def ConvertStatus(alarm):# 解析报警状态
        s=''
        if (alarm & 0x40000000 == 0x40000000) : # 状态报警-大类
            if ((alarm & 0x020000) == 0x020000):
                s += u'|油量异常下降'
            if ((alarm & 0x010000) == 0x010000):
                s += u'|驾驶员疲劳驾驶'
            if ((alarm & 0x008000) == 0x008000):
                s += u'|私有状态'
            if ((alarm & 0x004000) == 0x004000):
                s += u'|空重转换'
            if ((alarm & 0x002000) == 0x002000):
                s += u'|劫警(有图像)'
            if ((alarm & 0x001000) == 0x001000):
                s += u'|空车'
            if ((alarm & 0x000800) == 0x000800):
                s += u'|重车'
            if ((alarm & 0x000400) == 0x000400):
                s += u'|电瓶电量低'
            if ((alarm & 0x000200) == 0x000200):
                s += u'|ACC关'
            if ((alarm & 0x000100) == 0x000100):
                s += u'|ACC开'
            if ((alarm & 0x000080) == 0x000080):
                s += u'|GPS数据无效'
            if ((alarm & 0x000040) == 0x000040):
                s += u'|关门'
            if ((alarm & 0x000020) == 0x000020):
                s += u'|开门'
        if (s!= ""):
            s = s[1:]
        return s
        
def FullToHalf(s):
    n = []
    try:
        s = s.decode('gbk')
    except UnicodeDecodeError as err:
        print("###################")
        print(err)
        print(s)
        print("###################")
        import sys
        sys.exit(1)
    for char in s:
        num = ord(char)
        if num == 0x3000:
            num = 32
        elif 0xFF01 <= num <= 0xFF5E:
            num -= 0xfee0
        num = unichr(num)
        n.append(num)
    return ''.join(n)
            
