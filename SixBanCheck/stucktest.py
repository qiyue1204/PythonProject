# coding=utf-8
from selenium import webdriver
import time
import os
from selenium.webdriver.support.ui import WebDriverWait
# from _ctypes import Array
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"])
driver = webdriver.Chrome(chrome_options=options)

#登录
def login():    
    driver.get('http://125.71.30.136:8406/')
    driver.maximize_window()
    driver.find_element_by_id("txtUser").send_keys("shm2")
    driver.find_element_by_id("txtPwd").send_keys("123456")
    driver.find_element_by_id("button").click()
#     time.sleep(3)

#退出
def quit():
    time.sleep(3)
    driver.quit()  
    
#建立保存结果的文件夹
def mkdir(path):
    path=path.strip()
    path=path.rstrip("\\")
    isExists=os.path.exists(path)
    if not isExists:
        print path+ " 创建成功"
        os.makedirs(path)
        return True
    else:
        print path+ " 目录已存在"
        return False  
    
#各个页面进入和返回
def check():
    time.sleep(2)
    driver.find_element_by_xpath("//*[@id='home_content_trade_online_plateform']").click()
    time.sleep(2)
    driver.find_element_by_xpath("//*[@id='level_nav']/label[1]").click()
    time.sleep(2)
    driver.find_element_by_xpath("//*[@id='home_platform_chart']/div/canvas[3]").click()
    time.sleep(5)
    driver.find_element_by_xpath("//*[@id='level_nav']/label[1]").click()
    time.sleep(2)
    driver.find_element_by_xpath("//*[@id='home_vehicle_entity']/div/canvas[3]").click()
    time.sleep(2)
    driver.find_element_by_xpath("//*[@id='level_nav']/label[1]").click()
    time.sleep(2)
    driver.find_element_by_xpath("//*[@id='home-index']/div[1]/div[2]/div[2]/a[1]").click()
    time.sleep(2)
    driver.find_element_by_xpath("//*[@id='level_nav']/label[1]").click()
    time.sleep(2)
    driver.find_element_by_xpath("//*[@id='home-index']/div[1]/div[2]/div[2]/a[2]").click()
    time.sleep(2)
    driver.find_element_by_xpath("//*[@id='level_nav']/label[1]").click()
    time.sleep(2)
    driver.find_element_by_xpath("//*[@id='home-index']/div[1]/div[2]/div[2]/a[3]").click()
    time.sleep(2)
    driver.find_element_by_xpath("//*[@id='level_nav']/label[1]").click()
    time.sleep(2)
    driver.find_element_by_xpath("//*[@id='home-index']/div[1]/div[2]/div[2]/a[4]").click()
    time.sleep(2)
    driver.find_element_by_xpath("//*[@id='level_nav']/label[1]").click()
    time.sleep(2)
#查询安装数
def vihicleinstall():
    WebDriverWait(driver, 15).until(lambda x:x.find_element_by_xpath("//*[@id='home-index']/div[1]/div[2]/div[2]/a[3]").is_displayed()) 
    driver.find_element_by_xpath("//*[@id='home-index']/div[1]/div[2]/div[2]/a[3]").click()
    time.sleep(2)
#     driver.find_element_by_xpath("//*[@id='report-index']/div[1]/div/p[1]").click()
    driver.find_element_by_xpath("//*[@id='report_vehicle']/li[1]/a").click()
#地区汇总
    driver.find_element_by_xpath("//*[@id='report_vehicleinstall_table_div_tabs0_ul_nav0']/a").click()
    driver.find_element_by_xpath("//*[@id='report_vehicleinstall_table_div_tabs0_content_panel0_form0_datePeriod0_date0_txt']").clear()
    driver.find_element_by_xpath("//*[@id='report_vehicleinstall_table_div_tabs0_content_panel0_form0_datePeriod0_date0_txt']").send_keys("2016-05-28")
    driver.find_element_by_xpath("//*[@id='report_vehicleinstall_table_div_tabs0_content_panel0_form0_datePeriod0_date1_txt']").clear()
    driver.find_element_by_xpath("//*[@id='report_vehicleinstall_table_div_tabs0_content_panel0_form0_datePeriod0_date1_txt']").send_keys("2016-06-21")
    driver.find_element_by_xpath("//*[@id='report_vehicleinstall_table_div_tabs0_content_panel0_form0_button1_btn']").click()
    WebDriverWait(driver, 120).until(lambda x:x.find_element_by_xpath("//*[@id='report_vehicleinstall_zone_table_table']/tfoot/tr/td[1]").is_displayed())
    t = driver.find_element_by_xpath("//*[@id='report_vehicleinstall_zone_table_table']/tfoot/tr")
    totals = t.find_elements_by_tag_name("td")
    arr_install_zone = []
    for total in totals:
        text = total.text
        arr_install_zone.append(text)
        print text,
    print('\n')     
    
#接入平台汇总
    driver.find_element_by_xpath("//*[@id='report_vehicleinstall_table_div_tabs0_ul_nav1']/a").click()
    driver.find_element_by_xpath("//*[@id='report_vehicleinstall_table_div_tabs0_content_panel1_form0_datePeriod0_date0_txt']").clear()
    driver.find_element_by_xpath("//*[@id='report_vehicleinstall_table_div_tabs0_content_panel1_form0_datePeriod0_date0_txt']").send_keys("2016-05-28")
    driver.find_element_by_xpath("//*[@id='report_vehicleinstall_table_div_tabs0_content_panel1_form0_datePeriod0_date1_txt']").clear()
    driver.find_element_by_xpath("//*[@id='report_vehicleinstall_table_div_tabs0_content_panel1_form0_datePeriod0_date1_txt']").send_keys("2016-06-21")
    driver.find_element_by_xpath("//*[@id='report_vehicleinstall_table_div_tabs0_content_panel1_form0_button1_btn']").click()
    WebDriverWait(driver, 120).until(lambda x:x.find_element_by_xpath("//*[@id='report_vehicleinstall_platform_table_table']/tfoot/tr/td[1]").is_displayed())
    t = driver.find_element_by_xpath("//*[@id='report_vehicleinstall_platform_table_table']/tfoot/tr")
    totals = t.find_elements_by_tag_name("td")
    arr_install_platform = []
    for total in totals:
        text = total.text
        arr_install_platform.append(text)
        print text,
    print('\n')  
    
