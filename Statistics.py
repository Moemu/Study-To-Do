'''
统计函数库
'''

def Creft_file():
    '''
    创建存放数据用Json文件
    '''
    import json
    text={
        '创建的任务数':0,
        '完成的任务数':0,
        '完成任务总用时':0,
        '完成语文的任务总数':0,
        '完成数学的任务总数':0,
        '完成英语的任务总数':0,
        '完成物理的任务总数':0,
        '完成历史的任务总数':0,
        '完成生物的任务总数':0,
        '完成地理的任务总数':0,
        '完成政治的任务总数':0,
        '完成化学的任务总数':0,
        '完成体育的任务总数':0,
    }
    with open('data/Statistics.json','w',encoding='utf-8') as f:
        f.write(json.dumps(text, sort_keys=True, indent=4, separators=(',', ': ')))

def Update_plan_data():
    '''
    更新统计数据
    '''
    from tool import count_time,count_list
    import json
    #获取各任务值列表
    sub_list=chart.get_data('B')
    stime_list=chart.get_data('D')
    etime_list=chart.get_data('E')
    status_list=chart.get_data('G')
    #初始化列表
    done_sub_list=[]
    done_ctime_list=[]
    #遍历任务列表
    for num in range(len(status_list)):
        status=status_list[num]
        if status=='已结束':
            done_sub_list.append(sub_list[num]) #统计任务完成数量
            done_ctime_list.append(count_time(stime_list[num],etime_list[num])) #统计任务完成时间
    atime=count_list(done_ctime_list)
    Creft_file() #创建存放数据用Json文件
    with open('data/Statistics.json','r') as f:
        data=json.loads(f.read()) #读取新建的JSON文件
    #写入统计数据
    data['创建的任务数']=len(sub_list)
    data['完成的任务数']=len(done_sub_list)
    data['完成任务总用时']=atime
    for sub in ['语文','数学','英语','物理','历史','化学','生物','地理','政治','体育']: #遍历科目
        time_list=[]
        for num in range(len(done_sub_list)): #遍历完成任务列表
            if done_sub_list[num]==sub:
                time_list.append(done_ctime_list[num])
        data['完成{}的任务总数'.format(sub)]=done_sub_list.count(sub)
    with open('data/Statistics.json','w') as f:
        f.write(json.dumps(data))
    return None

def Show_data():
    '''
    显示统计数据
    '''
    import PySimpleGUI as sg
    import json
    from tool import progress
    Progress = progress()
    Progress.new()
    Update_plan_data()
    Progress.add(60)
    with open('data/Statistics.json','r',encoding='utf-8') as f:
        data=json.loads(f.read())
        text='创建的任务数: '+str(data['创建的任务数'])+'\n'+'完成的任务数: '+str(data['完成的任务数'])
        for sub in ['语文','数学','英语','物理','历史','化学','生物','地理','政治','体育']:
            text+='\n'+'完成'+sub+'的任务总数'+': '+str(data['完成'+sub+'的任务总数'])
    Progress.add(90)
    layout=[
        [sg.Text('统计数据',font=('微软雅黑 15'))],
        [sg.Text(text,font=('微软雅黑 10'))],
        [sg.Push(),sg.Button("返回")]
    ]
    Progress.add(100)
    Progress.close()
    windows=sg.Window('统计数据',layout=layout,size=(350,330),icon='ico/LOGO.ico')
    windows.Read()
    windows.Close()

