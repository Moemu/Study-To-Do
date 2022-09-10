import PySimpleGUI as sg
import leancloud
from account import log_in,read_key

leancloud.init("","") # 自行配置Leancloud的APPID和APPKEY

def Check_Class_Account():
    import json,os
    if os.path.isfile('data/key.json'):
        with open('data/key.json','r') as f:
            key=json.loads(f.read())
        if key['User_name'] != None:
            return True
    else:
        return False

def Get_Class_Account():
    '''
    查询账户所在班级ID
    '''
    import json
    with open('data/key.json','r') as f:
        data=json.loads(f.read())
    if data['Realname'] != None:
        Username,password=read_key()
        User_ID = log_in(Username,password)
        Class_list_services = leancloud.Object.extend('Class_member') #定位到Class_member类
        Class_list_service = Class_list_services.query #查询服务
        Class_ID_Status = Class_list_service.equal_to('User_ID',User_ID).find() #查询该班级ID
        return Class_ID_Status[0].get('Class_ID')
    else:
        return False

def View_Class():
    '''
    查看班级信息
    '''
    Class_ID = Get_Class_Account()
    print(Class_ID)
    # 获取班级名
    Class_list_services = leancloud.Object.extend('Class_list') #定位到Class_list类
    Class_list_service = Class_list_services.query #查询服务
    Class_ID_Status = Class_list_service.equal_to('Class_ID',Class_ID).find() #查询该班级ID
    if len(Class_ID_Status) == 0:
        sg.Popup('该账号尚未绑定任何班级!',font=('微软雅黑 10'))
        return None
    Class_Name =  Class_ID_Status[0].get('Class_Name')
    # 获取班级成员
    Class_services = leancloud.Object.extend('Class_member').query
    Class_services.equal_to('Class_ID', Class_ID)
    Class_list = Class_services.find()
    stu=[]
    for plan in Class_list:
        stu.append(plan.get('Realname'))
    # 班级成员格式化
    text = ', '
    texts = ''
    while stu!=[]:
        print('stu ->',stu)
        texts+=(text.join(stu[:10])+'\n')
        del stu[:10]
    layout = [
        [sg.Text('班级名:',font=('微软雅黑 15')),sg.Text(Class_Name)],
        [sg.Text('班级ID:',font=('微软雅黑 15')),sg.Text(Class_ID)],
        [sg.Text('班级成员:',font=('微软雅黑 15'))],
        [sg.Text(texts)],
        [sg.Push(),sg.Button(tooltip='返回',button_color=(sg.theme_background_color(), sg.theme_background_color()),border_width=0,image_filename='ico/back.png',key='返回')]
    ]
    window = sg.Window('班级信息',layout=layout,font=('微软雅黑 10'))
    window.Read()
    window.Close()
    return None

def Check_New_Homework():
    '''
    检查新作业
    '''
    from account import log_in,read_key
    from plan_manager import save_plan
    import os
    Username,Password = read_key()
    UserID=log_in(Username,Password)
    Homework_list_services = leancloud.Object.extend('Homework_list') #定位到Homework_list类
    Homework_list_service = Homework_list_services.query #查询服务
    Homework_list = Homework_list_service.equal_to('Class_ID',Get_Class_Account()).find() #查询该班级ID
    print('Homework_list -> ',Homework_list)
    #判断是否在作业列表中含有作业
    if Homework_list == []:
        sg.Popup('没有新作业')
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
        sg.Popup('没有新作业')
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
    sg.Popup('有新的作业,请检查!')
    return None

def Finish_Homework(HomeworkID:str,Overtime:bool=False) -> None:
    '''
    完成作业
    :HomeworkID 作业ID
    '''
    Homework_Status_services = leancloud.Object.extend('Homework_Status') #定位到Homework_Status类
    Homework_Status_service = Homework_Status_services() #初始化类
    Homework_Status_service.set('HomeworkID',HomeworkID)
    Homework_Status_service.set('Realname',read_key(True))
    Homework_Status_service.set('User_ID',log_in(list(read_key())))
    Homework_Status_service.set('Overtime',Overtime)
    Homework_Status_service.save()
    return None

if __name__ == '__main__':
    from tool import Run_check
    Run_check()
    Check_New_Homework()