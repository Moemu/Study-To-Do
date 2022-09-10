'''
BNS: Background notification service(后台通知服务)
存放于程序主目录
'''
import platform,leancloud
import PySimpleGUI as sg
from windows_toasts import WindowsToaster, ToastImageAndText4

leancloud.init("","") # 自行配置Leancloud的APPID和APPKEY

def notice(text):
    #判断Windows版本是否高于Windows 8
    if int(platform.release()) >= 8:
        newToast = ToastImageAndText4()
        newToast.SetHeadline("学习待办任务提醒")
        newToast.SetBody(text)
        newToast.SetImage('ico/Logo.ico')
        # newToast.on_activated = lambda _: print('Toast clicked!')
        WindowsToaster('School Mail').show_toast(newToast)
    else:
        sg.set_options(font=('微软雅黑 10'))
        sg.popup_notify(text,title='学习待办任务提醒',display_duration_in_ms=5000)
    return None

def check_plan_status():
    from plan_manager import read_plan_list,get_plan_info
    from datetime import datetime,timedelta
    import os
    os.chdir(os.getenv('APPDATA')+r'\Study to do')
    ready_done = 0
    plan_list = read_plan_list()
    for plan_name in range(len(plan_list)):
        st,et=get_plan_info(int(plan_name)-1,'atime')
        nt=datetime.now()+timedelta(seconds=600)
        nt=datetime.strftime(nt,'%Y-%m-%d %H:%M')
        if et==nt:
            ready_done+=1
    if ready_done!=0:
        notice("您有{}个任务将于10分钟后截止,请尽快完成".format(ready_done))
        print('Message Send!')

def Check_New_Homework():
    '''
    检查新作业
    '''
    from account import log_in,read_key
    from plan_manager import save_plan
    from Student import Get_Class_Account
    import os
    Username,Password = read_key()
    UserID=log_in(Username,Password)
    Homework_list_services = leancloud.Object.extend('Homework_list') #定位到Homework_list类
    Homework_list_service = Homework_list_services.query #查询服务
    Homework_list = Homework_list_service.equal_to('Class_ID',Get_Class_Account()).find() #查询该班级ID
    print('Homework_list -> ',Homework_list)
    #判断是否在作业列表中含有作业
    if Homework_list == []:
        return None
    HomeworkID_list = []
    for h in Homework_list:
        HomeworkID_list.append(h.get('HomeworkID'))
    #移除已完成的作业
    Homework_Status_services = leancloud.Object.extend('Homework_Status') #定位到Homework_Status类
    Homework_Status_service = Homework_Status_services.query #查询服务
    Homework_Done_list = Homework_Status_service.equal_to('User_ID',UserID).find() #查询该用户ID
    print('Homework_Done_list -> ',Homework_Done_list)
    for h in Homework_Done_list:
        HomeworkID_list.remove(h.get('HomeworkID'))
    OldHomeworkID_list = HomeworkID_list.copy()
    for h in OldHomeworkID_list:
        Plan_list = os.listdir('plan')
        if h+'.json' in Plan_list:
            HomeworkID_list.remove(h)
    print('Homework_list -> ',Homework_list)
    if HomeworkID_list == []:
        return None
    for hid in HomeworkID_list:
        Homework_list_services = leancloud.Object.extend('Homework_list') #定位到Homework_list类
        Homework_list_service = Homework_list_services.query #查询服务
        AHomework = Homework_list_service.equal_to('HomeworkID',hid).find()[0] #查询该任务ID
        sub = AHomework.get('sub')
        plan = AHomework.get('plan')
        stime = AHomework.get('stime')
        etime = AHomework.get('etime')
        des = AHomework.get('des')
        save_plan(hid+'.json',sub,plan,stime,etime,des,HomeworkID=hid)
    notice('有新的作业,请检查!')
    return None

def main():
    import time
    while True:
        check_plan_status()
        Check_New_Homework()
        time.sleep(30)

if __name__=='__main__':
    main()