#企业汇总
    driver.find_element_by_xpath("//*[@id='report_vehicleinstall_table_div_tabs0_ul_nav2']/a").click()
    driver.find_element_by_xpath("//*[@id='report_vehicleinstall_table_div_tabs0_content_panel2_form0_datePeriod0_date0_txt']").clear()
    driver.find_element_by_xpath("//*[@id='report_vehicleinstall_table_div_tabs0_content_panel2_form0_datePeriod0_date0_txt']").send_keys("2016-05-28")
    driver.find_element_by_xpath("//*[@id='report_vehicleinstall_table_div_tabs0_content_panel2_form0_datePeriod0_date1_txt']").clear()
    driver.find_element_by_xpath("//*[@id='report_vehicleinstall_table_div_tabs0_content_panel2_form0_datePeriod0_date1_txt']").send_keys("2016-06-21")
    driver.find_element_by_xpath("//*[@id='report_vehicleinstall_table_div_tabs0_content_panel2_form0_button1_btn']").click()
    WebDriverWait(driver, 120).until(lambda x:x.find_element_by_xpath("//*[@id='report_vehicleinstall_company_table_table']/tfoot/tr/td[3]").is_displayed())
    t = driver.find_element_by_xpath("//*[@id='report_vehicleinstall_company_table_table']/tfoot/tr")
    totals = t.find_elements_by_tag_name("td")
    arr_install_unit = []
    for total in totals:
        text = total.text
        arr_install_unit.append(text)
        print text,
    print('\n')  
    
#车辆安装明细
    driver.find_element_by_xpath("//*[@id='report_vehicleinstall_table_div_tabs0_ul_nav3']/a").click()
    driver.find_element_by_xpath("//*[@id='report_vehicleinstall_table_div_tabs0_content_panel3_form0_date0_txt']").clear()
    driver.find_element_by_xpath("//*[@id='report_vehicleinstall_table_div_tabs0_content_panel3_form0_date0_txt']").send_keys("2016-06-21")
#     driver.find_element_by_xpath("//*[@id='report_vehicleinstall_table_div_tabs0_content_panel2_form0_datePeriod0_date1_txt']").clear()
#     driver.find_element_by_xpath("//*[@id='report_vehicleinstall_table_div_tabs0_content_panel2_form0_datePeriod0_date1_txt']").send_keys("2016-06-21")
#选安装类型
    driver.find_element_by_xpath("//*[@id='report_vehicleinstall_table_div_tabs0_content_panel3_form0_select2']/input").click()
#     t = driver.find_element_by_xpath("//*[@id='report_vehicleinstall_table_div_tabs0_content_panel3_form0_select2']/ul")  
    driver.find_element_by_xpath("//*[@id='report_vehicleinstall_table_div_tabs0_content_panel3_form0_select2']/ul/li[1]").click()  #应安装
    driver.find_element_by_xpath("//*[@id='report_vehicleinstall_table_div_tabs0_content_panel3_form0_button1_btn']").click()
    WebDriverWait(driver, 120).until(lambda x:x.find_element_by_xpath("//*[@id='report_vehicleinstall_detail_table_table_info']").is_displayed())
    text=driver.find_element_by_xpath("//*[@id='report_vehicleinstall_detail_table_table_info']").text
    print text
    
    driver.find_element_by_xpath("//*[@id='report_vehicleinstall_table_div_tabs0_content_panel3_form0_select2']/input").click()
    driver.find_element_by_xpath("//*[@id='report_vehicleinstall_table_div_tabs0_content_panel3_form0_select2']/ul/li[2]").click()  #已安装
    driver.find_element_by_xpath("//*[@id='report_vehicleinstall_table_div_tabs0_content_panel3_form0_button1_btn']").click()
    WebDriverWait(driver, 120).until(lambda x:x.find_element_by_xpath("//*[@id='report_vehicleinstall_detail_table_table_info']").is_displayed())
    text=driver.find_element_by_xpath("//*[@id='report_vehicleinstall_detail_table_table_info']").text
    print text

    driver.find_element_by_xpath("//*[@id='report_vehicleinstall_table_div_tabs0_content_panel3_form0_select2']/input").click()
    driver.find_element_by_xpath("//*[@id='report_vehicleinstall_table_div_tabs0_content_panel3_form0_select2']/ul/li[3]").click()  #未安装
    driver.find_element_by_xpath("//*[@id='report_vehicleinstall_table_div_tabs0_content_panel3_form0_button1_btn']").click()
    WebDriverWait(driver, 120).until(lambda x:x.find_element_by_xpath("//*[@id='report_vehicleinstall_detail_table_table_info']").is_displayed())
    text=driver.find_element_by_xpath("//*[@id='report_vehicleinstall_detail_table_table_info']").text
    print text

