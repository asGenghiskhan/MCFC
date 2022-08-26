from easygui import *


def nb(msg1, title, x, n, msg2):
    a = enterbox(msg1, title, x)
    try:
        ls[n] = msg2 + str(int(a))
        f = open('config.yml', 'w')
        f.write('\n'.join(ls))
        f.close()
    except:
        msgbox('错误!', 'indev文件转换器设置', '确定')


while True:
    c1 = choicebox("请选择一个选项", '设置(indev文件转换器)', [
                       'indev方块id列表', 'indev文件转换器设置', '返回'])
    if c1 == 'indev方块id列表':
        textbox('以下列举了全部indev方块id', 'indev方块id列表',
                    open('blockid.ini').read())
    elif c1 == 'indev文件转换器设置':
        f = open('config.yml')
        ls = []
        for line in f:
                ls.append(line.replace("\n", ''))
        f.close()
        Dict = {}
        f = open('blockid.ini')
        for line in f:
            List = []
            List = line.replace('\n', '').split('—')
            Dict[List[0]] = List[1]
        f.close()
        cc = Dict[ls[7].split(': ')[-1]]
        ls1 = ['在 x 轴上偏移{}个区块'.format(ls[1].split(
            ': ')[-1]), '世界在y轴偏移{}'.format(ls[3].split(': ')[-1]), '在 z 轴上偏移{}个区块'.format(ls[5].split(': ')[-1]),
            '偏移填充方块ID-{}({})'.format(ls[7].split(': ')[-1],
                                         cc), '地形填充标签-{}'.format(ls[9].split(': ')[-1]),
            '随机种子-{}'.format(ls[11].split(': ')[-1]), '返回']
        c2 = choicebox("请选择一个选项", 'indev文件转换器设置', ls1)
        if c2 == ls1[0]:
            nb('默认情况下，世界仅放置在正/正象限中\n因此，如果您希望它在此轴上居中，请将该值设置为地图宽度的负半除以2（以区块为单位）',
                '在 x 轴上要偏移多少个区块', 0, 1, 'x_chunk_offset: ')
        elif c2 == ls1[1]:
            a1 = enterbox('必须小于或等于 64，具体取决于您的世界大小设置\n也必须是偶数',
                              '世界在y轴上会偏移多远', 32)
            try:
                a2 = int(a1)
                if (a2 % 2 == 0 and a2 <= 64):
                    ls[3] = 'y_offset: ' + str(a2)
                    f = open('config.yml', 'w')
                    f.write('\n'.join(ls))
                    f.close()
                else:
                    msgbox('错误!', 'indev文件转换器设置', '确定')
            except:
                msgbox('错误!', 'indev文件转换器设置', '确定')
        elif c2 == ls1[2]:
            nb('默认情况下，世界仅放置在正/正象限中\n因此，如果您希望它在此轴上居中，请将该值设置为地图宽度的负半除以2（以区块为单位）',
                '在 z 轴上要偏移多少个区块', 0, 5, 'z_chunk_offset: ')
        elif c2 == ls1[3]:
            a1 = enterbox('如果y_offset不是0，则使用区块的种类来填补空白\n此值为区块 ID\n常用值：0（空气）、1（石头）、7（基岩）',
                            '偏移填充方块ID', 0)
            try:
                if (int(a1) > -1 and int(a1) < 255):
                    ls[7] = 'offset_fill_block: ' + str(int(a1))
                    f = open('config.yml', 'w')
                    f.write('\n'.join(ls))
                    f.close()
                else:
                    msgbox('错误!', 'indev文件转换器设置', '确定')
            except:
                msgbox('错误!', 'indev文件转换器设置', '确定')
        elif c2 == ls1[4]:
            a1 = indexbox(
                '默认情况下，当转换世界时，地形会重新填充。如果您不希望发生这种情况，请将其设置为1\n必须为 0 或 1', '设置地形填充标签', ['0', '1'])
            if not a1 == None:
                ls[9] = 'terrain_populated: ' + str(a1)
                f = open('config.yml', 'w')
                f.write('\n'.join(ls))
                f.close()
            else:
                msgbox('错误!', 'indev文件转换器设置', '确定')
        elif c2 == ls1[5]:
            a1 = enterbox('为随机种子留空\n必须是数字','转换世界时使用的种子', '')
            try:
                ls[11] = 'offset_fill_block: ' + str(int(a1))
                f = open('config.yml', 'w')
                f.write('\n'.join(ls))
                f.close()
            except:
                if a1 == '':
                    ls[11] = 'random_seed: ' + str(a1)
                    f = open('config.yml', 'w')
                    f.write('\n'.join(ls))
                    f.close()
                else:
                    msgbox('错误!', 'indev文件转换器设置', '确定')
        else:
            pass
    else:
        break
