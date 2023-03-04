import os,json
from tool import check_time
import PySimpleGUI as sg

def time_get():
    mins=[]
    for i in range(0,60):
        if i <=9:
            i='0'+str(i)
        else:
            i=str(i)
        mins.append(i)
    hour=[]
    for i in range(0,24):
        if i <=9:
            i='0'+str(i)
        else:
            i=str(i)
        hour.append(i)
    day=[]
    for i in range(1,32):
        if i <=9:
            i='0'+str(i)
        else:
            i=str(i)
        day.append(i)
    mon=[]
    for i in range(1,13):
        if i <=9:
            i='0'+str(i)
        else:
            i=str(i)
        mon.append(i)
    year=[]
    for i in range(2021,2031):
        i=str(i)
        year.append(i)
    return year,mon,day,hour,mins

def get_newplan_name():
    '''
    获取到新任务的文件名
    返回: 'xx.json' -> str
    '''
    from tool import repair_num
    try:
        lastname=os.listdir('plan')[-1:][0].rstrip('.json')
        newname=str(int(lastname)+1)
        if len(newname)<2:
            newname='0'+newname
        return newname+'.json'
    except:
        txtnum=0
        dirtree=os.listdir('plan')
        while True:
            txtnum+=1
            txtname=repair_num(txtnum)+'.json'
            if not txtname in dirtree:
                return txtname
            else:               
                pass
    
def time_gets() -> tuple:
    '''
    返回时间设定的初始值
    '''
    import time,datetime
    Now_time=time.localtime()
    Now_time_year=time.strftime("%Y", Now_time)
    Now_time_mon=time.strftime("%m", Now_time)
    Now_time_day=time.strftime("%d", Now_time)
    Now_time_hour=time.strftime("%H", Now_time)
    Now_time_min=time.strftime("%M", Now_time)
    Now_time=time.strftime('%Y-%m-%d-%H-%M',Now_time)
    future_time=datetime.datetime.strptime(Now_time,'%Y-%m-%d-%H-%M')+datetime.timedelta(minutes=20)
    future_time_year,future_time_mon,future_time_day,future_time_hour,future_time_min=future_time=datetime.datetime.strftime(future_time,'%Y-%m-%d-%H-%M').split('-')
    return Now_time_year,Now_time_mon,Now_time_day,Now_time_hour,Now_time_min,future_time_year,future_time_mon,future_time_day,future_time_hour,future_time_min

def time_seter(value:str) -> str:
    '''
    截止时间设定,返回结束时间
    '''
    from datetime import datetime,timedelta
    nowtime = datetime.now()
    if value.find('分钟后') != -1:
        mins = int(value.rstrip('分钟后'))
        endtime =  timedelta(minutes=mins)
    elif value.find('小时后') != -1:
        hours = int(value.rstrip('小时后'))
        endtime =  timedelta(hours=hours)
    else:
        endtime =  timedelta(days=1)
    endtime = datetime.strftime(nowtime + endtime, '%Y-%m-%d %H:%M')
    return endtime

def save_plan(txtname:str,sub:str,plan:str,
    stime=None,etime=None,
    detail=None,status='进行中',
    HomeworkID=None):
    '''
    保存任务
    导入变量列表: 文档名,科目,计划,开始结束时间,描述(detail),状态(status),HomeworkID
    '''
    with open('plan/'+txtname,mode='w') as f:
        f.write(json.dumps({'sub':sub,'text':plan,'stime':stime,'etime':etime,'des':detail,'status':status,'HomeworkID':HomeworkID},sort_keys=True, indent=4, separators=(',', ': ')))