#新装车辆明细
    driver.find_element_by_xpath("//*[@id='report_vehicleinstall_table_div_tabs0_ul_nav4']/a").click()
    driver.find_element_by_xpath("//*[@id='report_vehicleinstall_table_div_tabs0_content_panel4_form0_datePeriod0_date0_txt']").clear()
    driver.find_element_by_xpath("//*[@id='report_vehicleinstall_table_div_tabs0_content_panel4_form0_datePeriod0_date0_txt']").send_keys("2016-05-28")
    driver.find_element_by_xpath("//*[@id='report_vehicleinstall_table_div_tabs0_content_panel4_form0_datePeriod0_date1_txt']").clear()
    driver.find_element_by_xpath("//*[@id='report_vehicleinstall_table_div_tabs0_content_panel4_form0_datePeriod0_date1_txt']").send_keys("2016-06-21")
    driver.find_element_by_xpath("//*[@id='report_vehicleinstall_table_div_tabs0_content_panel4_form0_button1_btn']").click()
    WebDriverWait(driver, 120).until(lambda x:x.find_element_by_xpath("//*[@id='report_vehicleinstall_newdetail_table_table_info']").is_displayed())
    text=driver.find_element_by_xpath("//*[@id='report_vehicleinstall_newdetail_table_table_info']").text
    print('\n') 
    print text
    
#返回首页    
    driver.find_element_by_xpath("//*[@id='level_nav']/label[1]").click()
    time.sleep(2)     
  



#查询六严禁
def sixban():
    WebDriverWait(driver, 15).until(lambda x:x.find_element_by_xpath("//*[@id='home-index']/div[1]/div[2]/div[2]/a[4]").is_displayed()) 
    driver.find_element_by_xpath("//*[@id='home-index']/div[1]/div[2]/div[2]/a[4]").click()
    time.sleep(2)
#地区汇总
    driver.find_element_by_id("pro-table-div_tabs0_content_panel0_form0_datePeriod0_date0_txt").clear()
    driver.find_element_by_id("pro-table-div_tabs0_content_panel0_form0_datePeriod0_date0_txt").send_keys("2016-05-28")
    driver.find_element_by_id("pro-table-div_tabs0_content_panel0_form0_datePeriod0_date1_txt").clear()   
    driver.find_element_by_id("pro-table-div_tabs0_content_panel0_form0_datePeriod0_date1_txt").send_keys("2016-06-21")
#选车辆类型
    driver.find_element_by_xpath("//*[@id='pro-table-div_tabs0_content_panel0_form0_select0']/input").click()
    t = driver.find_element_by_xpath("//*[@id='pro-table-div_tabs0_content_panel0_form0_select0']/ul")
    VehicleTypes = t.find_elements_by_tag_name("li")
    i=0
    for VehicleType in VehicleTypes:
        VehicleType.click()
        i=i+1
        if i>=5:
            break

    driver.find_element_by_id("pro-table-div_tabs0_content_panel0_form0_button0_btn").click()
    WebDriverWait(driver, 120).until(lambda x:x.find_element_by_xpath("//*[@id='pro-zone-table_table']/tfoot/tr/td[2]").is_displayed())
    time.sleep(1)
    driver.get_screenshot_as_file(u"E:/Dailydata/2016-06-21/ZoneTable.png")
    t = driver.find_element_by_xpath("//*[@id='pro-zone-table_table']/tfoot/tr")
    totals = t.find_elements_by_tag_name("td")
    arr_zone = []
    for total in totals:
        text = total.text
        arr_zone.append(text)
        print text,
    print('\n')     
    a="%.2f%%" %(float(arr_zone[3])/float(arr_zone[1])*100)   #超速违章车辆比例
    b="%.2f%%" %(float(arr_zone[9])/float(arr_zone[1])*100)   #异动违章车辆比例
    c="%.2f%%" %(float(arr_zone[12])/float(arr_zone[1])*100)   #定位中断违章车辆比例
    d="%.2f%%" %(float(arr_zone[15])/float(arr_zone[1])*100)   #超4小时运行违章车辆比例
    e=float(arr_zone[5])+float(arr_zone[6])+float(arr_zone[7])+float(arr_zone[8]) #超速违章次数
    f=arr_zone[10] #异动违章次数
    g=arr_zone[13] #定位中断违章次数
    h=arr_zone[16] #超4小时运行违章次数
    if a == arr_zone[4]:
        print u"地区汇总超速违章车辆比例计算正确！"
    else:
        print u"地区汇总超速违章车辆比例计算错误！"       
    if b == arr_zone[11]:
        print u"地区汇总异动违章车辆比例计算正确！"
    else:
        print u"地区汇总异动违章车辆比例计算错误！"    
    if c == arr_zone[14]:
        print u"地区汇总定位中断违章车辆比例计算正确！"
    else:
        print u"地区汇总定位中断违章车辆比例计算错误！"        
    if d == arr_zone[17]:
        print u"地区汇总超4小时运行违章车辆比例计算正确！"
    else:
        print u"地区汇总超4小时运行违章车辆比例计算错误！"
#接入平台汇总
    driver.find_element_by_xpath("//*[@id='pro-table-div_tabs0_ul_nav1']/a").click()
    driver.find_element_by_id("pro-table-div_tabs0_content_panel1_form0_datePeriod0_date0_txt").clear()
    driver.find_element_by_id("pro-table-div_tabs0_content_panel1_form0_datePeriod0_date0_txt").send_keys("2016-05-28")
    driver.find_element_by_id("pro-table-div_tabs0_content_panel1_form0_datePeriod0_date1_txt").clear()   
    driver.find_element_by_id("pro-table-div_tabs0_content_panel1_form0_datePeriod0_date1_txt").send_keys("2016-06-21")
