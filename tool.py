import PySimpleGUI as sg
import asyncio

def check_time(t1,t2,t3,t4,t5,t6,t7,t8,t9,t10) -> bool|tuple:
    '''
    将时间整合并检查导入时间是否合法
    '''
    from datetime import datetime
    try:
        stime='{}-{}-{} {}:{}'.format(t1,t2,t3,t4,t5)
        etime='{}-{}-{} {}:{}'.format(t6,t7,t8,t9,t10)
        st=datetime.strptime(stime,'%Y-%m-%d %H:%M')
        et=datetime.strptime(etime,'%Y-%m-%d %H:%M')
    except:
        return False
    if st>=et:
        return False
    else:
        return stime,etime

def repair_num(num):
    '''
    自动将一位数字转化为2位数字
    '''
    if len(str(num))==1:
        return '0'+str(num)
    else:
        return str(num)

def split_time(times):
    '''
    自动将时间字符串拆分为多个变量
    '''
    st=times.split('~')[0]
    et=times.split('~')[1]
    st_d=st.split('-')
    st_m=st.split(':')
    et_d=et.split('-')
    et_m=et.split(':')
    sty=st_d[0]
    stM=st_d[1]
    std=st_d[2].split(' ')[0]
    sth=st_m[0].split(' ')[1]
    stm=st_m[1]
    ety=et_d[0]
    etM=et_d[1]
    etd=et_d[2].split(' ')[0]
    eth=et_m[0].split(' ')[1]
    etm=et_m[1]
    return sty,stM,std,sth,stm,ety,etM,etd,eth,etm

def count_time(stime,etime):
    """
    计算两个时间之间的间隔
    :param stime: 开始时间
    :param etime: 结束时间
    :return: 间隔天数
    """
    if stime in ('无',None):
        return 0
    from datetime import datetime
    st=datetime.strptime(stime,'%Y-%m-%d %H:%M')
    et=datetime.strptime(etime,'%Y-%m-%d %H:%M')
    return round(((et-st).days),2)

def count_list(lists) -> float:
    '''
    自动求列表中的所有元素的总和
    '''
    a=0
    for b in lists:
        a+=float(b)
    return a

def Early_time_list(Time_list:list) -> str:
    '''
    从给定的时间列表中找出最早时间
    '''
    for num in range(len(Time_list)):
        Time_list[num] = Time_list[num].replace('-','')[:8]
    return min(Time_list)

def list_to_str(List:list) -> str:
    '''
    列表转字符串
    '''
    text=','
    return text.join(List)
    
def default_sen(mode:str) -> None:
    '''
    默认句子库, 用于在句子文件丢失时创建临时文件以供使用
    '''
    if mode == 'learn_sen':
        learn_sen=['读书在于造成完全的人格。——培根\n',
        '登高而招，臂非加长也，而见者远；顺风而呼，声非加疾也，而闻者彰。——《荀子·劝学》\n',
        '知识永远战胜愚昧\n',
        '人生最大的喜悦是每个人都说你做不到 ，你却完成它了!\n',
        '一本新书象一艘船，带领我们从狭隘的地方，驰向无限广阔的生活的海洋。——凯勒\n',
        '只要功夫深，铁杵 磨成绣花针。\n',
        '莫等闲，白了少年头，空悲切。 ——岳飞\n',
        '不奋苦而求速效，只落得少日浮夸，老来窘隘而已。─郑板桥\n',
        '知识无底，学海无涯\n',
        '我们的生命，就是以不断出发的姿势得到重生。\n',
        '少而好学如日出之阳\n']
        with open('data/learn_sen.txt','w',encoding='utf-8') as f:
            f.writelines(learn_sen)
    elif mode == 'hitokoto':
        hitokoto=[
        '我站在路口，哈出的气可以把那些六角形的雪融化。 By 佚名\n',
        '金风玉露一相逢，便胜却人间无数。 By 秦观\n',
        '今人不见古时月，今月曾经照古人。 By 李白\n',
        '莫愁前路无知己，天下谁人不识君。 By 高适\n',
        '但愿世间人无病，何愁架上药生尘。 By 清朝对联\n',
        '我们一直在离别中，比如和爱的人，和伤害，甚至和时光。By 萤火虫之墓\n',
        '或许此刻需要“推力”来成长。By 小世\n',
        '愿时光能缓，愿故人不散！ —— By 我们仍未知道那天所看见的花的名字\n',
        '你制定的计划是.txt还是.exe? —— By 网络\n',
        '用我一生，换你十年天真无邪。By 盗墓笔记\n']
        with open('data/hitokoto.txt','w',encoding='utf-8') as f:
            f.writelines(hitokoto)