#chart类：绘制图表
class chart:
    def generate_data():
        from output import plan_log
        plan_log.main(GUI=False)
        return None

    def count_sub(sub_list):
        '''
        任务数量计数
        sub_list: 科目列表
        '''
        sub=['语文','数学','英语','物理','历史','化学','生物','地理','政治','体育','生活','其他']
        sub_num=[0,0,0,0,0,0,0,0,0,0,0,0]
        for asub in sub_list:
            for num in range(len(sub)):
                if asub==sub[num]:
                    sub_num[num]+=1
        return sub_num

    def count_time(sub_list,st_list,et_list):
        '''
        任务时间计数
        sub_list: 科目列表
        st_list/et_list: 开始与结束时间列表
        '''
        from datetime import datetime
        sub_lists=['语文','数学','英语','物理','历史','化学','生物','地理','政治','体育','生活','其他']
        sub_min=[0,0,0,0,0,0,0,0,0,0,0,0]
        for num in range(len(st_list)):
            st=st_list[num]
            et=et_list[num]
            sub=sub_list[num]
            if st!='无':
                et=datetime.strptime(et,"%Y-%m-%d %H:%M")
                st=datetime.strptime(st,"%Y-%m-%d %H:%M")
                ct=round((et-st).total_seconds()/3600,2)
                for num in range(len(sub_lists)):
                    if sub==sub_lists[num]:
                        sub_min[num]+=ct
        return sub_min

    def get_data(word:str) -> str:
        '''
        获取到excel文档数据
        word->str
        word:B -> 科目
        word:D,E -> 开始, 结束时间
        word:G -> 状态
        返回一个list
        '''
        from openpyxl import load_workbook
        chart.generate_data()
        sheet = load_workbook('data/Plan_log.xlsx').worksheets[0]
        col=[]
        for a in sheet[word]:
            col.append(a.value)
        del col[0]
        return col

    def polar(value,title,Progress):
        '''
        绘制雷达图
        '''
        import numpy as np
        import matplotlib.pyplot as plt
        plt.rcParams["font.sans-serif"]=["SimHei"]
        plt.rcParams["axes.unicode_minus"]=False
        plt.subplot(111,polar = True)
        sub=['语文','数学','英语','物理','历史','化学','生物','地理','政治','体育','生活','其他']
        dataLenth=len(sub)
        angles=np.linspace(0,2*np.pi,dataLenth,endpoint=False)
        labels = np.array(sub)
        value = np.array(value)
        plt.polar(angles,value,color='green',marker='o')
        plt.thetagrids(angles*180/np.pi,labels)
        plt.fill(angles,value,facecolor='green',alpha=0.8)
        plt.title(title)
        Progress.close()
        plt.show()
        plt.savefig('data/{}.jpg'.format(title))

    def polars(value1,value2,title,sub):
        '''
        绘制雷达图(双图像)
        '''
        import numpy as np
        import matplotlib.pyplot as plt
        plt.rcParams["font.sans-serif"]=["SimHei"]
        plt.rcParams["axes.unicode_minus"]=False
        plt.subplot(111,polar = True)
        dataLenth=len(sub)
        angles=np.linspace(0,2*np.pi,dataLenth,endpoint=False)
        labels = np.array(sub)
        value1 = np.array(value1)
        value2 = np.array(value2)
        ax = plt.subplot(111, polar=True)        
        ax.plot(angles, value1, color='r',marker='o')
        ax.plot(angles, value2, color='b',marker='o')
        ax.set_thetagrids(angles*180/np.pi,labels)
        plt.fill(angles,value1,facecolor='red',alpha=0.5)
        plt.fill(angles,value2,facecolor='blue',alpha=0.5)
        ax.set_title(title)
        plt.legend(labels=['任务数量比','年级排名比'],bbox_to_anchor=(1.2, 1.12))
        plt.savefig('data/{}.png'.format(title))

    def pie(value,title,Progress):
        '''
        绘制饼状图
        '''
        import numpy as np
        import matplotlib.pyplot as plt
        plt.rcParams["font.sans-serif"]=["SimHei"]
        plt.rcParams["axes.unicode_minus"]=False
        plt.subplot(1,1,1)
        sub=['语文','数学','英语','物理','历史','化学','生物','地理','政治','体育','生活','其他']
        labels = np.array(sub)
        value = np.array(value)
        plt.pie(value,labels=labels,autopct='%.0f%%',radius=1.0)
        plt.title(title)
        Progress.close()
        plt.show()
        plt.savefig('data/{}.jpg'.format(title))

    def main(mode):
        from tool import progress
        Progress = progress()
        Progress.new()
        sub_list=chart.get_data('B')
        Progress.add(50)
        if mode=='雷达图(任务完成数量占比)':
            chart.polar(value=chart.count_sub(sub_list),title='任务完成数量占比',Progress=Progress)
        else:
            chart.pie(value=chart.count_sub(sub_list),title='任务完成数量占比',Progress=Progress)