#选车辆类型
    driver.find_element_by_xpath("//*[@id='pro-table-div_tabs0_content_panel1_form0_select1']/input").click()
    t = driver.find_element_by_xpath("//*[@id='pro-table-div_tabs0_content_panel1_form0_select1']/ul")
    VehicleTypes = t.find_elements_by_tag_name("li")
    i=0
    for VehicleType in VehicleTypes:
        VehicleType.click()
        i=i+1
        if i>=5:
            break

    driver.find_element_by_id("pro-table-div_tabs0_content_panel1_form0_button1_btn").click()
    WebDriverWait(driver, 120).until(lambda x:x.find_element_by_xpath("//*[@id='pro-service-table_table']/tfoot/tr/td[1]").is_displayed())
    time.sleep(1)
    driver.get_screenshot_as_file(u"E:/Dailydata/2016-06-21/PlatformTable.png")
    t = driver.find_element_by_xpath("//*[@id='pro-service-table_table']/tfoot/tr")
    totals = t.find_elements_by_tag_name("td")
    arr_platform = []
    for total in totals:
        text = total.text
        arr_platform.append(text)
        print text,
    print('\n')       
    a="%.2f%%" %(float(arr_platform[4])/float(arr_platform[2])*100)   #超速违章车辆比例
    b="%.2f%%" %(float(arr_platform[10])/float(arr_platform[2])*100)   #异动违章车辆比例
    c="%.2f%%" %(float(arr_platform[13])/float(arr_platform[2])*100)   #定位中断违章车辆比例
    d="%.2f%%" %(float(arr_platform[16])/float(arr_platform[2])*100)   #超4小时运行违章车辆比例
    if a == arr_platform[5]:
        print u"接入平台汇总超速违章车辆比例计算正确！"
    else:
        print u"接入平台汇总超速违章车辆比例计算错误！"      
    if b == arr_platform[12]:
        print u"接入平台汇总异动违章车辆比例计算正确！"
    else:
        print u"接入平台汇总异动违章车辆比例计算错误！" 
    if c == arr_platform[15]:
        print u"接入平台汇总定位中断违章车辆比例计算正确！"
    else:
        print u"接入平台汇总定位中断违章车辆比例计算错误！"      
    if d == arr_platform[18]:
        print u"接入平台汇总超4小时运行违章车辆比例计算正确！"
    else:
        print u"接入平台汇总超4小时运行违章车辆比例计算错误！"
#地区与接入平台汇总是否一致
    l=len(arr_zone)
    for i in range(1,l):
        if arr_zone[i]!=arr_platform[i+1]:
            print u"地区汇总与接入平台汇总不一致！"
#企业汇总
    driver.find_element_by_xpath("//*[@id='pro-table-div_tabs0_ul_nav2']/a").click()
    driver.find_element_by_id("pro-table-div_tabs0_content_panel2_form0_datePeriod0_date0_txt").clear()
    driver.find_element_by_id("pro-table-div_tabs0_content_panel2_form0_datePeriod0_date0_txt").send_keys("2016-05-28")
    driver.find_element_by_id("pro-table-div_tabs0_content_panel2_form0_datePeriod0_date1_txt").clear()   
    driver.find_element_by_id("pro-table-div_tabs0_content_panel2_form0_datePeriod0_date1_txt").send_keys("2016-06-21")
#选车辆类型
    driver.find_element_by_xpath("//*[@id='pro-table-div_tabs0_content_panel2_form0_select0']/input").click()
    t = driver.find_element_by_xpath("//*[@id='pro-table-div_tabs0_content_panel2_form0_select0']/ul")
    VehicleTypes = t.find_elements_by_tag_name("li")
    i=0
    for VehicleType in VehicleTypes:
        VehicleType.click()
        i=i+1
        if i>=5:
            break

    driver.find_element_by_id("pro-table-div_tabs0_content_panel2_form0_button1_btn").click()
    WebDriverWait(driver, 120).until(lambda x:x.find_element_by_xpath("//*[@id='pro-company-table_table']/tfoot/tr/td[1]").is_displayed())
    time.sleep(1)
    driver.get_screenshot_as_file(u"E:/Dailydata/2016-06-21/UnitTable.png")
    t = driver.find_element_by_xpath("//*[@id='pro-company-table_table']/tfoot/tr")
    totals = t.find_elements_by_tag_name("td")
    arr_unit = []
    for total in totals:
        text = total.text
        arr_unit.append(text)
        print text,
    print('\n')
    a="%.2f%%" %(float(arr_unit[4])/float(arr_unit[2])*100)   #超速违章车辆比例
    b="%.2f%%" %(float(arr_unit[10])/float(arr_unit[2])*100)   #异动违章车辆比例
    c="%.2f%%" %(float(arr_unit[13])/float(arr_unit[2])*100)   #定位中断违章车辆比例
    d="%.2f%%" %(float(arr_unit[16])/float(arr_unit[2])*100)   #超4小时运行违章车辆比例
    if a == arr_unit[5]:
        print u"企业汇总超速违章车辆比例计算正确！"
    else:
        print u"企业汇总超速违章车辆比例计算错误！"       
    if b == arr_unit[12]:
        print u"企业汇总异动违章车辆比例计算正确！"
    else:
        print u"企业汇总异动违章车辆比例计算错误！"
    if c == arr_unit[15]:
        print u"企业汇总定位中断违章车辆比例计算正确！"
    else:
        print u"企业汇总定位中断违章车辆比例计算错误！"    
    if d == arr_unit[18]:
        print u"企业汇总超4小时运行违章车辆比例计算正确！"
    else:
        print u"企业汇总超4小时运行违章车辆比例计算错误！"
#地区与企业汇总是否一致
    for i in [5,6,7,8,9,10,12,13,15,16,18,19]:
        if arr_zone[i]!=arr_unit[i+1]:
            print u"地区汇总与企业汇总不一致！"
