from plan_manager import *
from Setting import read_setting,GetTheme
from requests.exceptions import ConnectionError
from datetime import datetime
import PySimpleGUI as sg
import random,time,webbrowser

ver='3.4.0 - Chat with ChatGPT'

def Error_Message():
    '''
    错误报告
    '''
    import traceback,sys
    exc_type, exc_value, exc_traceback = sys.exc_info()
    layout = [
        [sg.Text('哦不!!!',font = ('微软雅黑 15'))],
        [sg.Text('我们似乎遇到了些问题, 导致程序被迫停止运行')],
        [sg.Text('失败的信息: '+str(exc_value))],
        [sg.Text('详细报错信息:')],
        [sg.Multiline(traceback.format_exc(),background_color=sg.theme_background_color(),size=(50,7))],
        [sg.Text('你可以选择:')],
        [sg.Text('· 重启应用程序')],
        [sg.Text('· 通过邮箱发送反馈',text_color='blue',enable_events=True,key='Feedback')],
        [sg.Text('· 重置数据文件夹',text_color='blue',enable_events=True,key='ReStore')]
    ]
    window = sg.Window('程序错误',layout,font=('微软雅黑 10'),resizable=True,icon='ico/LOGO.ico')
    event,value = window.Read()
    while True:
        if event == sg.WIN_CLOSED:
            window.Close()
            return None
        if event == 'ReStore':
            layout =[
                [sg.Text('注意:',font=('微软雅黑 12'))],
                [sg.Text('此选项将会清空任何已完成/进行中的任务,且无法恢复,请问要继续吗?')],
                [sg.Button('确定'),sg.Push(),sg.Button('取消')]
                ]
            windows = sg.Window('警告',layout=layout, font=('微软雅黑 10'))
            event,value = windows.Read()
            windows.Close()
            if event=='确定':
                for file in os.listdir('plan'):
                    os.remove('plan/'+file)
                for file in ['key.json','setting.json']:
                    os.remove('data/'+file)
            if event == 'Feedback':
                import subprocess
                subprocess.getstatusoutput('mailto:master@muspace.top')
        event,value = window.Read()
        

def choice_sen(showsen):
    if showsen=='学习技巧':
        with open('data/learn_sen.txt',encoding='utf-8') as l:
            show_sen=random.choice(l.readlines()).split('\n')[0]
    elif showsen=='一言(本地)':
        try:
            with open('data/hitokoto.txt',encoding='utf-8') as l:
                show_sen=random.choice(l.readlines()).split('\n')[0]
        except:
            with open('data/learn_sen.txt',encoding='utf-8') as l:
                show_sen=random.choice(l.readlines())                
    else:
        Now_time=int(time.strftime("%H", time.localtime()))
        if Now_time<12 and Now_time>=6:
            show_sen='早上好~今天也要加油哦~'
        elif Now_time<14 and Now_time>=12:
            show_sen='中午好~一顿充实的午饭和充实的午睡可以让下午工作动力增加哦'
        elif Now_time<18 and Now_time>=14:
            show_sen='下午好, 好好享受下午的时光吧~'
        elif Now_time<22 and Now_time>=18:
            show_sen='晚上好, 工作的同时也要要早点睡哦~'
        else:
            show_sen='深夜了, 要注意保护眼睛哦~'
    return show_sen

def note(et:str) -> str:
    '''
    给部分任务添加备注
    '''
    etd = datetime.strptime(et,'%Y-%m-%d %H:%M')
    ntd = datetime.now()
    text = '      '
    if etd<ntd:
        text+='已超时·'
    else:
        difference = round((etd - ntd).total_seconds()/60)
        if difference>=1000:
            difference = round(difference/1440)
            text+='剩余'+str(difference)+'天·'
        else:
            text+='剩余'+str(difference)+'分钟·'
    mon=et.split('-')[1]
    day=et.split('-')[2].split(' ')[0]
    text+='截止至:'+mon+'/'+day
    return text