def add_plan():
    import time,datetime
    from Teacher import Get_Plan_ID,Send_Plan
    layout=[
        [sg.Text('科目:')],
        [sg.InputCombo(['语文','数学','英语','物理','历史','化学','生物','地理','政治','体育','生活','其他'],size=(12,5))],
        [sg.Text('标题(20字以下)')],
        [sg.Input('')],
        [sg.Text('描述(可选)',font=('微软雅黑 10'))],
        [sg.Multiline(size=(55,12),font=('微软雅黑 8'))],
        [sg.Text('截止时间(可选):'),sg.InputCombo(['禁用','10分钟后','20分钟后','30分钟后','1小时后','2小时后','3小时后','6小时后','12小时后','1天后'],default_value='禁用',size=(12,5))],
        [sg.Text('或者指定具体开始/结束时间:'),sg.Checkbox('启用',font=('微软雅黑 8')),sg.Text(' (将在下一窗口设置)')],
        [sg.Button('下一步')]
    ]
    window=sg.Window('新建自定义作业',layout=layout,icon='ico/LOGO.ico',font=('微软雅黑 10'))
    event,value=window.Read()
    print('任务新建输出: ',value)
    if event==sg.WIN_CLOSED:
        return None
    sub=value[0]
    title=value[1]
    des=value[2]
    etime=value[3]
    detail_time=value[4]
    if des == '':
        des = None
    if etime == '禁用':
        stime = None
        etime  = None
    else:
        stime = datetime.datetime.strftime(datetime.datetime.now(),'%Y-%m-%d %H:%M')
        etime = time_seter(value[3])
    #切换页面前的检查
    if title == '' or not sub in ['语文','数学','英语','物理','历史','化学','生物','地理','政治','体育','生活','其他']:
        sg.popup('任务/科目有误,不应为空或是超出选择范围内的科目',font=('微软雅黑 10'))
        window.Close()
        return None
    if not 0<len(title)<20:
        sg.popup('任务字数有误, 应大于0且小于或等于20',font=('微软雅黑 10'))
        window.Close()
        return None
    #高级选项
    if detail_time==True:
        Glayout=[]
        year,mon,day,hour,mins=time_get()
        Now_time_year,Now_time_mon,Now_time_day,Now_time_hour,Now_time_min,future_time_year,future_time_mon,future_time_day,future_time_hour,future_time_min=time_gets()
        Glayout.append([sg.Text('时间限制(年/月/日/时/分):',font=('微软雅黑 10'))])
        Glayout.append([sg.Text('起始时间',font=('微软雅黑 8')),
        sg.InputCombo(year,Now_time_year,size=(6,5)),sg.InputCombo(mon,Now_time_mon,size=(6,5)),sg.InputCombo(day,Now_time_day,size=(6,5)),sg.InputCombo(hour,Now_time_hour,size=(6,5)),sg.InputCombo(mins,Now_time_min,size=(6,5))])
        Glayout.append([sg.Text('终止时间',font=('微软雅黑 8')),
        sg.InputCombo(year,future_time_year,size=(6,5)),sg.InputCombo(mon,future_time_mon,size=(6,5)),sg.InputCombo(day,future_time_day,size=(6,5)),sg.InputCombo(hour,future_time_hour,size=(6,5)),sg.InputCombo(mins,future_time_min,size=(6,5))])
        Glayout.append([sg.Button('提交',font=('微软雅黑 8'))])
        Gwindow=sg.Window('高级设置',layout=Glayout,icon='ico/LOGO.ico')
        event,values=Gwindow.Read()
        print('任务高级页面输出: ',values)
        if event==sg.WIN_CLOSED:
            window.Close()
            Gwindow.Close()
            return None
        newplan_name=get_newplan_name()
        result=check_time(values[0],values[1],values[2],values[3],values[4],values[5],values[6],values[7],values[8],values[9])
        if result==False:
            sg.popup('时间格式错误,请检查您的开始/结束时间是否正确',font=('微软雅黑 10'))
            window.Close()
            Gwindow.Close()
            return None
        stime,etime=result
        Gwindow.Close()
    HomeworkID = Get_Plan_ID()
    Filename = HomeworkID + '.json'
    save_plan(Filename,sub,title,stime,etime,des,HomeworkID=HomeworkID)
    Send_Plan(HomeworkID)
    sg.popup('作业发布成功~',font=('微软雅黑 10'))
    window.Close()

def read_plan_list():
    '''
    获取到任务列表
    '''
    dirtree=os.listdir('plan')
    txtname_list=[]
    for txtname in range(len(dirtree)):
        if dirtree[txtname][-5:]=='.json':
            txtname_list.append(txtname)
    return txtname_list

def get_plan_info(num,mode:str,Path=None):
    '''
    获取任务信息
    :num 任务索引号
    :mode 可以为'sub','text','des','status','atime'(返回任务起始时间和结束时间),'HomeworkID,'all'(返回全部信息)
    :Path(Debug) 返回测试数据: True/False
    '''
    if mode=='atime':
        txtname=os.listdir('plan')[int(num)]
        with open('plan/'+txtname,'r') as f:
            data=json.loads(f.read())
            st=data['stime']
            et=data['etime']
        return st,et
    elif mode=='all':
        txtname=os.listdir('plan')[int(num)]
        with open('plan/'+txtname,'r') as f:
            data=json.loads(f.read())
            return data.values()
    if Path!=None:
        try:
            with open('plan/'+Path,'r') as f:
                status=json.loads(f.read())['status']
            return True
        except:
            return False
    txtname=os.listdir('plan')[int(num)]
    with open('plan/'+txtname,'r') as f:
        info=json.loads(f.read())[mode]
    return info