#车辆汇总
    driver.find_element_by_xpath("//*[@id='pro-table-div_tabs0_ul_nav3']/a").click()
    driver.find_element_by_id("pro-table-div_tabs0_content_panel3_form0_datePeriod0_date0_txt").clear()
    driver.find_element_by_id("pro-table-div_tabs0_content_panel3_form0_datePeriod0_date0_txt").send_keys("2016-05-28")
    driver.find_element_by_id("pro-table-div_tabs0_content_panel3_form0_datePeriod0_date1_txt").clear()   
    driver.find_element_by_id("pro-table-div_tabs0_content_panel3_form0_datePeriod0_date1_txt").send_keys("2016-06-21")
#选车辆类型
    driver.find_element_by_xpath("//*[@id='pro-table-div_tabs0_content_panel3_form0_select0']/input").click()
    t = driver.find_element_by_xpath("//*[@id='pro-table-div_tabs0_content_panel3_form0_select0']/ul")
    VehicleTypes = t.find_elements_by_tag_name("li")
    i=0
    for VehicleType in VehicleTypes:
        VehicleType.click()
        i=i+1
        if i>=5:
            break

    driver.find_element_by_id("pro-table-div_tabs0_content_panel3_form0_button1_btn").click()
    WebDriverWait(driver, 120).until(lambda x:x.find_element_by_xpath("//*[@id='pro-vehicle-table_table']/tfoot/tr/td[1]").is_displayed())
    time.sleep(1)
    driver.get_screenshot_as_file(u"E:/Dailydata/2016-06-21/VehicleTable.png")
    t = driver.find_element_by_xpath("//*[@id='pro-vehicle-table_table']/tfoot/tr")
    totals = t.find_elements_by_tag_name("td")
    arr_vehicle = []
    for total in totals:
        text = total.text
        arr_vehicle.append(text)
        print text,
    print('\n')
#地区与车辆汇总是否一致
    if arr_zone[5]!=arr_vehicle[4]:
        print u"地区汇总与车辆汇总不一致！"
    if arr_zone[6]!=arr_vehicle[5]:
        print u"地区汇总与车辆汇总不一致！"
    if arr_zone[7]!=arr_vehicle[6]:
        print u"地区汇总与车辆汇总不一致！"
    if arr_zone[8]!=arr_vehicle[7]:
        print u"地区汇总与车辆汇总不一致！"
    if arr_zone[10]!=arr_vehicle[8]:
        print u"地区汇总与车辆汇总不一致！"
    if arr_zone[13]!=arr_vehicle[9]:
        print u"地区汇总与车辆汇总不一致！"
    if arr_zone[16]!=arr_vehicle[10]:
        print u"地区汇总与车辆汇总不一致！"
    if arr_zone[19]!=arr_vehicle[11]:
        print u"地区汇总与车辆汇总不一致！"
#超速违章次数
    driver.find_element_by_xpath("//*[@id='pro-table-div_tabs0_ul_nav4']/a").click()
    driver.find_element_by_xpath("//*[@id='pro-table-div_tabs0_content_panel4_form0_datePeriod0_date0_txt']").clear()
    driver.find_element_by_xpath("//*[@id='pro-table-div_tabs0_content_panel4_form0_datePeriod0_date0_txt']").send_keys("2016-05-28")
    driver.find_element_by_xpath("//*[@id='pro-table-div_tabs0_content_panel4_form0_datePeriod0_date1_txt']").clear()   
    driver.find_element_by_xpath("//*[@id='pro-table-div_tabs0_content_panel4_form0_datePeriod0_date1_txt']").send_keys("2016-06-21")
#选车辆类型
    driver.find_element_by_xpath("//*[@id='pro-table-div_tabs0_content_panel4_form0_select2']/input").click()
    t = driver.find_element_by_xpath("//*[@id='pro-table-div_tabs0_content_panel4_form0_select2']/ul")
    VehicleTypes = t.find_elements_by_tag_name("li")
    i=0
    for VehicleType in VehicleTypes:
        VehicleType.click()
        i=i+1
        if i>=5:
            break

    driver.find_element_by_xpath("//*[@id='pro-table-div_tabs0_content_panel4_form0_button1_btn']").click()
    WebDriverWait(driver, 120).until(lambda x:x.find_element_by_xpath("//*[@id='pro-overSpeed-table_table_info']").is_displayed())
    text=driver.find_element_by_xpath("//*[@id='pro-overSpeed-table_table_info']").text
    print text
    print e
    time.sleep(1)
    driver.get_screenshot_as_file(u"E:/Dailydata/2016-06-21/OverSpeed.png")
#异动违章次数
    driver.find_element_by_xpath("//*[@id='pro-table-div_tabs0_ul_nav5']/a").click()
    driver.find_element_by_xpath("//*[@id='pro-table-div_tabs0_content_panel5_form0_datePeriod0_date0_txt']").clear()
    driver.find_element_by_xpath("//*[@id='pro-table-div_tabs0_content_panel5_form0_datePeriod0_date0_txt']").send_keys("2016-05-28")
    driver.find_element_by_xpath("//*[@id='pro-table-div_tabs0_content_panel5_form0_datePeriod0_date1_txt']").clear()   
    driver.find_element_by_xpath("//*[@id='pro-table-div_tabs0_content_panel5_form0_datePeriod0_date1_txt']").send_keys("2016-06-21")
#选车辆类型
    driver.find_element_by_xpath("//*[@id='pro-table-div_tabs0_content_panel5_form0_select0']/input").click()
    t = driver.find_element_by_xpath("//*[@id='pro-table-div_tabs0_content_panel5_form0_select0']/ul")
    VehicleTypes = t.find_elements_by_tag_name("li")
    i=0
    for VehicleType in VehicleTypes:
        VehicleType.click()
        i=i+1
        if i>=5:
            break

    driver.find_element_by_xpath("//*[@id='pro-table-div_tabs0_content_panel5_form0_button1_btn']").click()
    WebDriverWait(driver, 120).until(lambda x:x.find_element_by_xpath("//*[@id='pro-abnormal-table_table_info']").is_displayed())
    text=driver.find_element_by_xpath("//*[@id='pro-abnormal-table_table_info']").text
    print text
    print f  
    time.sleep(1)
    driver.get_screenshot_as_file(u"E:/Dailydata/2016-06-21/Abnormal.png")