def get_menu():
    '''
    根据登录状态获取菜单列表
    '''
    from account import read_key
    from Teacher import read_class_key
    if read_key():
        Username,_=read_key()
        menu=[
        ['!作业',['发布作业','导出',['导出成PDF文件','导出任务总清单为xlsx文件']]],
        ['分类',['全部','按科目-语文','按科目-数学','按科目-英语','按科目-物理','按科目-化学','按科目-生物','按科目-地理','按科目-历史','按科目-政治','按科目-体育','按分类-生活','按时间-当天','按时间-当周','按状态-已超时']],
        ['账户',['!已登录: '+Username,'任务备份','任务还原','登出']],
        ['班级',['创建班级','!查看班级','!班级聊天室']],
        ['帮助',['设置','帮助文档','与AI聊天(Beta)','检查更新','关于']]
        ]
        if read_class_key():
            menu[0][0]='作业'
            menu[3][1][0]='!创建班级'
            menu[3][1][1]='查看班级'
            menu[3][1][2]='班级聊天室'
    else:
        menu=[
        ['!作业',['发布作业','导出',['导出成PDF文件','导出任务总清单为xlsx文件']]],
        ['分类',['全部','按科目-语文','按科目-数学','按科目-英语','按科目-物理','按科目-化学','按科目-生物','按科目-地理','按科目-历史','按科目-政治','按科目-体育','按分类-生活','按时间-当天','按时间-当周','按状态-已超时']],
        ['账户',['登录(注册)','!任务备份','!任务还原','!登出']],
        ['!班级',['创建班级','查看班级','班级聊天室']],
        ['帮助',['设置','帮助文档','与AI聊天(Beta)','检查更新','关于']]
        ]
    return menu

def Button_image(path=None,key=None):
    return sg.Button(tooltip=key,button_color=(sg.theme_background_color(), sg.theme_background_color()),border_width=0,image_filename=path,key=key)

