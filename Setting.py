import json

def read_setting():
    '''
    读取设置
    '''
    with open('data/setting.json','r',encoding='utf-8') as f:
        setting=json.loads(f.read())
    showsen=setting['showsen']
    showplan=setting['showplan']
    size=setting['size']
    backstage_status=setting['backstage_status']
    DarkMode=setting['DarkMode']
    return showsen,showplan,size,backstage_status,DarkMode

def save_setting(showsen=None,showplan=None,size=None,backstage_status=None,DarkMode=None):
    '''
    保存设置
    '''
    Old_showsen,Old_showplan,Old_size,Old_backstage_status,Old_DarkMode=read_setting()
    if showsen==None:
        showsen=Old_showsen
    if showplan==None:
        showplan=Old_showplan
    if size==None:
        size=Old_size
    if backstage_status==None:
        backstage_status=Old_backstage_status
    if DarkMode==None:
        DarkMode=Old_DarkMode
    with open('data/setting.json','w',encoding='utf-8') as f:
        setting={'showsen':showsen,'showplan':showplan,'size':size,'backstage_status':backstage_status,'DarkMode':DarkMode}
        f.write(json.dumps(setting, sort_keys=True, indent=4, separators=(',', ': ')))
    return None

def GetTheme() -> str:
    '''
    返回主题字符串
    '''
    value = read_setting()
    if value[4] == '开启':
        return 'DarkBlue1','#242834'
    else:
        return 'Reddit','white'

def main():
    from tool import Easy_GUI as eg
    import PySimpleGUI as sg
    import os
    showsen,showplan,size,backstage_status,DarkMode=read_setting()
    layout=[
        [sg.Text('设置',font=('微软雅黑 15'))],
        [sg.Text('主页面左上角显示句子设置',font=('微软雅黑 10')),sg.Push(),sg.InputCombo(['学习技巧','一言(本地)','日常问候语'],showsen,size=(12,5),font=('微软雅黑 10'))],
        [sg.Text('启动时显示的计划分类',font=('微软雅黑 10')),sg.Push(),sg.InputCombo(['全部','按科目-语文','按科目-数学','按科目-英语','按科目-物理','按科目-化学','按科目-生物','按科目-地理','按科目-历史','按科目-政治','按科目-体育','按分类-生活','按时间-当天','按时间-当周','按状态-已超时'],showplan,size=(12,5),font=('微软雅黑 10'))],
        [sg.Text('主页面分辨率'),sg.Push(),eg.InputCombo(['500x500','600x600','650x650'],default_value=size)],
        [sg.Text('任务提醒(需要管理员权限和开机自启)'),sg.Push(),eg.InputCombo(['开启','关闭'],default_value=backstage_status,size=(5,10))],
        [sg.Text('深色模式'),sg.Push(),eg.InputCombo(['开启','关闭'],default_value=DarkMode,size=(5,10))],
        [sg.VPush()],
        [sg.Button('保存',font=('微软雅黑 10'))]
    ]
    swindow=sg.Window('设置界面',layout=layout,icon='ico/LOGO.ico',size=(500,250),font=('微软雅黑 10'))
    event,value=swindow.Read()
    if event==sg.WIN_CLOSED:
        return True
    Oldbackstage_status=backstage_status
    New_setting=value
    showsen=New_setting[0]
    showplan=New_setting[1]
    size=New_setting[2]
    backstage_status=New_setting[3]
    DarkMode=New_setting[4]
    if backstage_status=='开启':
        import win32api,win32con,os
        path=os.getenv('APPDATA')+r'\Study to do\data\bns.exe'
        try:
            key = win32api.RegOpenKey(win32con.HKEY_LOCAL_MACHINE,'SOFTWARE\Microsoft\Windows\CurrentVersion\Run',0, win32con.KEY_ALL_ACCESS)
            win32api.RegSetValueEx(key,'Study to do',0,win32con.REG_SZ,path) # 写值（key, '项名', ...）
        except:
            eg.Popup('保存设置失败,请用管理员模式打开本程序')
            backstage_status='关闭'
    if backstage_status!='开启' and backstage_status!=Oldbackstage_status:
        import win32api,win32con,os
        try:
            key = win32api.RegOpenKey(win32con.HKEY_LOCAL_MACHINE,'SOFTWARE\Microsoft\Windows\CurrentVersion\Run',0, win32con.KEY_ALL_ACCESS)
            win32api.RegSetValueEx(key,'Study to do',0,win32con.REG_SZ,'')
        except:
            eg.Popup('保存设置失败,请用管理员模式打开本程序')
            backstage_status='开启'
    if showplan!=None or showsen!=None or backstage_status!=None or size!=None:
        eg.Popup('保存设置成功!')
        save_setting(showsen,showplan,size,backstage_status,DarkMode)
    else:
        pass
    swindow.Close()
    return False