class progress():
    '''
    进度条服务
    '''
    def __init__(self) -> None: # 初始化类
        pass
    def new(self):
        '''
        新建进度条
        '''
        import PySimpleGUI as sg
        layout = [[sg.Text('操作执行进度',font=('微软雅黑 12'))],
                [sg.ProgressBar(100, orientation='h', size=(20, 20), key='progressbar')],
                [sg.Text('此操作需要一定时间,感谢您的耐心等待...',font=('微软雅黑 12'))]]
        window = sg.Window('操作执行进度', layout)
        self.window = window
        self.progress_bar = self.window['progressbar']
        event, values = self.window.read(timeout=10)
        i=0
        self.progress_bar.UpdateBar(i)
    def add(self,value):
        '''
        更改进度条值
        '''
        self.progress_bar.UpdateBar(value)
    def close(self):
        '''
        关闭进度条
        '''
        self.window.Close()


def open_file_tip():
    '''
    用于在用户打开文件时提供提示
    '''
    layout = [
        [sg.Text('您的文件将在稍后开启,\n只有关闭新打开的窗口后,您才可以继续操作Study To Do')]
    ]
    Twindow = sg.Window('提示',layout=layout,icon='ico/LOGO.ico',font=('微软雅黑 10'))
    Twindow.Read(timeout=100)
    return Twindow

def plan_folder_check():
    '''
    检查plan目录下的所有任务文件是否正常
    '''
    import os
    from plan_manager import get_plan_info
    os.chdir(os.getenv('APPDATA')+'\Study to do')
    def remove_error_file():
        '''
        移除错误文件
        '''
        listdir=os.listdir('plan')
        for index_num in range(len(listdir)):
            try:
                print('[Info] Geting info from: ',listdir[index_num])
                get_plan_info(index_num,'status')
            except:
                if get_plan_info(num=None,mode='status',Path=os.listdir('plan')[index_num])==False:
                    print('[Warning] A File is error. Remove: ',os.listdir('plan')[index_num])
                    os.remove('plan/'+os.listdir('plan')[index_num])
                return False
        return True
    while True:
        status=remove_error_file()
        if status:
            break
    return None

def Run_check():
    '''
    启动检查
    '''
    #程序数据文件夹检查
    import os,json
    print('[Info] Start Run_check...')
    # if os.path.isdir('ico')==True and os.path.isdir(os.getenv('APPDATA')+'\Study to do\ico')==False:
    #     print('You are running by code')
    #     import shutil
    #     shutil.copytree('ico',os.getenv('APPDATA')+'\Study to do\ico')
    os.chdir(os.getenv('APPDATA'))
    if not os.path.isdir('Study to do'):
        os.mkdir('Study to do')
    os.chdir('Study to do')
    #plan文件夹检查
    if os.path.isdir('plan')==False:
        os.mkdir('plan')
    #data文件夹检查
    if os.path.isdir('data')==False:
        os.mkdir('data')
    #ico文件夹检查
    if os.path.isdir('ico')==False:
        sg.Popup('依赖文件丢失,请重新安装Study To Do')
        os._exit(0)
    #设置文件检查
    if os.path.isfile('data/setting.json')==False:
        from datetime import datetime
        with open('data/setting.json','w',encoding='utf-8') as f:
            setting={'showsen':'学习技巧','showplan':'全部','size':'500x500','backstage_status':'关闭','DarkMode':'关闭'}
            f.write(json.dumps(setting, sort_keys=True, indent=4, separators=(',', ': ')))
    try:
        from Setting import read_setting
        read_setting()
    except:
        from datetime import datetime
        with open('data/setting.json','w',encoding='utf-8') as f:
            setting={'showsen':'学习技巧','showplan':'全部','size':'500x500','backstage_status':'关闭','DarkMode':'关闭'}
            f.write(json.dumps(setting, sort_keys=True, indent=4, separators=(',', ': ')))
    #依赖文件检查(learn_sen.txt)
    if os.path.isfile('data/learn_sen.txt')==False:
        print('[Warning] learn_sen.txt fail')
        default_sen('learn_sen')
    #依赖文件检查(hitokoto.txt)
    if os.path.isfile('data/hitokoto.txt')==False:
        print('[Warning] hitokoto.txt fail')
        default_sen('hitokoto')
    #检查任务文件夹是否出错
    plan_folder_check()
    print('[Info] Run_check pass')

