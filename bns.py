'''
BNS: Background notification service(后台通知服务)
适用于Windows 8 或更高(不包括Windows 11)
存放于程序主目录
'''

def notice(num):
    from win10toast import ToastNotifier
    toaster = ToastNotifier()
    toaster.show_toast("学习待办任务提醒",
                   "您有{}个任务将于10分钟后截止,请尽快完成".format(num),
                   icon_path="ico/Logo.ico",
                   duration=10)
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
        notice(ready_done)
        print('Message Send!')

def main():
    import time
    while True:
        check_plan_status()
        time.sleep(30)

if __name__=='__main__':
    main()