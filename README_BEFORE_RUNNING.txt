# 重要提示：解决中文字体显示问题

如果您在运行游戏时发现中文字符显示为方块或乱码，请按照以下步骤操作：

## 1. 添加中文字体

请下载以下任意一款中文字体并放置到 `assets/fonts/` 目录：

- SimHei.ttf (黑体)
- SimSun.ttf (宋体)
- Microsoft YaHei (微软雅黑)
- SourceHanSansSC-Regular.otf (思源黑体)

字体下载链接：
- SimHei: https://www.fonts.net.cn/font-download-29.html
- 思源黑体: https://github.com/adobe-fonts/source-han-sans/tree/release

## 2. 修改配置（可选）

如果您添加了与默认字体名称不同的字体，请修改 `src/utils/helpers.py` 文件中的 
`DEFAULT_FONT_FILENAME` 变量为您添加的字体文件名。

## 3. 重新启动游戏

添加字体后，重新启动游戏，中文应该可以正常显示了。

## 故障排除

如果添加字体后仍然无法显示中文：

1. 确保字体文件已正确放置在 `assets/fonts/` 目录中
2. 查看游戏启动时的控制台输出，寻找字体加载相关的错误信息
3. 尝试使用不同的中文字体
4. 确保使用的是支持中文的操作系统环境

## 系统要求

- Python 3.6+
- Pygame 2.0+
- 操作系统需支持中文字符显示

如有任何问题，请参考 `docs/使用指南.md` 获取更多帮助信息。