def main():
    from tool import Run_check
    Run_check()
    sg.set_options(font=('微软雅黑 10'),icon=('ico/LOGO.ico'))
    sg.theme(GetTheme()[0])
    showsen,showplan,size,DarkMode=read_setting()
    menu=get_menu()
    layout=[
        [sg.Menu(menu,font=('微软雅黑 8'),background_color=GetTheme()[1])],
        [sg.Text('所有作业',font=('微软雅黑 15'))],
        [sg.Text(choice_sen(showsen),font=('微软雅黑 8'))]
        ]
    No_num=0
    try:
        if showplan=='全部':
            txtname_list=read_plan_list() #传入计划列表
        else:
            txtname_list=read_plan_with_setting(showplan) #传入计划列表
            layout[1]=[sg.Text('所有作业({})'.format(showplan.split('-')[1]),font=('微软雅黑 15'))]
        if txtname_list==[]:
            layout.append([sg.Image(filename='ico/empty-box.png')])
        else:
            show_plan_num=0
            a=0
            print('txtname_list -> ',txtname_list)
            for num in txtname_list:
                plan_name=num
                if get_plan_info(plan_name,'status')!='已结束':
                    st,et=get_plan_info(plan_name,'atime')
                    text=get_plan_info(plan_name,'sub')+': '+get_plan_info(plan_name,'text')
                    if et!=None:
                        linelayout=[]
                        if check_plan_time(plan_name)==True:
                            #超时任务
                            linelayout.append([sg.Text(str(No_num+1)+'. '+text,font=('微软雅黑 12'),text_color='red'),sg.Push(),
                            sg.Button(tooltip='查看',button_color=(sg.theme_background_color(), sg.theme_background_color()),border_width=0,image_filename='ico/menu.png',key='c'+str(num))])
                            linelayout.append([sg.Text(note(et),font=('微软雅黑 8'),text_color='red')])
                        else:
                            #未超时任务
                            linelayout.append([sg.Text(str(No_num+1)+'. '+text,font=('微软雅黑 12')),sg.Push(),
                            sg.Button(tooltip='查看',button_color=(sg.theme_background_color(), sg.theme_background_color()),border_width=0,image_filename='ico/menu.png',key='c'+str(num))])
                            linelayout.append([sg.Text(note(et),font=('微软雅黑 8'))])
                        layout.append(linelayout)
                    else:
                        #未设定时间任务
                        layout.append([sg.Text(str(No_num+1)+'. '+text,font=('微软雅黑 12')),sg.Push(),
                        sg.Button(tooltip='查看',button_color=(sg.theme_background_color(), sg.theme_background_color()),border_width=0,image_filename='ico/menu.png',key='c'+str(num))])
                    No_num+=1
                    if No_num==10:
                        layout.append([sg.Text('目前仅显示10个作业',justification='center',font=('微软雅黑 12'))])
                        break
                    show_plan_num=1
                a+=1
            if show_plan_num==0:
                layout.append([sg.Image(filename='ico/empty-box.png')])
    except:
        layout.append([sg.Image(filename='ico/empty-box.png')])
        num=0
    if size=='500x500':
        if 0<=No_num<7:
            No_num=0
        else:
            No_num-=7
        window=sg.Window('学习计划通(教师端) '+ver,layout=layout,size=(500,500+(55*No_num)),icon='ico/LOGO.ico')
    else:
        x,y=size.split('x')
        size=(x,y)
        window=sg.Window('学习计划通(教师端) '+ver,layout=layout,size=size,icon='ico/LOGO.ico')
    while True:
        event,value=window.Read()
        print('主页面输出: ',event)
        if event==sg.WIN_CLOSED:
            break
        elif event=='发布作业':
            try:
                add_plan()
            except ConnectionError:
                sg.Popup('网络异常,请检查您的网络连接')
            window.Close()
            main()
            break
        elif event=='导出成PDF文件':
            from print import txt_to_PDF_GUI
            txt_to_PDF_GUI()
        elif event=='导出任务总清单为xlsx文件':
            from print import plan_log
            from tool import progress
            P = progress()
            P.new()
            plan_log.main()
            P.close()
        elif event=='登录(注册)':
            from account import log_in_gui
            log_in_gui()
            window.Close()
            main()
            break
        elif event=='任务备份':
            from account import send_plans
            try:
                send_plans()
            except ConnectionError:
                sg.Popup('网络异常,请检查您的网络连接')
        elif event=='任务还原':
            from account import get_plans
            try:
                get_plans()
            except ConnectionError:
                sg.Popup('网络异常,请检查您的网络连接')
            window.Close()
            main()
            break
        elif event=='登出':
            from account import log_out
            log_out()
            window.Close()
            main()
            break
        elif event=='创建班级':
            from Teacher import Creat_Class
            creat_class = Creat_Class()
            try:
                creat_class.GUI()
            except ConnectionError:
                sg.Popup('网络异常,请检查您的网络连接')
            window.Close()
            main()
            break
        elif event=='查看班级':
            from Teacher import View_Class
            try:
                View_Class()
            except ConnectionError:
                sg.Popup('网络异常,请检查您的网络连接')
        elif event=="班级聊天室":
            from Teacher import Class_Chat
            try:
                Class_Chat.main()
            except ConnectionError:
                sg.Popup('网络异常,请检查您的网络连接')
        elif event=='关于':
            layout=[
                [sg.Text('关于',font=('微软雅黑 20'))],
                [sg.Text('学习计划通(教师端)',font=('微软雅黑 15'))],
                [sg.Text('版本: '+ver)],
                [sg.Text('By Moemu')],
                [sg.Text('特别感谢: ',font=('微软雅黑 13'))],
                [sg.Text('Teacher Xie (提供部分改进建议和BUG反馈)')],
                [sg.Text('Student Zhu (手气不错,测试出几个漏洞)')],
                [sg.Text('A High-School Student (帮忙测试的学长)')],
                [sg.Text('版权声明:',font=('微软雅黑 13'))],
                [sg.Text('本程序是自由软件：\n你可以再分发之和/或依照由自由软件基金会发布的 GNU 通用公共许可证修改之，\n无论是版本 3 许可证，还是（按你的决定）任何以后版都可以。\n发布该程序是希望它能有用,但是并无保障;甚至连可销售和符合某个特定的目的都不保证。')],
                [sg.Text('请参看 GNU 通用公共许可证。'),sg.Text('了解详情',font=('微软雅黑 10'),text_color='blue',enable_events=True,key='licenses')],
                [sg.Text('开源地址: ',font=('微软雅黑 13')),sg.Text('https://github.com/WhitemuTeam/Study-To-Do',font=('微软雅黑 10'),text_color='blue',enable_events=True,key='github')],
                [sg.VPush()],
                [sg.Button(tooltip='返回',button_color=(sg.theme_background_color(), sg.theme_background_color()),border_width=0,image_filename='ico/back.png',key='返回')]
            ]
            windows=sg.Window('关于页面',layout=layout,size=(550,450),icon='ico/LOGO.ico',resizable=True)
            event,value=windows.Read()
            if event == 'licenses':
                webbrowser.open_new('https://github.com/WhitemuTeam/Study-To-Do/blob/main/License')
            elif event == 'github':
                webbrowser.open_new('https://github.com/WhitemuTeam/Study-To-Do')
            windows.Close()
        elif event=='帮助文档':
            webbrowser.open_new('https://doc.muspace.top/#/zh-cn/Program/Study-To-Do')
        elif event=='检查更新':
            Update_file=os.path.dirname(os.path.abspath(__file__))+r'\..\Update.exe'
            import subprocess
            subprocess.getstatusoutput(Update_file)
        elif event=='与AI聊天(Beta)':
            from tool import ChatWithGPT
            ChatWithGPT().main()
        elif event=='设置':
            import Setting
            status=Setting.main()
            if status==False:
                window.Close()
                main()
                break
        elif event.find('c')!=-1:
            #查看任务详情
            from Teacher import Get_UnFinishStus,Get_OtFinishStus
            tasknum=int(event.split('c')[1])
            layout=[
                [sg.Text('科目:',font=('微软雅黑 14'))],
                [sg.Text(get_plan_info(tasknum,'sub'))],
                [sg.Text('计划内容:',font=('微软雅黑 14'))],
                [sg.Text(get_plan_info(tasknum,'text'))]]
            if get_plan_info(tasknum,'atime')!=(None,None):
                atime=get_plan_info(tasknum,'atime')
                text='从 '+atime[0]+' 至 '+atime[1]
                layout.extend([
                    [sg.Text('时间限制:',font=('微软雅黑 14'))],
                    [sg.Text(text)]])
            if get_plan_info(tasknum,'des')!=None:
                layout.extend([
                    [sg.Text('计划描述:',font=('微软雅黑 14'))],
                    [sg.Text(get_plan_info(tasknum,'des'))]])
            try:
                UnFinishStu = Get_UnFinishStus(get_plan_info(tasknum,'HomeworkID'))
                OtFinishStu = Get_OtFinishStus(get_plan_info(tasknum,'HomeworkID'))
                if UnFinishStu == '(所有学生均已完成)':
                    Complete_plan(tasknum)
                layout.append([
                [sg.Text('超时完成:',font=('微软雅黑 14'))],
                [sg.Text(OtFinishStu)],
                [sg.Text('未完成学生: ',font=('微软雅黑 14'))],
                [sg.Text(UnFinishStu)]])
            except ConnectionError:
                sg.Popup('网络异常,请检查您的网络连接')
                return None
            # layout.extend([
            #     [sg.VPush()],
            #     [sg.Button_image('ico/edit.png','更改'),sg.Button_image('ico/done.png','标记为结束'),sg.Button_image(path='ico/delete.png',key='删除'),sg.Push(),sg.back()]
            # ])
            layout.extend([
                [sg.VPush()],
                [sg.Push(),sg.Button('退出')]
            ])
            detail_info=sg.Window('作业详情',layout,icon='ico/LOGO.ico',font=('微软雅黑 10'))
            event,value=detail_info.Read()
            detail_info.Close()
            print(event)
            # if not event in (sg.WIN_CLOSED,'返回',None):
            #     if event=='更改':
            #         change_plan(str(tasknum))
            #     elif event=='标记为结束':
            #         Complete_plan(tasknum)
            #     elif event=='删除':
            #         os.remove('plan/'+os.listdir('plan')[tasknum])
            #     window.Close()
            #     main()
            #     break
        elif showplan=='全部'or showplan.split('-')[1]:
            #分类选择
            if event=='全部'or event.find('-')!=-1:
                from Setting import save_setting
                save_setting(showplan=event)
                window.Close()
                main()
                break
        else:
            pass

if __name__=='__main__':
    try:
        main()
    except:
        Error_Message()