def summary():
    '''
    分析统计数据, 并提出反馈
    '''
    import json,os
    import PySimpleGUI as sg
    from tool import list_to_str,Early_time_list,progress
    from datetime import datetime
    #---检查数据文件---
    if not os.path.isfile('data/User_info.json'):
        layout = [
            [sg.Text('必要的信息收集',font=('微软雅黑 15'))],
            [sg.Text('若想进行对统计数据的查看,请务必补充一些必要的数据。')],
            [sg.Text('此数据通常包括: 您的各科考试成绩和您的选科')],
            [sg.Text('预计用时: 3分钟')],
            [sg.Text('您想继续吗?'),sg.Push(),sg.Button('继续')]
        ]
        window = sg.Window('数据收集提示',layout=layout,font=('微软雅黑 10'))
        event, value = window.Read()
        window.Close()
        if event==sg.WIN_CLOSED:
            return None
        layout = [
            [sg.Text('必要的信息收集(1/2)',font=('微软雅黑 12'))],
            [sg.Text('作为高中生,您目前的选科是?(若为未选科,请留空)')],
            [sg.Checkbox('物理',font=('微软雅黑 10')),sg.Checkbox('历史',font=('微软雅黑 10'))],
            [sg.Checkbox('化学',font=('微软雅黑 10')),sg.Checkbox('生物',font=('微软雅黑 10')),sg.Checkbox('地理',font=('微软雅黑 10')),sg.Checkbox('政治',font=('微软雅黑 10'))],
            [sg.Push(),sg.Button('下一步')]
        ]
        window = sg.Window('数据收集(1/2)',layout=layout,font=('微软雅黑 10'))
        event, value = window.Read()
        window.Close()
        if event==sg.WIN_CLOSED:
            return None
        All_sub=['物理','历史','化学','生物','地理','政治']
        Choose_sub=['语文','数学','英语']
        if value=={0: False, 1: False, 2: False, 3: False, 4: False, 5: False}:
            Choose_sub.extend(All_sub)
        else:
            for_times=0
            for index_num,sub in value.items():
                if sub==True:
                    Choose_sub.append(All_sub[index_num])
                    for_times+=1
            if for_times!=3:
                sg.Popup('请检查您的的选考科目是否等于3科')
                return None
        layout = [
            [sg.Text('必要的信息收集(2/2)',font=('微软雅黑 12'))],
            [sg.Text('拿出您的成绩单,让我们知道您的提升方向')]]
        for sub in Choose_sub:
            layout.append([sg.Text('科目: '+sub+'  级排名: '),sg.Input()])
        layout.append([sg.Push(),sg.Button('下一步')])
        window = sg.Window('数据收集(2/2)',layout=layout,font=('微软雅黑 10'))
        event,value = window.Read()
        window.Close()
        if event == sg.WIN_CLOSED:
            return None
        values = list(value.values())
        for point in values:
            if point =='':
                sg.Popup('缺失数据或数据格式有误,请重新填写数据')
                return None
            try:
                point=int(point)
                if point <= 0:
                    sg.Popup('级排名不能小于0,请重新填写数据')
                    return None
            except:
                sg.Popup('缺失数据或数据格式有误,请重新填写数据')
                return None
        for i in range(len(values)):
            values[i]=round((1000-int(values[i]))/1000,2) #转换百分比(前:xx%)
        # sum=count_list(values)
        # for i in range(len(values)):
        #     values[i]=round(values[i]/sum,2) #转换百分比(优势比较)
        data = {Choose_sub[0]:values[0],
                Choose_sub[1]:values[1],
                Choose_sub[2]:values[2],
                Choose_sub[3]:values[3],
                Choose_sub[4]:values[4],
                Choose_sub[5]:values[5]}
        print('[Info] Get score data -> ',data)
        with open('data/User_info.json','w') as f:
            f.write(json.dumps(data,sort_keys=True,indent=4,separators=(',', ': ')))
        sg.Popup('感谢!所有的数据已收集完毕,现在让我们开始统计分析')
    #---分界线---
    Progress = progress()
    Progress.new()
    print('[Info] Loading data...')
    Update_plan_data()
    Progress.add(30)
    print('[Info] Statistics.json is readying...')
    with open('data/User_info.json','r') as f:
        data = json.loads(f.read())
    Choose_sub = list(data.keys())
    sub_score = list(data.values())
    with open('data/Statistics.json','r') as f:
        data = json.loads(f.read())
    All_plan_stime = chart.get_data('D') #获取所有任务的开始时间
    if All_plan_stime == []:
        sg.Popup('分析失败,创建1个带有任务限制的任务再试试吧')
        Progress.close()
        return None
    Early_time = Early_time_list(All_plan_stime)
    Progress.add(40)
    frequency=[] #任务总数
    Total_time=[]
    for sub in Choose_sub:
        frequency.append(data['完成{}的任务总数'.format(sub)])
    all_Total_time=round(data['完成任务总用时'],2)
    all_frequency=data['完成的任务数']
    if all_frequency<3:
        sg.Popup('完成的任务太少,还是多完成一些任务再来吧')
        return None
    print('[Info] Choose_sub -> ',Choose_sub)
    print('[Info] sub_score -> ',sub_score)
    print('[Info] frequency ->',frequency)
    #初始化列表
    max_frequency_sub=[]
    max_frequency_value=[]
    max_sub_value=[]
    max_sub_score=[]
    #建立副本
    Choose_sub1 = Choose_sub.copy()
    Choose_sub3 = Choose_sub.copy()
    Progress.add(50)
    #对frequency列表进行排序
    for i in range(len(Choose_sub)):
        max_value = max(frequency) #获取frequency的最大值
        max_idx = frequency.index(max_value) #获取frequency最大值的索引
        max_frequency_sub.append(Choose_sub1[max_idx]) #最大值所在科目加入max_frequency_sub列表
        max_frequency_value.append(round(max_value/all_frequency,2)) #最大值转换为百分比加入max_frequency_value列表
        frequency.remove(frequency[max_idx]) #移除最大值
        Choose_sub1.remove(Choose_sub1[max_idx]) #移除最大值所在科目
    #对max_sub_score列表进行排序(按照由大到小顺序,生成max_sub_value列表)
    sub_score2 = sub_score.copy()
    Progress.add(60)
    #对sub_score进行排序
    for i in range(len(Choose_sub)):
        max_value = max(sub_score2) #获取sub_score最大值
        max_idx = sub_score2.index(max_value) #获取sub_score最大值所在索引
        max_sub_score.append(max_value) #将sub_score最大值加入max_sub_value列表
        max_sub_value.append(Choose_sub3[max_idx]) #将max_sub_score最大值所在科目加入max_sub_value列表
        Choose_sub3.remove(Choose_sub3[max_idx])
        sub_score2.remove(max_value)
    #对max_sub_score进行二次排序(按照max_frequency_sub中的科目顺序排序)
    temp_max_sub_score = max_sub_score.copy()
    for i in range(len(max_frequency_sub)):
        sub = max_frequency_sub[i]
        sub_idx = max_sub_value.index(sub)
        max_sub_score[i] = temp_max_sub_score[sub_idx]
    Progress.add(70)
    print('[Info] max_frequency_sub -> ',max_frequency_sub)
    print('[Info] max_frequency_value -> ',max_frequency_value)
    print('[Info] max_sub_score -> ',max_sub_score)
    print('[Info] max_sub_value -> ',max_sub_value)
    chart.polars(max_frequency_value,max_sub_score,'各学科所占时间之比',max_frequency_sub)
    Progress.add(80)
    count_time=str((datetime.now()-datetime.strptime(Early_time,'%Y%m%d')).days)
    #科目分类
    n = int(len(Choose_sub)/2)
    #获取成绩优秀但是用时较多的科目
    best_and_max_fre_sub=[]
    for i in range(n):
        best_sub = max_sub_value[i]
        if best_sub in max_frequency_sub[:n]:
            best_and_max_fre_sub.append(best_sub)
    print('best_and_max_fre_sub -> ',best_and_max_fre_sub)
    Progress.add(90)
    #获取成绩一般但是用时较少的科目
    bad_and_less_fre_sub=[]
    bad_subs = max_sub_value[n:]
    print('bad_subs -> ',bad_subs)
    for bad_sub in bad_subs:
        if bad_sub in max_frequency_sub[(n):]:
            bad_and_less_fre_sub.append(bad_sub)
    print('bad_and_less_fre_sub -> ',bad_and_less_fre_sub)
    text=('从{}年{}月{}日'.format(Early_time[:4],Early_time[4:6],Early_time[6:8])+'到现在的一共'+count_time+'天中,\n'+
        '您一共完成了'+str(all_frequency)+'个任务,其中完成有时间限制的任务一共消耗了'+str(all_Total_time)+'天,\n'+
        '其中:\n')
    if best_and_max_fre_sub!=[]:
        text+=(list_to_str(best_and_max_fre_sub)+'是你的优势科目,也是你花时间最多的科目之一,但回头想想是不是要多用点时间在'+list_to_str(bad_subs)+'这些弱势学科上呢?\n')
    if bad_and_less_fre_sub!=[]:
        text+=(list_to_str(bad_and_less_fre_sub)+'是你的弱势科目,但也是你花时间最少的科目之一,回头想想是不是要下点功夫时间在这些科目上呢?')
    if bad_and_less_fre_sub==[] and best_and_max_fre_sub==[]:
        text+=('你在各科的时间分布均匀,懂得弱势科目要多花点时间,这点要表扬一下,\n今后也要多花点时间在'+list_to_str(bad_subs)+'这些弱势学科上哦~')
    Progress.add(100)
    #生成GUI
    layout = [
        [sg.Text(text)],
        [sg.Text('以下是各科时间和成绩的比较雷达图,您可以结合着雷达图制定您的学习计划\n其中:"任务数量比"数据占比越大,所用时间越多; "年级排名比"数据占比越大,年级排名越靠前')],
        [sg.Image(r'data\各学科所占时间之比.png')],
        [sg.Text('注意:如果雷达图出现2层红色图层,请重启Study To Do')],
        [sg.Push(),sg.Button(tooltip='返回',button_color=(sg.theme_background_color(), sg.theme_background_color()),border_width=0,image_filename='ico/back.png',key='返回')]
    ]
    Progress.close()
    window = sg.Window('统计分析',layout=layout,font=('微软雅黑 10'))
    event,value = window.Read()
    window.Close()

if __name__=='__main__':
    from tool import Run_check
    Run_check()
    summary()