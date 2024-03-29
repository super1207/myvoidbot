# MyVoidBot

## 介绍

cover & copy 一些好玩的插件 <br />
基于 [voidbot](https://github.com/FloatTech/voidbot) , 略有修改:
1. 增加了message格式转化
2. 增加了插件加载机制
3. 拓展了一些message处理工具 , 如获取message中被at的人
4. 一些异常的处理

## 插件列表

| 插件名      | 介绍 | 备注 | LICENSE | 三方库依赖 |
| ----------- | ----------- | ----------- | ----------- | ----------- |
| [myfriend](/plus/myfriend_plus)  | 我的朋友图片合成       | 如果在linux上，需要自己将`simsun.ttc`放到`/usr/share/fonts/font/`目录下 | MIT | Pillow |
| [randpic](/plus/randpic_plus)   | 发送一张随机图片   | 接口来自[iw233](https://iw233.cn/api/Random.php) | MIT | - |
| [zbgif](/plus/zbgif_plus)   | 各种表情包合成   | cover自[tdf1939/ZeroBot-Plugin-Gif](https://github.com/tdf1939/ZeroBot-Plugin-Gif) | - | Pillow |
| [todaynew](/plus/todaynew_plus)   | 今日新闻   | 接口来自[优客API](https://api.iyk0.com/60s/)，已经失效 | MIT | - |
| [wordcloud](/plus/wordcloud_plus)   | 今日词云   | cover自[Hellobaka/WordCloud](https://github.com/Hellobaka/WordCloud)，如果在linux上，需要自己将`simsun.ttc`放到`/usr/share/fonts/font/`目录下 | ApacheV2 | jieba,zhon,wordcloud |
| [EmojiMix](/plus/emojimix_plus)   | Emoji混合   | cover自[Hellobaka/EmojiMix](https://github.com/Hellobaka/EmojiMix) | ApacheV2 | - |
| [runall](/plus/runall_plus)   | 在线运行各种编程语言   | cover自[super1207/runall](https://github.com/super1207/runall) | AGPLV3 | - |
| [cet4](/plus/cet4_plus)   | 发送一套四级听力   | cover自[renren0103/CET4-Mirai](https://github.com/renren0103/CET4-Mirai) | - | - |
| [givemepic](/plus/givemepic_plus)   | 来点xxx的图片  | cover自[super1207/PicBot](https://github.com/super1207/PicBot) | AGPLV3 | - |
| [picsearch](/plus/picsearch_plus)   | 以图搜图  | 接口来自[yandex图片搜索](https://yandex.com/images/) | MIT | - |
| [covid_plus](/plus/covid_plus)   | 新冠疫情  | 接口来自[丁香医生](https://ncov.dxy.cn/ncovh5/view/pneumonia) | MIT | - |
| [whpj_plus](/plus/whpj_plus)   | 汇率换算  | 接口来自[中国银行](https://www.boc.cn/sourcedb/whpj) | MIT | - |
| [cppreference_plus](/plus/cppreference_plus)   | cppreference查询  | cover自[jie65535/mirai-console-jcr-plugin](https://github.com/jie65535/mirai-console-jcr-plugin) | AGPLV3 | - |
| [song_plus](/plus/song_plus)   | 点歌插件  | 接口来自[优客API](https://api.iyk0.com/doc/wymusic)，已经失效 | MIT | - |
| [getwife_plus](/plus/getwife_plus)   | 今天谁是我老婆  | cover自(果果,QQ:2114460639) | - | - |
| [express_plus](/plus/express_plus)   | 查询快递单号  | 接口来自[alapi](https://www.alapi.cn/),需要自己注册账号并获取token | MIT | - |
| [repeat_plus](/plus/repeat_plus)   | 复读插件  | idea来自幽幽子(QQ:2694900224) | MIT | - |

## 运行

### 运行环境

python 3.8 & [onebot-11](https://github.com/botuniverse/onebot-11)

### 如何运行

1. 先用pip安装 requestment.txt 里面的依赖
2. 修改 core/Voidbot.py 里面的ws正向连接端口号等信息
3. 运行 core/Voidbot.py

## 注意

这不是voidbot的插件框架 , 请不要在这个项目中直接pr新的插件. 同时 , 也不保证这个项目外的插件的兼容性 .

voidbot使用 Apache License V2 , 所以这个项目中core文件夹中的内容也遵循 Apache License V2 . plus文件夹中的内容 , 因cover/copy的对象不同 , 所以 , 可能会有各自不同的协议 .