#定位中断违章次数
    driver.find_element_by_xpath("//*[@id='pro-table-div_tabs0_ul_nav6']/a").click()
    driver.find_element_by_xpath("//*[@id='pro-table-div_tabs0_content_panel6_form0_datePeriod0_date0_txt']").clear()
    driver.find_element_by_xpath("//*[@id='pro-table-div_tabs0_content_panel6_form0_datePeriod0_date0_txt']").send_keys("2016-05-28")
    driver.find_element_by_xpath("//*[@id='pro-table-div_tabs0_content_panel6_form0_datePeriod0_date1_txt']").clear()   
    driver.find_element_by_xpath("//*[@id='pro-table-div_tabs0_content_panel6_form0_datePeriod0_date1_txt']").send_keys("2016-06-21")
#选车辆类型
    driver.find_element_by_xpath("//*[@id='pro-table-div_tabs0_content_panel6_form0_select0']/input").click()
    t = driver.find_element_by_xpath("//*[@id='pro-table-div_tabs0_content_panel6_form0_select0']/ul")
    VehicleTypes = t.find_elements_by_tag_name("li")
    i=0
    for VehicleType in VehicleTypes:
        VehicleType.click()
        i=i+1
        if i>=5:
            break

    driver.find_element_by_xpath("//*[@id='pro-table-div_tabs0_content_panel6_form0_button1_btn']").click()
    WebDriverWait(driver, 120).until(lambda x:x.find_element_by_xpath("//*[@id='pro-positionBreak-table_table_info']").is_displayed())
    text=driver.find_element_by_xpath("//*[@id='pro-positionBreak-table_table_info']").text
    print text
    print g
    time.sleep(1)
    driver.get_screenshot_as_file(u"E:/Dailydata/2016-06-21/PositionBreak.png")
#超4小时运行违章次数
    driver.find_element_by_xpath("//*[@id='pro-table-div_tabs0_ul_nav7']/a").click()
    driver.find_element_by_xpath("//*[@id='pro-table-div_tabs0_content_panel7_form0_datePeriod0_date0_txt']").clear()
    driver.find_element_by_xpath("//*[@id='pro-table-div_tabs0_content_panel7_form0_datePeriod0_date0_txt']").send_keys("2016-05-28")
    driver.find_element_by_xpath("//*[@id='pro-table-div_tabs0_content_panel7_form0_datePeriod0_date1_txt']").clear()   
    driver.find_element_by_xpath("//*[@id='pro-table-div_tabs0_content_panel7_form0_datePeriod0_date1_txt']").send_keys("2016-06-21")
#选车辆类型
    driver.find_element_by_xpath("//*[@id='pro-table-div_tabs0_content_panel7_form0_select0']/input").click()
    t = driver.find_element_by_xpath("//*[@id='pro-table-div_tabs0_content_panel7_form0_select0']/ul")
    VehicleTypes = t.find_elements_by_tag_name("li")
    i=0
    for VehicleType in VehicleTypes:
        VehicleType.click()
        i=i+1
        if i>=5:
            break

    driver.find_element_by_xpath("//*[@id='pro-table-div_tabs0_content_panel7_form0_button1_btn']").click()
    WebDriverWait(driver, 120).until(lambda x:x.find_element_by_xpath("//*[@id='pro-over4H-table_table_info']").is_displayed())
    text=driver.find_element_by_xpath("//*[@id='pro-over4H-table_table_info']").text
    print text
    print h  
    time.sleep(1)
    driver.get_screenshot_as_file(u"E:/Dailydata/2016-06-21/Over4hours.png") 
#返回首页    
    driver.find_element_by_xpath("//*[@id='level_nav']/label[1]").click()
    time.sleep(2)     

 
#查询在线率
def onlinerate():
    WebDriverWait(driver, 15).until(lambda x:x.find_element_by_xpath("//*[@id='home-index']/div[1]/div[2]/div[2]/a[3]").is_displayed()) 
    driver.find_element_by_xpath("//*[@id='home-index']/div[1]/div[2]/div[2]/a[3]").click()
    time.sleep(2)
#     driver.find_element_by_xpath("//*[@id='report-index']/div[1]/div/p[1]").click()
    driver.find_element_by_xpath("//*[@id='report_vehicle']/li[2]/a").click()
    time.sleep(2)
#地区汇总
    driver.find_element_by_xpath("//*[@id='report_vehicleonline_table_div_tabs0_ul_nav0']/a").click()
    driver.find_element_by_xpath("//*[@id='report_vehicleonline_table_div_tabs0_content_panel0_form0_date0_txt']").clear()
    driver.find_element_by_xpath("//*[@id='report_vehicleonline_table_div_tabs0_content_panel0_form0_date0_txt']").send_keys("2016-06")
#     driver.find_element_by_xpath("//*[@id='report_vehicleinstall_table_div_tabs0_content_panel0_form0_datePeriod0_date1_txt']").clear()
#     driver.find_element_by_xpath("//*[@id='report_vehicleinstall_table_div_tabs0_content_panel0_form0_datePeriod0_date1_txt']").send_keys("2016-06-21")
    driver.find_element_by_xpath("//*[@id='report_vehicleonline_table_div_tabs0_content_panel0_form0_button1_btn']").click()
    WebDriverWait(driver, 120).until(lambda x:x.find_element_by_xpath("//*[@id='report_vehicleonline_zone_table_table']/tfoot/tr/td[2]").is_displayed())
    t = driver.find_element_by_xpath("//*[@id='report_vehicleonline_zone_table_table']/tfoot/tr")
    totals = t.find_elements_by_tag_name("td")
    arr_online_zone = []
    for total in totals:
        text = total.text
        arr_online_zone.append(text)
        print text,
    print('\n')     
    
