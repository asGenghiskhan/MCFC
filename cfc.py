import nbtlib
from nbtlib import *
import gzip
import os
import io
import easygui


def wd(a):
    global World, Worlds
    try:
        World = easygui.fileopenbox('', 'classic文件转换器', a)
        Worlds = []
        Worlds.append(World.replace('\\', '/'))
        print(f'目标文件路径：{Worlds[0]}')
    except:
        exit()

# 选择存档类型
c = easygui.choicebox("请选择你的存档类型", "classic文件转换器", [
                      '客户端(.mine)', '服务器(server_level.dat)'])
if c == '客户端(.mine)':
    wd('*.mine')
else:
    wd('*.dat')
    aa = ''.join(Worlds).split('/')
    if not aa[-1] == 'server_level.dat':
        easygui.msgbox(f'你选的目标文件{Worlds[0]}不是classic服务器存档', 'classic文件转换器')
        exit()

# 读取世界文件
file = open(Worlds[0], 'rb').read()

# 解码level并判断世界大小
print('解码level中...')
if c == '客户端(.mine)':
    try:
        a = 128
        b = 7603
        Classic_file = gzip.decompress(file)[b:b+a*a*64]
        Blocks = []
        for byte in Classic_file:
            Blocks.append(Byte(byte))
    except:
        try:
            a = 256
            b = 20630
            Classic_file = gzip.decompress(file)[b:b+a*a*64]
            Blocks = []
            for byte in Classic_file:
                Blocks.append(Byte(byte))
        except:
            a = 512
            b = 72883
            Classic_file = gzip.decompress(file)[b:b+a*a*64]
            Blocks = []
            for byte in Classic_file:
                Blocks.append(Byte(byte))
else:
    a = 256
    b = 18385
    Classic_file = gzip.decompress(file)[b:b+a*a*64]
    Blocks = []
    for byte in Classic_file:
        Blocks.append(Byte(byte))


# 创建*.mclevel

print('创建索引级文件中...')

new_file = File({
    'MinecraftLevel': Compound({
        'Environment': Compound({
            'CloudColor': Int(16777215),
            'CloudHeight': Short(66),
            'FogColor': Int(16777215),
            'SkyBrightness': Byte(100),
            'SkyColor': Int(10079487),
            'SurroundingGroundHeight': Short(23),
            'SurroundingGroundType': Byte(2),
            'SurroundingWaterHeight': Short(32),
            'SurroundingWaterType': Byte(8),
        }),
        'Map': Compound({
            'Spawn': List[Short]([Short(a/2), Short(36), Short(a/2)]),
            'Height': Short(64),
            'Length': Short(a),
            'Width': Short(a),
            'Blocks': ByteArray(Blocks),
            'Data': ByteArray([Byte(15)] * a * a * 64)
        })
    })
})

while True:  # 创建文件
    worldname = easygui.enterbox('请输入文件名称', 'classic文件转换器', 'world')
    fileb = []
    folder = easygui.diropenbox('请选择文件保存路径', 'classic文件转换器')
    if folder == None or worldname == None:
        easygui.msgbox('请选择正确的文件保存路径或正确的文件名称', 'classic文件转换器')
    else:
        fileb.append(folder.replace('\\', '/'))
        a = fileb[0] + '/' + worldname
        new_file.save('{}.mclevel'.format(a), gzipped=True)
        easygui.msgbox(f'已将世界{Worlds[0]}转换为indev保存格式', 'classic文件转换器')
        break
