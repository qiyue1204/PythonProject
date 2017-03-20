#coding:utf-8
import xlsxwriter
import sys
reload(sys)
sys.setdefaultencoding('gbk')
def excel():
    workbook = xlsxwriter.Workbook(U'd:\全省卫星定位系统车辆动态统计报表.xlsx')
    titleFormat = workbook.add_format({
        'bold': True,
        'align': 'center',
        'valign': 'vcenter',
        'font_size': 14
    })
    # 居中格式
    centerFormat = workbook.add_format({
        'align': 'center',
        'valign': 'vcenter',
        'text_wrap': True,
        'border': 1,
        'font_size': 10
    })
    # 居中无边框格式
    centerNoBorder = workbook.add_format({
        'align': 'center',
        'valign': 'vcenter',
        'font_size': 10
    })
    # 百分数格式
    percentageFormat = workbook.add_format({
        'align': 'center',
        'valign': 'vcenter',
        'text_wrap': True,
        'border': 1,
        'font_size': 10,
        'num_format': '0.00%'
    })
    # 边框格式
    borderFormat = workbook.add_format({
        'border': 1,
        'font_size': 10,
        'text_wrap': True
    })
    # 描述格式
    descriptionFormat = workbook.add_format({
        'text_wrap': True,
        'font_size': 10
    })
    wsAll = workbook.add_worksheet(U'全省统计表')
    wsAll.set_column(5, 8, 10)
    wsAll.merge_range(3, 5, 4, 8, U'超速', centerFormat)
    wsAll.write(5 ,5 ,U'违章车辆数', centerFormat)
    wsAll.write(5 ,6 ,U'违章车辆比例', centerFormat)
    wsAll.write(5 ,7 ,U'高速≥20%', centerFormat)
    wsAll.write(5 ,8 ,U'非高速≥50%', centerFormat)
    wsAll.set_column(10, 10, 6)
    wsAll.set_column(11, 11, 10)
    wsAll.merge_range(3, 9, 4, 11, U'凌晨2-5点违规运行', centerFormat)
    wsAll.write(5, 9, U'违章车辆数', centerFormat)
    wsAll.write(5, 10, U'次数', centerFormat)
    wsAll.write(5, 11, U'违章车辆比例', centerFormat)
    wsAll.set_column(13, 13, 6)
    wsAll.set_column(14, 14, 10)
    wsAll.merge_range(3, 12, 4, 14, U'持续半小时无数据上传', centerFormat)
    wsAll.write(5, 12, U'违章车辆数', centerFormat)
    wsAll.write(5, 13, U'次数', centerFormat)
    wsAll.write(5, 14, U'违章车辆比例', centerFormat)
    wsAll.set_column(16, 16, 6)
    wsAll.set_column(17, 17, 10)
    wsAll.merge_range(3, 15, 4, 17, U'超4小时运行', centerFormat)
    wsAll.write(5, 15, U'违章车辆数', centerFormat)
    wsAll.write(5, 16, U'次数', centerFormat)
    wsAll.write(5, 17, U'违章车辆比例', centerFormat)
    wsAll.set_row(1, 28.5)
    wsAll.set_column(0, 0, 8)
    wsAll.set_column(1, 4, 12)
    wsAll.set_column(18, 18, 18)
    wsAll.write('A1', U'附件：')
    wsAll.merge_range(1, 0, 1, 18, U'全省卫星定位系统危险货物运输车辆动态统计报表', titleFormat)
    wsAll.write('A3', '816')
    wsAll.write(2, 18, U'单位：辆/次', centerNoBorder)
    wsAll.merge_range(3, 0, 5, 0, U'地区', centerFormat)
    wsAll.merge_range(3, 1, 5, 1, U'车辆应安装总数', centerFormat)
    wsAll.merge_range(3, 2, 5, 2, U'车辆安装总数', centerFormat)
    wsAll.merge_range(3, 3, 5, 3, U'入网率', centerFormat)
    wsAll.merge_range(3, 4, 5, 4, U'上线率', centerFormat)
    wsAll.merge_range(3, 18, 5, 18, U'违章行为次数合计', centerFormat)
    wsAll.freeze_panes(6, 0)
    wsAll.set_tab_color('red')
    workbook.close()
    print 'success!'
excel()