#接入平台汇总
    driver.find_element_by_xpath("//*[@id='report_vehicleonline_table_div_tabs0_ul_nav1']/a").click()
    driver.find_element_by_xpath("//*[@id='report_vehicleonline_table_div_tabs0_content_panel1_form0_date0_txt']").clear()
    driver.find_element_by_xpath("//*[@id='report_vehicleonline_table_div_tabs0_content_panel1_form0_date0_txt']").send_keys("2016-06")
#     driver.find_element_by_xpath("//*[@id='report_vehicleinstall_table_div_tabs0_content_panel1_form0_datePeriod0_date1_txt']").clear()
#     driver.find_element_by_xpath("//*[@id='report_vehicleinstall_table_div_tabs0_content_panel1_form0_datePeriod0_date1_txt']").send_keys("2016-06-21")
    driver.find_element_by_xpath("//*[@id='report_vehicleonline_table_div_tabs0_content_panel1_form0_button1_btn']").click()
    WebDriverWait(driver, 120).until(lambda x:x.find_element_by_xpath("//*[@id='report_vehicleonline_platform_table_table']/tfoot/tr/td[3]").is_displayed())
    t = driver.find_element_by_xpath("//*[@id='report_vehicleonline_platform_table_table']/tfoot/tr")
    totals = t.find_elements_by_tag_name("td")
    arr_online_platform = []
    for total in totals:
        text = total.text
        arr_online_platform.append(text)
        print text,
    print('\n')  
    
#企业汇总
    driver.find_element_by_xpath("//*[@id='report_vehicleonline_table_div_tabs0_ul_nav2']/a").click()
    driver.find_element_by_xpath("//*[@id='report_vehicleonline_table_div_tabs0_content_panel2_form0_date0_txt']").clear()
    driver.find_element_by_xpath("//*[@id='report_vehicleonline_table_div_tabs0_content_panel2_form0_date0_txt']").send_keys("2016-06")
#     driver.find_element_by_xpath("//*[@id='report_vehicleinstall_table_div_tabs0_content_panel2_form0_datePeriod0_date1_txt']").clear()
#     driver.find_element_by_xpath("//*[@id='report_vehicleinstall_table_div_tabs0_content_panel2_form0_datePeriod0_date1_txt']").send_keys("2016-06-21")
    driver.find_element_by_xpath("//*[@id='report_vehicleonline_table_div_tabs0_content_panel2_form0_button1_btn']").click()
    WebDriverWait(driver, 120).until(lambda x:x.find_element_by_xpath("//*[@id='report_vehicleonline_company_table_table']/tfoot/tr/td[3]").is_displayed())
    t = driver.find_element_by_xpath("//*[@id='report_vehicleonline_company_table_table']/tfoot/tr")
    totals = t.find_elements_by_tag_name("td")
    arr_online_unit = []
    for total in totals:
        text = total.text
        arr_online_unit.append(text)
        print text,
    print('\n')  
    
#车辆汇总（数据太多，这里不查询）
#     driver.find_element_by_xpath("//*[@id='report_vehicleonline_table_div_tabs0_ul_nav3']/a").click()
#     driver.find_element_by_xpath("//*[@id='report_vehicleonline_table_div_tabs0_content_panel3_form0_date0_txt']").clear()
#     driver.find_element_by_xpath("//*[@id='report_vehicleonline_table_div_tabs0_content_panel3_form0_date0_txt']").send_keys("2016-06")
#     driver.find_element_by_xpath("//*[@id='report_vehicleinstall_table_div_tabs0_content_panel2_form0_datePeriod0_date1_txt']").clear()
#     driver.find_element_by_xpath("//*[@id='report_vehicleinstall_table_div_tabs0_content_panel2_form0_datePeriod0_date1_txt']").send_keys("2016-06-21")
#     driver.find_element_by_xpath("//*[@id='report_vehicleonline_table_div_tabs0_content_panel3_form0_button1_btn']").click()

    
#返回首页    
    driver.find_element_by_xpath("//*[@id='level_nav']/label[1]").click()
    time.sleep(2)     
  


  
     
#查询上线率
def uplinerate():
    WebDriverWait(driver, 15).until(lambda x:x.find_element_by_xpath("//*[@id='home-index']/div[1]/div[2]/div[2]/a[3]").is_displayed()) 
    driver.find_element_by_xpath("//*[@id='home-index']/div[1]/div[2]/div[2]/a[3]").click()
    time.sleep(2)
#     driver.find_element_by_xpath("//*[@id='report-index']/div[1]/div/p[1]").click()
    driver.find_element_by_xpath("//*[@id='report_vehicle']/li[3]/a").click()
    time.sleep(2)
