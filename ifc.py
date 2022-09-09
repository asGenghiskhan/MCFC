from nbtlib import *
from yaml import safe_load
import numpy as np
import os
import easygui

# 加载文件并返回级别字典
def load_indev(dir):

    nbt_file = load(dir)

    level_indev = {
        'About': nbt_file.root['About'],
        'Environment': nbt_file.root['Environment'],
        'Map': nbt_file.root['Map'],
        'Entities': nbt_file.root['Entities'],
        'TileEntities': nbt_file.root['TileEntities']
        }
        
    return(level_indev)


def convert_entities(level_indev, config):

    L = level_indev['Map']['Length']
    W = level_indev['Map']['Width']

    World_entity_chunks = [[] for i in range((L // 16) * (W // 16))]

    for Entity in level_indev['Entities']:
        if Entity['id'] != 'LocalPlayer':
            
            motion_new = []
            for i in Entity['Motion']:
                motion_new.append(Double(i))
                
            Entity['Motion'] = List[Double](motion_new)
            
            pos_new = []
            for i in Entity['Pos']:
                pos_new.append(Double(i))
                
            x = int(pos_new[0])
            z = int(pos_new[2])
            
            pos_new[0] += config['x_chunk_offset'] * 16
            pos_new[1] += config['y_offset'] + 1
            pos_new[2] += config['z_chunk_offset'] * 16
            
            Entity['Pos'] = List[Double](pos_new)
            
            try:
                Entity['TileX'] += config['x_chunk_offset'] * 16
                Entity['TileY'] += config['y_offset']
                Entity['TileZ'] += config['z_chunk_offset'] * 16
            except KeyError:
                pass
                
            try:
                Entity['xTile'] += config['x_chunk_offset'] * 16
                Entity['yTile'] += config['y_offset']
                Entity['zTile'] += config['z_chunk_offset'] * 16
            except KeyError:
                pass
            
            chunk = x // 16 * L // 16 + z // 16
            World_entity_chunks[chunk].append(Entity)
    
    return(World_entity_chunks)
    

def convert_tile_entities(level_indev, config):

    L = level_indev['Map']['Length']
    W = level_indev['Map']['Width']

    World_tile_entity_chunks = [[] for i in range((L // 16) * (W // 16))]
    
    for TileEntity in level_indev['TileEntities']:
    
        pos = int(TileEntity['Pos'])
        TileEntity['x'] = Int(pos % 1024 + config['x_chunk_offset'] * 16)
        TileEntity['y'] = Int((pos >> 10) % 1024 + config['y_offset'])
        TileEntity['z'] = Int((pos >> 20) % 1024 + config['z_chunk_offset'] * 16)
        TileEntity.pop('Pos')
        
        x = pos % 1024
        z = (pos >> 20) % 1024
        
        chunk = x // 16 * L // 16 + z // 16
        World_tile_entity_chunks[chunk].append(TileEntity)
        
    return(World_tile_entity_chunks)
    
    
def convert_block_IDs(level_indev, config):

    L = level_indev['Map']['Length']
    W = level_indev['Map']['Width']
    H = level_indev['Map']['Height']
    
    Block_data = level_indev['Map']['Blocks']
    
    World_blocks = np.zeros(L * W * 128, dtype=int)
    i = 0

    for z_chunk in range(0, W//16):
        for x_chunk in range(0, L//16):
            for z in range(z_chunk*16, z_chunk*16+16):
                for x in range(x_chunk*16, x_chunk*16+16):
                
                    for y in range(0, config['y_offset']):
                        World_blocks[i] = Byte(config['offset_fill_block'])
                        i += 1

                    for y in range(0, H):
                        # (y * L + x) * W + z
                        World_blocks[i] = Block_data[(y * L + x) * W + z]
                        i += 1
                        
                    i += 128 - H - config['y_offset']
                    
    World_block_chunks = np.split(World_blocks, L//16 * W//16)
    
    return(World_block_chunks)
    
    
def convert_block_DVs(level_indev, config):

    L = level_indev['Map']['Length']
    W = level_indev['Map']['Width']
    H = level_indev['Map']['Height']
    
    Block_data = level_indev['Map']['Data']
    
    World_blocks = np.zeros(L * W * 64, dtype=int)
    i = 0

    for z_chunk in range(0, W//16):
        for x_chunk in range(0, L//16):
            for z in range(z_chunk*16, z_chunk*16+16):
                for x in range(x_chunk*16, x_chunk*16+16):
                    
                    for y in range(0, config['y_offset'], 2):
                        World_blocks[i] = Byte(0)
                        i += 1

                    for y in range(0, H, 2):
                        nibble0 = Block_data[(y * L + x) * W + z] // 16 % 16
                        nibble1 = Block_data[((y+1) * L + x) * W + z] // 16 % 16
                        byte = nibble1 * 16 + nibble0
                        byte -= 256 * (byte > 127)
                        World_blocks[i] = Byte(byte)
                        i += 1

                    i += (128 - H - config['y_offset']) // 2
    
    World_data_chunks = np.split(World_blocks, L//16 * W//16)
    
    return(World_data_chunks)
    
    
def convert_block_light(level_indev, config):

    L = level_indev['Map']['Length']
    W = level_indev['Map']['Width']
    H = level_indev['Map']['Height']
    
    Block_data = level_indev['Map']['Data']
    
    World_blocks = np.zeros(L * W * 64, dtype=int)
    i = 0

    for z_chunk in range(0, W//16):
        for x_chunk in range(0, L//16):
            for z in range(z_chunk*16, z_chunk*16+16):
                for x in range(x_chunk*16, x_chunk*16+16):

                    for y in range(0, config['y_offset'], 2):
                        World_blocks[i] = Byte(0)
                        i += 1
                        
                    for y in range(0, H, 2):
                        nibble0 = Block_data[(y * L + x) * W + z] % 16
                        nibble1 = Block_data[((y+1) * L + x) * W + z] % 16
                        byte = nibble1 * 16 + nibble0
                        byte -= 256 * (byte > 127)
                        World_blocks[i] = Byte(byte)
                        i += 1

                    i += (128 - H - config['y_offset']) // 2
    
    World_light_chunks = np.split(World_blocks, L//16 * W//16)
    
    return(World_light_chunks)
    
    
def calculate_height_map(World_block_chunks):

    chunk_count = len(World_block_chunks)
    World_height_map_chunks = [[] for i in range(chunk_count)]
    
    for chunk in range(0, chunk_count):
        for x in range(16):
            for z in range(16):
            
                n = z*2048 + x*128
                column = World_block_chunks[chunk][n:n+128][::-1]
                
                try: top_block = 128 - [i for i, x in enumerate(column) if not(x in [0, 6, 20, 37, 38, 39, 40, 50, 51])][0]
                except: top_block = 0
                
                World_height_map_chunks[chunk].append(Byte(top_block))
    
    return(World_height_map_chunks)
    
    
def create_level_dat_alpha(world_name, level_indev, config):
    
    for Entity in level_indev['Entities']:
        if Entity['id'] == 'LocalPlayer':
            level_dat_alpha = {}
            
            # 加载旧值或默认值
            level_dat_alpha['Inventory'] = Entity['Inventory']
            level_dat_alpha['Motion0'] = Double(Entity['Motion'][0])
            level_dat_alpha['Motion1'] = Double(Entity['Motion'][1])
            level_dat_alpha['Motion2'] = Double(Entity['Motion'][2])
            level_dat_alpha['Pos0'] = Double(Entity['Pos'][0] + config['x_chunk_offset'] * 16)
            level_dat_alpha['Pos1'] = Double(Entity['Pos'][1] + config['y_offset'])
            level_dat_alpha['Pos2'] = Double(Entity['Pos'][2] + config['z_chunk_offset'] * 16)
            level_dat_alpha['Rotation'] = Entity['Rotation']
            level_dat_alpha['Air'] = Entity['Air']
            try: level_dat_alpha['AttackTime'] = Entity['AttackTime']
            except: level_dat_alpha['AttackTime'] = Short(0)
            try: level_dat_alpha['DeathTime'] = Entity['DeathTime']
            except: level_dat_alpha['DeathTime'] = Short(0)
            level_dat_alpha['FallDistance'] = Entity['FallDistance']
            level_dat_alpha['Fire'] = Entity['Fire']
            try: level_dat_alpha['Health'] = Entity['Health']
            except: level_dat_alpha['Health'] = Short(10)
            try: level_dat_alpha['HurtTime'] = Entity['HurtTime']
            except: level_dat_alpha['HurtTime'] = Short(0)
            level_dat_alpha['OnGround'] = Byte(1)
            level_dat_alpha['Score'] = Entity['Score']
            level_dat_alpha['SpawnX'] = Int(level_indev['Map']['Spawn'][0] + config['x_chunk_offset'] * 16)
            level_dat_alpha['SpawnY'] = Int(level_indev['Map']['Spawn'][1] + config['y_offset'])
            level_dat_alpha['SpawnZ'] = Int(level_indev['Map']['Spawn'][2] + config['z_chunk_offset'] * 16)
            level_dat_alpha['LastPlayed'] = level_indev['About']['CreatedOn']
            try: level_dat_alpha['Time'] = Long(level_indev['Environment']['TimeOfDay'])
            except: level_dat_alpha['Time'] = Long(0)
            
            break
            
    data_compound = {
        'Player': Compound({
            'Inventory': level_dat_alpha['Inventory'],
            'Motion': List[Double]([level_dat_alpha['Motion0'], level_dat_alpha['Motion1'], level_dat_alpha['Motion2']]),
            'Pos': List[Double]([level_dat_alpha['Pos0'], level_dat_alpha['Pos1'], level_dat_alpha['Pos2']]),
            'Rotation': level_dat_alpha['Rotation'],
            'Air': level_dat_alpha['Air'],
            'AttackTime': level_dat_alpha['AttackTime'],
            'DeathTime': level_dat_alpha['DeathTime'],
            'FallDistance': level_dat_alpha['FallDistance'],
            'Fire': level_dat_alpha['Fire'],
            'Health': level_dat_alpha['Health'],
            'HurtTime': level_dat_alpha['HurtTime'],
            'OnGround': level_dat_alpha['OnGround'],
            'Score': level_dat_alpha['Score'],
            }),
        'LastPlayed': level_dat_alpha['LastPlayed'],
        'SpawnX': level_dat_alpha['SpawnX'],
        'SpawnY': level_dat_alpha['SpawnY'],
        'SpawnZ': level_dat_alpha['SpawnZ'],
        'Time': level_dat_alpha['Time']
        }
        
    if not config['random_seed'] is None:
        data_compound['RandomSeed'] = Long(config['random_seed'])
    
    # 创建文件
    new_file = File({
        '': Compound({
            'Data': Compound(data_compound)
            })
        })

    new_file.save(f'{world_name}/level.dat', gzipped=True)
    

def create_chunks(world_name, level_indev, World_entity_chunks, World_tile_entity_chunks, World_block_chunks, World_data_chunks, World_light_chunks, World_height_map_chunks, config):

    L = level_indev['Map']['Length'] // 16
    W = level_indev['Map']['Width'] // 16
    chunk_count = L * W
    
    for i in range(chunk_count):
    
        x = i // L + config['x_chunk_offset']
        z = i % L + config['z_chunk_offset']
        x36folder = np.base_repr(x % 64, 36).lower()
        z36folder = np.base_repr(z % 64, 36).lower()
        x36file = np.base_repr(x, 36).lower()
        z36file = np.base_repr(z, 36).lower()
            
        new_file = File({
        '': Compound({
            'Level': Compound({
                'Entities': List[Compound](World_entity_chunks[i]),
                'TileEntities': List[Compound](World_tile_entity_chunks[i]),
                'LastUpdate': Long(200),
                'xPos': Int(x),
                'zPos': Int(z),
                'Blocks': ByteArray(World_block_chunks[i]),
                'Data': ByteArray(World_data_chunks[i]),
                'BlockLight': ByteArray(np.zeros(16384, dtype=int)),
                'SkyLight': ByteArray(World_light_chunks[i]),
                'HeightMap': ByteArray(World_height_map_chunks[i]),
                'TerrainPopulated': Byte(config['terrain_populated']),
                })
            })
        })
        
        try: os.mkdir(f'{world_name}/{x36folder}/')
        except: pass
        try: os.mkdir(f'{world_name}/{x36folder}/{z36folder}/')
        except: pass
        
        new_file.save(f'{world_name}/{x36folder}/{z36folder}/c.{x36file}.{z36file}.dat', gzipped=True)


def indev_converter(file_name, config):

    while True:
        world_indev = load_indev(file_name)
        fileb = []
        worldname = easygui.enterbox('请输入存档名称', 'indev文件转换器', 'World1')
        folder = easygui.diropenbox('请选择文件保存路径', 'indev文件转换器')
        if folder == None or worldname == None:
            easygui.msgbox('请输入正确的文件保存路径或正确的文件名称', 'indev文件转换器')
        else:
            fileb.append(folder.replace('\\', '/'))
            world_name = fileb[0] + '/' + worldname
            break

    L = int(world_indev['Map']['Length'])
    W = int(world_indev['Map']['Width'])
    H = int(world_indev['Map']['Height'])

    print(f"转换目标文件中：{file_name}:")

    if L % 16: raise ValueError(f'地图长度不能被 16 整除(长度：{L})')
    if W % 16:raise ValueError(f'地图宽度不能被 16 整除(宽度: {W})')
    if H > 128:raise ValueError(f'地图高度不能大于 128(高度: {H})')

    os.mkdir(world_name)
    
    print("正在转换实体...", end='\r')
    world_entity = convert_entities(world_indev, config)
    
    print("正在转换磁贴实体...", end='\r')
    world_tile_entity = convert_tile_entities(world_indev, config)
    
    print("正在转换方块...", end='\r')
    world_block_ID = convert_block_IDs(world_indev, config)
    
    print("正在转换数据值...", end='\r')
    world_block_DV = convert_block_DVs(world_indev, config)
    
    print("正在转换光源...", end='\r')
    world_block_light = convert_block_light(world_indev, config)

    print("正在计算地图高度...", end='\r')
    world_height_map = calculate_height_map(world_block_ID)
    
    print("正在创建文件...", end='\r')
    create_level_dat_alpha(world_name, world_indev, config)
    create_chunks(world_name, world_indev, world_entity, world_tile_entity, world_block_ID, world_block_DV, world_block_light, world_height_map, config)

    easygui.msgbox(f"已将{file_name}转换为世界{world_name}!", 'indev文件转换器')


def test_config(config):
    
    if not type(config['x_chunk_offset']) is int:
        raise ValueError("x_chunk_offset必须是整数")

    if not type(config['z_chunk_offset']) is int:
        raise ValueError("z_chunk_offset必须是整数")

    if config['y_offset'] > 64:
        raise ValueError("y_offset必须小于或等于 64")

    if config['y_offset'] % 2:
        raise ValueError("y_offset必须是偶数")

    if config['offset_fill_block'] > 255:
        raise ValueError("offset_fill_block必须是有效的区块 ID")

    if config['terrain_populated'] != 0 and config['terrain_populated'] != 1:
        raise ValueError("terrain_populated必须是 0 或 1")

    if not type(config['random_seed']) is int and not config['random_seed'] is None:
        raise ValueError("random_seed必须是整数或空")

    
if __name__ == '__main__':
    
    # 查找世界
    try:
        world = easygui.fileopenbox('', 'indev文件转换器', '*.mclevel')
        worlds = []
        worlds.append(world.replace('\\', '/'))
    except:
        exit()

    # 查找配置文件
    with open("config.yml", 'r') as config_file:
        config = safe_load(config_file)
        test_config(config)
        
    print("已成功加载 config.yml")
    print(f"目标文件路径：{', '.join(worlds)}")

    for world in worlds:
        try: 
            indev_converter(world, config)
        except Exception as e:
            easygui.msgbox(f'无法转换{world}: {e}', 'indev文件转换器')
