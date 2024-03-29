'''
提供在线服务
'''

import leancloud,requests
import PySimpleGUI as sg
from plan_manager import *

leancloud.init("OzN2cISaG1cUDK9wLAw2lB4F-gzGzoHsz", "ex4DGUuGw9yQAVoRfwUpbU2p")
sg.set_options(font=('微软雅黑 10'))

def sign_up(User_name:str, password:str) -> (bool|str):
    '''
    注册一个账号

    Args:
        User_name (str): 用户名
        password (str): 密码
    Returns:
        注册成功返回True,否则返回False或者报错字符串
    '''
    account_service = leancloud.User()
    account_service.set_username(User_name)
    account_service.set_password(password)
    try:
        account_service.sign_up()
        print('[Info] Sign up done')
        return True
    except leancloud.errors.LeanCloudError:
        return False
    except TypeError:
        return 'TypeError'
    except requests.exceptions.ConnectionError:
        return 'InternetError'

def log_in(User_name:str, password:str) -> (str|bool):
    '''
    登录一个账号

    Args:
        User_name (str): 用户名
        password (str): 密码
    Returns:
       登录成功返回True,否则返回False或者报错字符串
    '''
    user = leancloud.User()
    try:
        user.login(username=User_name, password=password)
        print('[Info] Log in done')
        user_id=leancloud.User.get_current()
        return user_id
    except leancloud.errors.LeanCloudError:
        return False
    except TypeError:
        return 'TypeError'
    except requests.exceptions.ConnectionError:
        return 'InternetError'

def save_key(Username:str,password:str) -> None:
    '''
    保存登录账号和密码

    Args:
        Username (str): 用户名
        password (str): 密码
    '''
    import json
    User_ID=log_in(Username,password)
    User_services = leancloud.Object.extend('Class_member')
    User_list_services = User_services.query #查询服务
    User_ID_Status = User_list_services.equal_to('User_ID',User_ID).find() #查询该用户ID是否被占用
    if User_ID_Status != []:
        Realname = User_ID_Status[0].get('Realname')
        ClassID = User_ID_Status[0].get('Class_ID')
        key={
            'User_name':Username,
            'Password':password,
            'Realname':Realname,
            'ClassID':ClassID
        }
    else:
        key={
            'User_name':Username,
            'Password':password,
            'Realname':None,
            'ClassID':None
        }
    with open('data/key.json','w') as f:
        f.write(json.dumps(key))

def read_key(Show_Status:bool=False) -> list:
    '''
    读取登录账号和密码

    Args:
        Show_Status (bool): 是否显示用户名
    Returns:
        如果文件存在返回用户名和密码,否则返回False
    '''
    import json,os
    if os.path.isfile('data/key.json'):
        with open('data/key.json','r') as f:
            key=json.loads(f.read())
        Username=key['User_name']
        Realname=key['Realname']
        if Show_Status == True:
            print('[Info] This user is a student. Realname -> ',Realname)
            if Realname != None:
                return Realname
            else:
                return Username
        password=key['Password']
        return Username,password
    else:
        return False

def send_plans() -> None:
    """
    将本地的任务列表发送到云端
    """
    import time
    import PySimpleGUI as sg
    User_name,password=read_key()
    user_id=log_in(User_name=User_name,password=password)
    if user_id == False:
        return None
    #执行删除操作
    Plan_services = leancloud.Object.extend('Plan').query
    Plan_services.equal_to('owner', user_id)
    plan_list = Plan_services.find()
    leancloud.Object.destroy_all(plan_list)
    #获取新的任务列表
    plan_list = read_plan_list()
    #进度条GUI
    layout = [[sg.Text('同步完成进度',font=('微软雅黑 12'))],
            [sg.ProgressBar(len(plan_list), orientation='h', size=(20, 20), key='progressbar')],
            [sg.Text('此操作需要一定时间,感谢您的耐心等待...',font=('微软雅黑 12'))]]
    window = sg.Window('同步进度', layout)
    progress_bar = window['progressbar']
    event, values = window.read(timeout=10)
    i=0
    progress_bar.UpdateBar(i)
    #数据打包并和远程服务器同步
    Plan_services = leancloud.Object.extend('Plan')
    for num in range(len(read_plan_list())):
        Plan_service=Plan_services()
        Plan_service.set('owner',user_id)
        Plan_service.set('sub',get_plan_info(num,'sub'))
        Plan_service.set('text',get_plan_info(num,'text'))
        Plan_service.set('status',get_plan_info(num,'status'))
        atime=get_plan_info(num,'atime')
        if atime!=(None,None):
            Plan_service.set('stime',atime[0])
            Plan_service.set('etime',atime[1])
        des=get_plan_info(num,'des')
        if des!=None:
            Plan_service.set('des',des)
        Plan_service.save()
        i+=1
        time.sleep(1)
        event, values = window.read(timeout=10)
        progress_bar.UpdateBar(i + 1)
    window.Close()
    sg.Popup('已完成数据在云端的备份操作')
    return None