#地区汇总
    driver.find_element_by_xpath("//*[@id='report_vehicleuplinerate_table_div_tabs0_ul_nav0']/a").click()
    driver.find_element_by_xpath("//*[@id='report_vehicleuplinerate_table_div_tabs0_content_panel0_form0_datePeriod0_date0_txt']").clear()
    driver.find_element_by_xpath("//*[@id='report_vehicleuplinerate_table_div_tabs0_content_panel0_form0_datePeriod0_date0_txt']").send_keys("2016-06-21")
    driver.find_element_by_xpath("//*[@id='report_vehicleuplinerate_table_div_tabs0_content_panel0_form0_datePeriod0_date1_txt']").clear()
    driver.find_element_by_xpath("//*[@id='report_vehicleuplinerate_table_div_tabs0_content_panel0_form0_datePeriod0_date1_txt']").send_keys("2016-06-21")
    driver.find_element_by_xpath("//*[@id='report_vehicleuplinerate_table_div_tabs0_content_panel0_form0_button1_btn']").click()
    WebDriverWait(driver, 120).until(lambda x:x.find_element_by_xpath("//*[@id='report_vehicleuplinerate_zone_table_table']/tfoot/tr/td[2]").is_displayed())
    t = driver.find_element_by_xpath("//*[@id='report_vehicleuplinerate_zone_table_table']/tfoot/tr")
    totals = t.find_elements_by_tag_name("td")
    arr_upline_zone = []
    for total in totals:
        text = total.text
        arr_upline_zone.append(text)
        print text,
    print('\n')     
    
#接入平台汇总
    driver.find_element_by_xpath("//*[@id='report_vehicleuplinerate_table_div_tabs0_ul_nav1']/a").click()
    driver.find_element_by_xpath("//*[@id='report_vehicleuplinerate_table_div_tabs0_content_panel1_form0_datePeriod0_date0_txt']").clear()
    driver.find_element_by_xpath("//*[@id='report_vehicleuplinerate_table_div_tabs0_content_panel1_form0_datePeriod0_date0_txt']").send_keys("2016-06-21")
    driver.find_element_by_xpath("//*[@id='report_vehicleuplinerate_table_div_tabs0_content_panel1_form0_datePeriod0_date1_txt']").clear()
    driver.find_element_by_xpath("//*[@id='report_vehicleuplinerate_table_div_tabs0_content_panel1_form0_datePeriod0_date1_txt']").send_keys("2016-06-21")
    driver.find_element_by_xpath("//*[@id='report_vehicleuplinerate_table_div_tabs0_content_panel1_form0_button1_btn']").click()
    WebDriverWait(driver, 120).until(lambda x:x.find_element_by_xpath("//*[@id='report_vehicleuplinerate_platform_table_table']/tfoot/tr/td[2]").is_displayed())
    t = driver.find_element_by_xpath("//*[@id='report_vehicleuplinerate_platform_table_table']/tfoot/tr")
    totals = t.find_elements_by_tag_name("td")
    arr_upline_platform = []
    for total in totals:
        text = total.text
        arr_upline_platform.append(text)
        print text,
    print('\n')  
    
#企业汇总
    driver.find_element_by_xpath("//*[@id='report_vehicleuplinerate_table_div_tabs0_ul_nav2']/a").click()
    driver.find_element_by_xpath("//*[@id='report_vehicleuplinerate_table_div_tabs0_content_panel2_form0_datePeriod0_date0_txt']").clear()
    driver.find_element_by_xpath("//*[@id='report_vehicleuplinerate_table_div_tabs0_content_panel2_form0_datePeriod0_date0_txt']").send_keys("2016-06-21")
    driver.find_element_by_xpath("//*[@id='report_vehicleuplinerate_table_div_tabs0_content_panel2_form0_datePeriod0_date1_txt']").clear()
    driver.find_element_by_xpath("//*[@id='report_vehicleuplinerate_table_div_tabs0_content_panel2_form0_datePeriod0_date1_txt']").send_keys("2016-06-21")
    driver.find_element_by_xpath("//*[@id='report_vehicleuplinerate_table_div_tabs0_content_panel2_form0_button1_btn']").click()
    WebDriverWait(driver, 120).until(lambda x:x.find_element_by_xpath("//*[@id='report_vehicleuplinerate_company_table_table']/tfoot/tr/td[3]").is_displayed())
    t = driver.find_element_by_xpath("//*[@id='report_vehicleuplinerate_company_table_table']/tfoot/tr")
    totals = t.find_elements_by_tag_name("td")
    arr_upline_unit = []
    for total in totals:
        text = total.text
        arr_upline_unit.append(text)
        print text,
    print('\n')  
    
#上线车辆明细
    driver.find_element_by_xpath("//*[@id='report_vehicleuplinerate_table_div_tabs0_ul_nav3']/a").click()
    driver.find_element_by_xpath("//*[@id='report_vehicleuplinerate_table_div_tabs0_content_panel3_form0_datePeriod0_date0_txt']").clear()
    driver.find_element_by_xpath("//*[@id='report_vehicleuplinerate_table_div_tabs0_content_panel3_form0_datePeriod0_date0_txt']").send_keys("2016-06-21")
    driver.find_element_by_xpath("//*[@id='report_vehicleuplinerate_table_div_tabs0_content_panel3_form0_datePeriod0_date1_txt']").clear()
    driver.find_element_by_xpath("//*[@id='report_vehicleuplinerate_table_div_tabs0_content_panel3_form0_datePeriod0_date1_txt']").send_keys("2016-06-21")
    driver.find_element_by_xpath("//*[@id='report_vehicleuplinerate_table_div_tabs0_content_panel3_form0_button1_btn']").click()
    WebDriverWait(driver, 120).until(lambda x:x.find_element_by_xpath("//*[@id='report_vehicleuplinerate_detail_table_table_info']").is_displayed())
    text = driver.find_element_by_xpath("//*[@id='report_vehicleuplinerate_detail_table_table_info']").text
    print text,
    print('\n')  
    
#返回首页    
    driver.find_element_by_xpath("//*[@id='level_nav']/label[1]").click()
    time.sleep(2)     
  


  
# #查车、历史轨迹
# def vehicle_monitor():
 
 
 
    
login()
#quit()
# for i in range(5):
#     check()
# sixban()
# vihicleinstall()
# onlinerate()
uplinerate()
