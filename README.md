MCFC使用教程

准备工作：
1.去 https://www.python.org/downloads/ 里下载python
2.用管理员方式打开命令提示符(cmd)，然后输入python -m pip install nbtlib pyyaml easygui

一．打开：
1.按win+r输入cmd
2.cd 到当前文件目录(如果你的文件不在c盘，那么你需要输入文件所在盘符(例如D:))(例如我的MCFC包内文件路径在D:\Demo)
3.定位之后输入 python menu.py 
4.如果没有问题的话，那么会弹出一个窗口(菜单)

二.classic(.mine)转indev(.mclevel)
1.在菜单中依次打开 运行文件转换器 -classic文件转换器
2. 然后打开要转换的mc存档(例如我这里的text.mine)
3.随后把转换后的文件名填入输入框内
4.然后在选择文件保存路径
5.转换成功后会弹出一个窗口
6.打开游戏，然后打开存档即可游玩

三。indev(.mclevel) 转Alpha
1.在菜单中依次打开 运行文件转换器 -indev文件转换器
2.然后打开要转换的mc存档(例如我这里的text-indev.mclevel)
3.随后把转换后的文件名填入输入框内(如果转换后用Infdev 20100327 - Beta 1.2_01玩的话只能命名为World1-World5,当然您也可以使用将 alpha 保存格式转换为 mcregion 文件格式 （Beta 1.3 - 1.1） 的任何版本(没有命名限制).事实上,Infdev 0227也可以(需要装存档功能Mod,也只能命名为World1-World5))
4.然后在选择文件保存路径
5.转换成功后会弹出一个窗口
6.打开游戏，然后打开存档即可游玩

注意：
1.除了本教程文件以外，其它文件不能删除，一旦删除可能引发程序错误
2.无论标签集如何，世界都会在 Infdev 20100327中重新填充。这意味着你会看到比你想象的更多的树木，矿石和洞穴。
3.如果你的世界在加载时崩溃了，那么在该版本中，你可能有一些带有无效ID的块（可能是旧的彩色布）。
4.如果你的世界在打开一个箱子时崩溃了，那么你的箱子里可能有无效的ID（同样，可能是彩色的布）。
5.首次加载世界时，世界将需要一段时间才能播放，因为它必须重新计算光照数据，因为它不会使用此工具进行转换。
6.在Infdev 20100415之前，生物不会加载版本，因为他们在此之前没有再次保存。在这个版本之后，生物仍然会在那里，所以如果你把一个区块放在一个猪曾经的地方，它会在那个区块窒息。
7.射击箭头直到Infdev晚期/Alpha早期（版本未知）才会加载。
8.在 Indev 20100212-1 之前，火把的附着取决于它们周围的方块。这意味着，如果您在该版本之前转换一个世界，则火把似乎会放置在半空中。在上面的版本中断开并更换割炬将解决此问题。
9.部分方块、物品会转换(如：齿轮转化成红石粉(Alpha 1.0.1之后))
10.classic存档不能直接转成Alpha世界格式
11.不支持level.dat转indev世界格式

此工具不做什么：
1.它不会转换光源数据或任何未以 alpha 存储格式使用的 indev 数据（如天空盒子 颜色）。
2.它无法检查方块 ID 是否与要升级到的版本兼容。