class ChatWithGPT():
    '''
    Chat with GPT
    '''
    def __init__(self):
        from account import read_key
        self.username = read_key(Show_Status=True) or '你'
        self.conversation_list = []
        self.max_retries = 3

    def update_chatwindow(self,text,speecher):
        self.window.Element('_OUTPUT_').Update(speecher+': '+text+'\n',text_color_for_value='black',append=True)
        self.window.refresh()

    async def send_and_receive_message(self,message, retries=0):
        question = message
        try:
            result = await self.chatbot.ask(prompt=question)
        except:
            if retries < self.max_retries:
                self.update_chatwindow('连接Microsoft(Sydney)服务器失败，正在进行第%s次尝试...' % (retries+1),speecher='系统')
                return await self.send_and_receive_message(message, retries=retries+1)
            else:
                self.update_chatwindow('连接Microsoft(Sydney)服务器失败,请检查您的网络连接',speecher='系统')
                return False
        return result["item"]["messages"][1]["adaptiveCards"][0]["body"][0]["text"]

    def getcookie(self):
        self.update_chatwindow('获取Cookie....',speecher='系统')
        import leancloud
        leancloud.init("OzN2cISaG1cUDK9wLAw2lB4F-gzGzoHsz", "ex4DGUuGw9yQAVoRfwUpbU2p")
        cookie = leancloud.Object.extend('APIKey').query.find()[0].get('APIKey')
        with open('data/cookie.json','w') as f:
            f.write(cookie)
        return None
    
    def initGPT(self):
        from EdgeGPT import Chatbot,create_session
        self.getcookie()
        self.chatbot = Chatbot(cookiePath='data/cookie.json')
        self.session = create_session()
        self.update_chatwindow('连接Microsoft(Sydney)服务器',speecher='系统')
        answer = asyncio.run(self.send_and_receive_message("从现在开始,我可能会问你有关高中学习上的问题,如果您清楚,请给我一个问候"))
        if not answer:
            return False
        self.update_chatwindow('成功加载对话,进入聊天...',speecher='系统')
        self.update_chatwindow(answer,speecher='Sydney')
        return True

    def beforeuse_windows(self):
        layout = [
            [sg.Text('使用前提示:',font=('微软雅黑 15'))],
            [sg.Text('1. 该应用基于Microsoft未公布的api实现,但由于Microsoft的服务器问题,在国内可能无法访问或者比较慢,请过段时间再试',font=('微软雅黑 10'))],
            [sg.Text('2. 应用使用期间无响应是正常现象,请不要关闭窗口',font=('微软雅黑 10'))],
            [sg.Text('3. 该应用使用Newbing(GPT 3.5)模型,因此效果可能有些差,请不要介意',font=('微软雅黑 10'))],
            [sg.Button('继续',font=('微软雅黑 10'))]
        ]
        window = sg.Window('使用前提示',layout,font=('微软雅黑 10'))
        event,value = window.Read()
        window.close()

    def main(self):
        # menu = ['操作菜单',['刷新对话','重置对话']]
        self.beforeuse_windows()
        layout =[
            # [sg.Menu(menu)],
            [sg.Text('消息框')],
            [sg.Multiline(size=(80,20),key='_OUTPUT_',default_text='',disabled=True,autoscroll=True,text_color='blue')],
            [sg.Text('发送新消息:')],
            [sg.Input(size=(75,5),key='_INPUT_'),sg.Button('发送')],
        ]
        self.window = sg.Window('消息框',layout,font=('微软雅黑 10'),size=(700,500),return_keyboard_events=True)
        event,value = self.window.Read(timeout=1000)
        try:
            Internet_coonect = self.initGPT()
        except:
            Internet_coonect = False
            self.update_chatwindow('连接失败，这可能是由于Microsoft服务器设置的防火墙导致的。',speecher='系统')
        while True:
            event,value = self.window.Read(timeout=1500)
            if event == sg.WIN_CLOSED:
                self.window.Close()
                return None
            elif event in ('\r','发送') and Internet_coonect:
                Message = value['_INPUT_']
                self.update_chatwindow(Message,speecher=self.username)
                Answer = asyncio.run(self.send_and_receive_message(Message))
                if not Answer:
                    Internet_coonect = False
                else:
                    self.update_chatwindow(Answer,speecher='Sydney')
                    self.window.Element('_INPUT_').Update('')

if __name__ == '__main__':
    Run_check()
    ChatWithGPT().main()
