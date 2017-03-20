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
    
def ConvertFuncVType(FuncVtype,Func):
    array=[]
    array=(FuncVtype.split("||"))
    VtypeStr=array[0]
    Configstr=array[1]
    array1=[]
    array1=(VtypeStr.split(","))
    FirstVtypeStr=array1[0]
    SecondVtypeStr=array1[1]
#     ThirdVtypeStr=array1[2]
#     ForthVtypeStr=array1[3]
    
    array2=[]
    array2=(Configstr.split(","))
    FirstConfigstr=array2[0]
    SecondConfigstr=array2[1]
#     ThirdConfigstr=array2[2]
#     ForthConfigstr=array2[3]

    if (FirstVtypeStr == 0):
        where1 = '1=1'
    else:
        where1 = ' (' +ConvertVehicleType(int(FirstVtypeStr), 'N.VehicleType') + ')'  
        
    if (int(FirstConfigstr)!=-1 ):
        where1 = where1 + ' AND  configstatus  = '+FirstConfigstr
    else:
        where1 = where1
    
    if (SecondVtypeStr == 0):
        where2 = '1=1'
    else:
        where2 = ' (' +ConvertVehicleType(int(SecondVtypeStr), 'N.VehicleType') + ')'  
        
    if (SecondConfigstr!=-1 ):
        where2 = where2 + ' AND  configstatus  = '+SecondConfigstr
    else:
        where2=where2
        
    if (Func==1):
        return where1
    if (Func==2):
        return where2
    else:
        return 0
