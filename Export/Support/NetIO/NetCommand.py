# coding=utf8

#本服务主命令
mainCmd = 0x1000
#Excel报表导出主命令
mainCmdExcel = 0x0100
#六严禁一键导出标示字
#serverReserve_sixban = 1
#历史轨迹一键导出标示字
serverReserve = 4
#心跳包子命令
hbCmdRequest = 999
hbCmdResponse = 998
#Hook子命令
hookSubCmd = 50

# UINT16_T        ui16DataLength;         //数据包长度
# UINT16_T        ui16DataSequence;       //数据包序号
# UINT32_T        ui32SourceReserve;      //保留
# UINT16_T        ui16Cmd;                //主命令
# UINT16_T        ui16SubCmd;             //子命令
# UINT32_T        ui32TargetReserve;      //保留
# INT16_T         i16Reserve;             //保留
# INT16_T         i16Result;              //HOOK验证做服务器标志，和主命令功能基本一样
# UINT32_T	      ui32Link;               //链路标记，保留

#导出6严禁报表请求
exportSixBanRequest = 666
#导出普通报表请求
exportNormalRequest = 665
#导出6严禁报表请求结构体
# INT32_T       startDate                   //开始时间
# INT32_T       endDate                     //结束时间
# INT32_T       vehicleType                 //车辆类型
# INT32_T       platformId                  //接入平台ID