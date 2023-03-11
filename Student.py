import PySimpleGUI as sg
import leancloud
from datetime import datetime
from account import log_in,read_key

leancloud.init("OzN2cISaG1cUDK9wLAw2lB4F-gzGzoHsz", "ex4DGUuGw9yQAVoRfwUpbU2p")

def Check_Class_Account() -> bool:
    import json,os
    if os.path.isfile('data/key.json'):
        with open('data/key.json','r') as f:
            key=json.loads(f.read())
        if key['User_name'] != None:
            return True
    else:
        return False

def Get_Class_Account() -> str or bool:
    '''
    查询账户所在班级ID
    '''
    import json
    with open('data/key.json','r') as f:
        data=json.loads(f.read())
    return data['ClassID']

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

class Class_Chat:
    def Time_Get(datetimes=False):
        '''
        返回时间字符串
        '''
        if not datetimes:
            datetimes=datetime.now()
        time_str = datetime.strftime(datetimes,'%m-%d %H:%M:%S')
        return time_str

    def Format_Message(CreateAt,Username,Message):
        '''
        格式化信息
        '''
        return CreateAt+' '+Username+' 说: '+Message

    def Format_Message_From_Datetime(CreateAt,Username,Message):
        '''
        格式化信息
        '''
        CreateAt = datetime.strftime(CreateAt,'%m-%d %H:%M:%S')
        return CreateAt+' '+Username+' 说: '+Message
    
    def Get_New_Five_Message(ClassID):
        '''
        从云端获取信息后格式化
        :Return: 格式化后的5条新信息和一条最新信息
        '''
        Messages_list,Usernames_list,CreatAt_list = Class_Chat.get_message(ClassID)
        NewMessage_str = ''
        for num in range(len(Messages_list)):
            NewMessage_str += Class_Chat.Format_Message(Class_Chat.Time_Get(CreatAt_list[num]),Usernames_list[num],Messages_list[num]) + '\n'
        if len(Messages_list) >= 1:
            LastestMessage_str = Class_Chat.Format_Message(Class_Chat.Time_Get(CreatAt_list[-1]),Usernames_list[-1],Messages_list[-1])
        else:
            LastestMessage_str = ''
        return NewMessage_str,LastestMessage_str

    # 获取云端信息
    def get_message(ClassID) -> list:
        '''
        获取到最新的前五条信息
        :param ClassID: 班级ID
        :return 返回最新的前五条信息,顺序为Message,Username,CreatedAt
        '''
        # 绑定到MailBox类
        class_obj = leancloud.Object.extend('MailBox')
        # 查询服务
        class_obj_query = class_obj.query
        # 查询该班级ID的信息
        class_obj_query.equal_to('Class_ID',ClassID)
        # 获取信息
        class_obj_query_result = class_obj_query.find()
        # 返回信息
        # 检查是否有信息
        if class_obj_query_result == []:
            return [],[],[]
        else:
            Messages_list,Usernames_list,CreatAt_list = [],[],[]
            for i in class_obj_query_result:
                Messages_list.append(i.get('Message'))
                Usernames_list.append(i.get('Username'))
                CreatAt_list.append(i.get('createdAt'))
            return Messages_list,Usernames_list,CreatAt_list

    #发送信息至云端
    def send_message(message):
        '''
        返回一个时间字符串以校准时间
        '''
        ClassID = Get_Class_Account()
        Username = read_key(Show_Status=True)
        # 绑定到MailBox类
        class_obj = leancloud.Object.extend('MailBox')
        class_obj = class_obj()
        # 发送信息,包括班级ID和用户名
        class_obj.set('Message',message)
        class_obj.set('Class_ID',ClassID)
        class_obj.set('Username',Username)
        class_obj.save()
        return datetime.strftime(class_obj.get('createdAt'),'%m-%d %H:%M:%S')

    # 实时获取云端信息
    def get_realtime_message(ClassID,OldMessage) -> str:
        '''
        获取到最新的一条信息
        :param ClassID: 班级ID
        :return 返回最新的一条信息,顺序为Message,Username,createdAt
        '''
        # 绑定到MailBox类
        class_obj = leancloud.Object.extend('MailBox')
        # 查询服务
        class_obj_query = class_obj.query
        # 查询该班级ID的信息
        class_obj_query.equal_to('Class_ID',ClassID)
        # 获取信息
        class_obj_query_result = class_obj_query.find()
        if class_obj_query_result == []:
            return ''
        else:
            Formated_Message = Class_Chat.Format_Message_From_Datetime(class_obj_query_result[-1].get('createdAt'),class_obj_query_result[-1].get('Username'),class_obj_query_result[-1].get('Message'))
            if Formated_Message != OldMessage:
                return Formated_Message
            else:
                return ''

    def main():
        '''
        聊天主函数
        '''
        ClassID = Get_Class_Account()
        Username = read_key()[0]
        Class_list_services = leancloud.Object.extend('Class_list') #定位到Class_list类
        Class_list_service = Class_list_services.query #查询服务
        Class_ID_Status = Class_list_service.equal_to('Class_ID',ClassID).find()
        if len(Class_ID_Status) == 0:
            sg.Popup('该账号尚未绑定任何班级!',font=('微软雅黑 10'))
            return None
        NewMessage_str,Old_Message = Class_Chat.Get_New_Five_Message(ClassID)
        layout =[
            [sg.Text('消息框')],
            [sg.Multiline(size=(80,20),key='_OUTPUT_',default_text=NewMessage_str,disabled=True,autoscroll=True,text_color='blue')],
            [sg.Text('发送新消息:')],
            [sg.Input(size=(75,5),key='_INPUT_'),sg.Button('发送')],
        ]
        window = sg.Window('消息框',layout,font=('微软雅黑 10'),size=(700,500),return_keyboard_events=True)
        while True:
            event,value = window.Read(timeout=1500)
            if event == sg.WIN_CLOSED:
                window.Close()
                return None
            elif event in ('\r','发送'):
                Message = value['_INPUT_']
                Message_Time = Class_Chat.send_message(Message)
                Old_Message = Class_Chat.Format_Message(Message_Time,Username,Message)
                window.Element('_OUTPUT_').Update(Old_Message+'\n',text_color_for_value='black',append=True)
                window.Element('_INPUT_').Update('')
            elif event == '__TIMEOUT__':
                print('Updating Message...')
                Realtime_message = Class_Chat.get_realtime_message(ClassID,Old_Message)
                if Realtime_message != '':
                    Old_Message = Realtime_message
                    window.Element('_OUTPUT_').Update(Realtime_message+'\n',text_color_for_value='red',append=True)

if __name__ == '__main__':
    from tool import Run_check
    from Setting import GetTheme
    Run_check()
    sg.set_options(font=('微软雅黑 10'),icon=('ico/LOGO.ico'))
    sg.theme(GetTheme()[0])
    Class_Chat.main()