# MyVoidBot

## 介绍

cover & copy 一些好玩的插件 <br />
基于 [voidbot](https://github.com/FloatTech/voidbot) , 略有修改:
1. 增加了message格式转化
2. 增加了插件加载机制
3. 拓展了一些message处理工具 , 如获取message中被at的人
4. 一些异常的处理

## 插件列表

| 插件名      | 介绍 | 备注 | LICENSE |
| ----------- | ----------- | ----------- | ----------- |
| [myfriend](/plus/myfriend_plus)  | 我的朋友图片合成       | 模板插件 | MIT |
| [randpic](/plus/randpic_plus)   | 发送一张随机图片   | 接口来自[iw233](https://iw233.cn/api/Random.php) | MIT |
| [zbgif](/plus/zbgif_plus)   | 各种表情包合成   | cover自[tdf1939/ZeroBot-Plugin-Gif](https://github.com/tdf1939/ZeroBot-Plugin-Gif) | - |
| [todaynew](/plus/todaynew_plus)   | 今日新闻   | 接口来自[优客API](https://api.iyk0.com/60s/) | MIT |
| [wordcloud](/plus/wordcloud_plus)   | 今日词云   | cover自[Hellobaka/WordCloud](https://github.com/Hellobaka/WordCloud) | ApacheV2 |
| [EmojiMix](/plus/emojimix_plus)   | Emoji混合   | cover自[Hellobaka/EmojiMix](https://github.com/Hellobaka/EmojiMix) | ApacheV2 |

## 环境运行

python 3.8 & [onebot-11](https://github.com/botuniverse/onebot-11)

## 注意

这不是voidbot的插件框架 , 请不要在这个项目中直接pr新的插件. 同时 , 也不保证这个项目外的插件的兼容性 .

voidbot使用 Apache License V2 , 所以这个项目中core文件夹中的内容也遵循 Apache License V2 . plus文件夹中的内容 , 因cover/copy的对象不同 , 所以 , 可能会有各自不同的协议 .
