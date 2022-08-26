from easygui import *
import os 
import sys
import webbrowser


while True:
    choices = ['运行文件转换器', '设置(indev文件转换器)','MCFC更新...', '关于', '退出']
    c = choicebox("请选择一个选项", "菜单", choices)
    if c == choices[0]:
        choices1 = ['classic文件转换器', 'indev文件转换器', '返回']
        c1 = choicebox("你要运行哪一个文件转换器？", "运行文件转换器", choices1)
        if c1 == choices1[0]:
            os.system('python classic文件转换器.py')
        elif c1 == choices1[1]:
            os.system('python indev文件转换器.py')
        else:
            pass
    elif c == choices[1]:
        os.system('python options.py')
    elif c == choices[2]:
        choices1 = ['获取MCFC版本','遇到了bug,点这里反馈','退出']
        c1 = choicebox("请选择一个选项", "菜单", choices1)
        if c1 == choices1[0]:
            sys.path.append("libs")
            webbrowser.open('https://github.com/asGenghiskhan/MCFC/releases')
        elif c1 == choices1[1]:
            sys.path.append("libs")
            webbrowser.open(
                'https://github.com/asGenghiskhan/MCFC/discussions/2')
        else:
            pass
    elif c == choices[3]:
        cs = ["确定", "顺便做一下启动文件(.bat/.cmd)", "？？？"]
        r = buttonbox('MCFC版本：1.0-release\nMade by As Genghis khan',
                      '关于MCFC', cs)
        if r == cs[1]:
            r1 = buttonbox('请选择文件类型',
                           '做启动文件', ["bat", "cmd"])
            f = os.getcwd()
            f1 = f.split('\\')
            f2 = open('{}.{}'.format(input('Save as:'),r1), 'w')
            f2.write(
                '@ echo off\n{}\ncd {}\nstart python menu.py\nexit'.format(f1[0], f))
            f2.close()
        if r  == cs[2]:
            if msgbox('？？？', 'MCFC-？？？', '？？？') == None:
                msgbox('恭喜你发现彩蛋','MCFC','OK!')
                sys.path.append("libs")
                webbrowser.open('http://classic.minecraft.net')
                print(webbrowser.get())
    else:
        break
