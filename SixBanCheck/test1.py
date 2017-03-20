

ALTER   Function  [dbo].[FN_GOV_Split_FuncVtypeFilter]
(
    @FuncVtype  varchar (100),
    @Func  Int 
)
returns varchar(4000)
AS 

BEGIN
    
    Declare @where    varchar(2000)
    Declare @CNT INT  = 1
    Declare @VTypeString varchar(50) =''
    
    Declare @VtypeStr varchar(50) --截取后的第一个字符串
    Declare @Configstr varchar(1000) --截取第一个字符串后剩余的字符串
    
    Declare @FistVtypeStr varchar(50) --截取后的第一个字符串
    Declare @NewVtypestr varchar(1000) --截取第一个字符串后剩余的字符串
    
    Declare @FistConfigStr varchar(50) --截取后的第一个字符串
    Declare @NewConfigstr varchar(1000) --截取第一个字符串后剩余的字符串
    
    SET @VtypeStr  = left(@FuncVtype,charindex('||',@FuncVtype)-1)
    SET @Configstr = stuff(@FuncVtype,1,charindex('||',@FuncVtype)+1,'')
    
    SET @where  = ''
    SET  @VtypeStr += ',' 
    SET @Configstr +=','
    

    SET  @FistVtypeStr  = left(@VtypeStr,charindex(',',@VtypeStr)-1)
    SET  @NewVtypestr = stuff(@VtypeStr,1,charindex(',',@VtypeStr),'')
    
       IF (@FistVtypeStr =0  ) 
        SET @WHERE = '1=1'
        ELSE 
        SET @WHERE  = '  (' + dbo.FN_GOV_Get_IVTypeStr_ByQuery(@FistVtypeStr, 'N.VehicleType') + ')'    
    
    SET  @FistConfigStr  = left(@Configstr,charindex(',',@Configstr)-1)
    SET @NewConfigstr = stuff(@Configstr,1,charindex(',',@Configstr),'')
    
    IF (@FistConfigStr <>-1 )
    SET  @where += ' AND  configstatus  = '+@FistConfigStr
    
    
    IF  ( @Func = @CNT )return  (@where)       
    WHILE (len(@NewVtypestr)>0)
    BEGIN 
        SET   @FistVtypeStr =left(@NewVtypestr,charindex(',',@NewVtypestr)-1)
        SET @NewVtypestr = stuff(@NewVtypestr,1,charindex(',',@NewVtypestr),'')
        
        SET  @FistConfigStr  = left(@NewConfigstr,charindex(',',@NewConfigstr)-1)
        SET @NewConfigstr = stuff(@NewConfigstr,1,charindex(',',@NewConfigstr),'')

       
        IF (@FistVtypeStr =0  ) 
        SET @WHERE = '1=1'
        ELSE 
        SET @WHERE  = '  (' + dbo.FN_GOV_Get_IVTypeStr_ByQuery(@FistVtypeStr, 'N.VehicleType') + ')'    
        
        IF (@FistConfigStr <>-1 )
        SET  @where +=  ' AND   configstatus  = '+@FistConfigStr
        
        SET @CNT =@CNT +1  
    IF  ( @Func = @CNT ) return  (@where)
 
    END 
    
    return  (@where)


END 