def get_plans() -> None:
    """
    从云端获取任务列表
    """
    from plan_manager import get_newplan_name,save_plan
    import PySimpleGUI as sg
    import shutil,os
    User_name,password=read_key()
    user_id=log_in(User_name=User_name,password=password)
    #确认GUI
    layout=[
        [sg.Text('此操作会清空您的所有任务文件,并获取云端上所有的任务')],
        [sg.Text('因此请注意在程序根目录文件夹下的Plan文件夹备份所需文件')],
        [sg.Text('要继续吗?')],
        [sg.Button('继续'),sg.Push(),sg.Button('返回')]
    ]
    window=sg.Window('还原确认',layout=layout,font=('微软雅黑  10'))
    event,value=window.Read()
    window.Close()
    if event!='继续':
        return None 
    shutil.rmtree('plan')  
    os.mkdir('plan')  
    user_id=log_in(User_name=User_name,password=password)
    if user_id == False:
        return None
    Plan_services = leancloud.Object.extend('Plan').query
    Plan_services.equal_to('owner', user_id)
    plan_list = Plan_services.find()
    for plan in plan_list:
        sub=plan.get('sub')
        text=plan.get('text')
        status=plan.get('status')
        stime=plan.get('stime')
        etime=plan.get('etime')
        des=plan.get('des')
        if stime!=None and etime!=None:
            save_plan(get_newplan_name(),sub,text,stime,etime,des,status)
        else:
            save_plan(get_newplan_name(),sub,text,detail=des,status=status)
    return None

def log_in_gui() -> None:
    """
    登录或注册GUI
    """
    layout=[
        [sg.Text('用户名')],
        [sg.Input()],
        [sg.Text('密码')],
        [sg.Input()],
        [sg.Button('登录'),sg.Push(),sg.Button('注册')]
    ]
    lg=sg.Window('登录或注册',layout,font=('微软雅黑 10'))
    event,value=lg.Read()
    if event==sg.WIN_CLOSED:
        return None
    Username=value[0]
    password=value[1]
    if Username=='' or password=='':
        sg.Popup('用户名和密码不能为空!')
        return None
    if event=='登录':
        Status=log_in(Username,password)
        if not Status:
            sg.Popup('登录失败,可能的原因为:\n1. 密码错误或用户名不存在\n2. 您输入密码的次数过多,请重试...')
            lg.Close()
            return None
        elif Status=='TypeError':
            sg.Popup('登录失败: 用户名无效')
            lg.Close()
            return None
        elif Status=='InternetError':
            sg.Popup('登录失败: 请检查您的网络连接和代理设置')
            lg.Close()
            return None
        sg.Popup('登录成功...')
        lg.Close()
        save_key(Username,password)
        return None
    elif event=='注册':
        status=sign_up(Username,password)
        if status==False:
            sg.Popup('注册失败: 用户名已经存在或用户名存在特殊字符')
            lg.Close()
            return None
        elif status=='TypeError':
            sg.Popup('注册失败: 用户名无效')
            lg.Close()
            return None
        elif status=='InternetError':
            sg.Popup('注册失败: 请检查您的网络连接和代理设置')
            lg.Close()
            return None
        Status=log_in(Username,password)
        if not Status:
            sg.Popup('登录失败,可能的原因为:\n1. 密码错误或用户名不存在\n2. 您输入密码的次数过多,请重试...')
            lg.Close()
            return None
        elif Status=='TypeError':
            sg.Popup('登录失败: 用户名无效')
            lg.Close()
            return None
        elif Status=='InternetError':
            sg.Popup('登录失败: 请检查您的网络连接和代理设置')
            lg.Close()
            return None
        sg.Popup('登录成功...')
        lg.Close()
        save_key(Username,password)
        return None

def log_out():
    """
    登出操作
    """
    from Student import Check_Class_Account
    import os
    if Check_Class_Account():
        if sg.popup_yes_no('一旦登出,本地的作业文件将会删除,要继续吗?',title='确认') == 'Yes':
            from plan_manager import get_plan_info
            plan_list = os.listdir('plan')
            Remove_plan_list = []
            for plan in plan_list:
                if get_plan_info(plan_list.index(plan),'HomeworkID'):
                    Remove_plan_list.append(plan)
            for plan in Remove_plan_list:
                print('[Info]Remove: ',plan)
                os.remove('plan/'+plan)
        else:
            return None
    os.remove('data/key.json')
    sg.Popup('已登出...')
    return None