def read_plan_with_sub(sub):
    dirtree=os.listdir('plan')
    pass_plans=[]
    for txtnum in range(len(dirtree)):
        plan_sub=get_plan_info(txtnum,'sub')
        if plan_sub==sub:
            print('pass: ',txtnum)
            pass_plans.append(txtnum)
    print(pass_plans)
    return pass_plans

def read_plan_with_time(time):
    dirtree=os.listdir('plan')
    pass_plans=[]
    for txtnum in range(len(dirtree)):
        st,et=get_plan_info(txtnum,'atime')
        if et!=None:            
            if et.split(' ')[0]==time:
                pass_plans.append(txtnum)
    return pass_plans

def read_plan_with_setting(setting):
    '''
    按照传入的设置变量返回符合要求的任务文件列表
    '''
    try:
        setting=setting.split('-')[1]
    except:
        txtname_list=read_plan_list()
    if setting in ['语文','数学','英语','物理','历史','化学','生物','地理','政治','体育','生活','其他']:
        txtname_list=read_plan_with_sub(setting)
    elif setting=='当天':
        from datetime import datetime
        time = datetime.now() #获取当前时间
        realtime = time.strftime("%Y-%m-%d")
        txtname_list=read_plan_with_time(realtime)
    elif setting=='当周':
        from datetime import datetime,timedelta
        txtname_list=[]
        for i in range(8):
            time = datetime.now() + timedelta(days=i)
            time = time.strftime("%Y-%m-%d")
            plan_name=read_plan_with_time(time)
            txtname_list.extend(plan_name)
    elif setting=='已超时':
        Old_txtname_list=read_plan_list()
        txtname_list=[]
        for num in Old_txtname_list:
            if check_plan_time(num):
                txtname_list.append(num)
    return txtname_list

def change_plan_time(num,st=False,et=False):
    '''
    更改指定任务的开始或完成时间, 使其适应当前时间
    num -> 任务索引
    st,et ->开始/结束模式切换(默认为False)
    '''
    from datetime import datetime
    nt=datetime.strftime(datetime.now(),'%Y-%m-%d %H:%M')
    txtname=os.listdir('plan')[int(num)]
    with open('plan/'+txtname,'r') as f:
        data=json.loads(f.read())
    pst,pet=get_plan_info(num,'atime')
    if st:
        data['stime']=pst
        with open('plan/'+txtname,'w') as f:
            f.write(json.dumps(data,sort_keys=True, indent=4, separators=(',', ': ')))
    if et:
        data['etime']=pet
        with open('plan/'+txtname,'w') as f:
            f.write(json.dumps(data,sort_keys=True, indent=4, separators=(',', ': ')))
    return None

def Complete_plan(num,mode='Now'):
    '''
    对任务进行完成操作
    num -> 任务索引
    mode(可选) -> 完成模式(默认值: Now)
    '''
    txtname=os.listdir('plan')[int(num)]
    with open('plan/'+txtname,'r') as f:
        data=json.loads(f.read())
    data['status']='已结束'
    with open('plan/'+txtname,'w') as f:
        f.write(json.dumps(data,sort_keys=True,indent=4,separators=(',', ': ')))
    if get_plan_info(num,'atime')!=(None,None) and mode=='Now':
        change_plan_time(num,et=True)
    return None

def check_plan_time(num):
    '''
    检查任务是否超时
    若超时,返回True
    否则为False
    '''
    from datetime import datetime
    st,et=get_plan_info(num,'atime')
    if et==None:
        return None
    et=datetime.strptime(et,'%Y-%m-%d %H:%M')
    nt=datetime.now()
    if et<nt:
        return True
    else:
        return False

def show_plan(num):
    txtname=os.listdir('plan')[int(num)]
    with open('plan/'+txtname,'r') as f:
        txt=f.read()
    text=txt.split(' 计划')[0]+'\n'+'计划'+txt.split('计划')[1].split('状态')[0].split('时间:')[0].split('描述:\n')[0].split('\n')[0]
    try:
        text+='\n'+'任务开始与结束时间: '+txt.split('时间: ')[1].split('\n')[0]
    except:
        pass
    try:
        text+='\n'+'描述:\n'+txt.split('描述:\n')[1].rstrip('\n')
    except:
        pass
    return text

def get_plan_time(num) -> str:
    '''
    获取任务完成周期
    '''
    from datetime import datetime
    txtname=os.listdir('plan')[int(num)]
    with open('plan/'+txtname,'r') as f:
        txt=f.read()
    try:
        times=txt.split('时间: ')[1].split('\n')[0]
        st=times.split('~')[0]
        et=times.split('~')[1]
        et=datetime.strptime(et,"%Y-%m-%d %H:%M")
        st=datetime.strptime(st,"%Y-%m-%d %H:%M")
        ct=round((et-st).total_seconds()/60/60,2)
        return ct
    except:
        return None

def change_plan(num):
    '''
    更改任务页面
    '''
    from tool import split_time,repair_num
    txtname=os.listdir('plan')[int(num)]
    HomeworkID,des,etime,status,stime,sub,plan=get_plan_info(num,'all')
    if des == None:
        des = ''
    layout=[
        [sg.Text('科目:')],
        [sg.InputCombo(['语文','数学','英语','物理','历史','化学','生物','地理','政治','体育','生活','其他'],default_value=sub,size=(12,5))],
        [sg.Text('标题(20字以下):')],
        [sg.Input(plan)],
        [sg.Text('描述(可选):')],
        [sg.Multiline(des,size=(55,12),font=('微软雅黑 8'))],
        [sg.Text('截止时间(无法更改,请至下方的高级选项中更更改)):'),sg.InputCombo(['(编辑时此项不可用)'],default_value='(编辑时此项不可用)',size=(12,5))],
        [sg.Text('编辑具体开始/结束时间:'),sg.Checkbox('启用',font=('微软雅黑 8')),sg.Text(' (将在下一窗口设置)')],
        [sg.Button('下一步')]
    ]
    window=sg.Window('编辑任务',layout=layout,icon='ico/LOGO.ico',font=('微软雅黑 10'))
    event,value=window.Read()
    if event==sg.WIN_CLOSED:
        return None
    sub=value[0]
    title=value[1]
    des=value[2]
    detail_time=value[4]
    if des == '':
        des = None
    #切换页面前的检查
    if event==sg.WIN_CLOSED:
        return None
    if title == '' or not sub in ['语文','数学','英语','物理','历史','化学','生物','地理','政治','体育','生活','其他']:
        sg.popup('任务/科目有误,不应为空或是超出选择范围内的科目',font=('微软雅黑 10'))
        window.Close()
        return None
    if not 0<len(title)<20:
        sg.popup('任务字数有误, 应大于0且小于或等于20',font=('微软雅黑 10'))
        window.Close()
        return None
    #高级选项
    if detail_time==True:
        year,mon,day,hour,mins=time_get()
        if stime == None and etime == None:
            sty,stM,std,sth,stm,ety,etM,etd,eth,etm=time_gets()
        else:
            sty,stM,std,sth,stm,ety,etM,etd,eth,etm=split_time(stime+'~'+etime)
        Glayout=[]
        Glayout.append([sg.Text('时间限制(年/月/日/时/分):',font=('微软雅黑 10'))])
        Glayout.append([sg.Text('起始时间',font=('微软雅黑 8')),
        sg.InputCombo(year,sty,size=(6,5)),sg.InputCombo(mon,stM,size=(6,5)),sg.InputCombo(day,std,size=(6,5)),sg.InputCombo(hour,sth,size=(6,5)),sg.InputCombo(mins,stm,size=(6,5))])
        Glayout.append([sg.Text('终止时间',font=('微软雅黑 8')),
        sg.InputCombo(year,ety,size=(6,5)),sg.InputCombo(mon,etM,size=(6,5)),sg.InputCombo(day,etd,size=(6,5)),sg.InputCombo(hour,eth,size=(6,5)),sg.InputCombo(mins,etm,size=(6,5))])
        Glayout.append([sg.Button('提交',font=('微软雅黑 8'))])
        Gwindow=sg.Window('高级设置',layout=Glayout,icon='ico/LOGO.ico')
        event,values=Gwindow.Read()
        print('任务高级页面输出: ',values)
        if event==sg.WIN_CLOSED:
            window.Close()
            Gwindow.Close()
            return None
        result=check_time(values[0],values[1],values[2],values[3],values[4],values[5],values[6],values[7],values[8],values[9])
        if result==False:
            sg.popup('时间格式错误,请检查您的开始/结束时间是否正确',font=('微软雅黑 10'))
            window.Close()
            Gwindow.Close()
            return None
        stime,etime=result
        Gwindow.Close()
    save_plan(txtname,sub,title,stime,etime,des)
    window.Close()
    return None