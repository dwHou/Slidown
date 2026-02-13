# Slidown 使用指南

详细使用说明和高级功能指南

## 快速开始

### 1. 安装依赖

```bash
cd /Applications/Programming/code/GitProj/Slidown
pip install -r requirements.txt
```

仅需两个依赖包：
- `markdown` - Markdown 文档解析
- `Pygments` - 代码语法高亮

### 2. 基本使用

```bash
# 转换单个文件（默认 Cyberpunk 主题）
python slidedown.py input.md output.html

# 使用暗色主题
python slidedown.py input.md output.html --theme dark

# 使用亮色主题
python slidedown.py input.md output.html --theme light

# 使用简洁主题
python slidedown.py input.md output.html --theme clean
```

## 高级功能

### 自定义分页级别

默认情况下，工具会在 H2 标题（##）处创建新幻灯片。你可以自定义：

```bash
# H1 标题创建新幻灯片（更少的幻灯片）
python slidedown.py input.md output.html --split-level 1

# H2 标题创建新幻灯片（默认，推荐）
python slidedown.py input.md output.html --split-level 2

# H3 标题创建新幻灯片（更多的幻灯片）
python slidedown.py input.md output.html --split-level 3
```

### 主题选择

```bash
# Cyberpunk 主题（默认，科技感强）
python slidedown.py input.md output.html --theme cyberpunk

# 暗色主题（优雅黑色背景）
python slidedown.py input.md output.html --theme dark

# 亮色主题（明亮白色背景）
python slidedown.py input.md output.html --theme light

# 简洁主题（专业简约风格）
python slidedown.py input.md output.html --theme clean
```

### 查看帮助信息

```bash
python slidedown.py --help
```

## 支持的 Markdown 语法

### 1. 标题

```markdown
# H1 标题
## H2 标题
### H3 标题
#### H4 标题
##### H5 标题
###### H6 标题
```

### 2. 文本格式

```markdown
**粗体文本**
*斜体文本*
`行内代码`
~~删除线~~
```

### 3. 列表

```markdown
- 无序列表项 1
- 无序列表项 2
  - 嵌套列表项
- 无序列表项 3

1. 有序列表项 1
2. 有序列表项 2
3. 有序列表项 3
```

### 4. 代码块

支持语法高亮的代码块：

````markdown
```python
def hello():
    print("Hello, World!")
```

```javascript
function hello() {
    console.log("Hello, World!");
}
```

```bash
echo "Hello, World!"
```
````

支持的语言包括：Python, JavaScript, TypeScript, C++, C#, Java, Go, Rust, Ruby, PHP, Shell, SQL, HTML, CSS, JSON, YAML, Markdown 等。

### 5. 引用块

```markdown
> 这是一段引用文本。
> 可以包含多行。
```

### 6. 链接

```markdown
[链接文本](https://example.com)
[内部链接](#section-id)
```

### 7. 图片

```markdown
![图片描述](path/to/image.png)
![网络图片](https://example.com/image.png)
```

支持：
- 本地图片（相对路径和绝对路径）
- 网络图片（需要网络连接）
- 自动适应幻灯片大小

### 8. 表格

```markdown
| 列1 | 列2 | 列3 |
|-----|-----|-----|
| A   | B   | C   |
| D   | E   | F   |
```

### 9. 分隔线

```markdown
---
```

## 演示文稿操作

### 键盘导航

- **→** 或 **空格** 或 **PageDown**：下一页
- **←** 或 **PageUp**：上一页
- **Home**：跳转到第一页
- **End**：跳转到最后一页
- **F11**：全屏模式
- **Esc**：退出全屏

### 触摸导航

- **左滑**：下一页
- **右滑**：上一页
- **双击**：全屏模式

### 鼠标导航

- **点击右侧**：下一页
- **点击左侧**：上一页
- **点击全屏按钮**：全屏模式

## 主题详解

### 1. Cyberpunk 主题（默认）

科技感强烈的未来主义风格：

- 深色背景 + 网格纹理
- 霓虹色彩（青色、品红、绿色、黄色）
- 扫描线效果
- 发光文字效果
- 适合：技术演讲、创新项目展示

```bash
python slidedown.py input.md output.html --theme cyberpunk
```

### 2. Dark 主题

优雅的暗色风格：

- 深色背景
- 高对比度文字
- 现代简约设计
- 适合：技术分享、产品演示

```bash
python slidedown.py input.md output.html --theme dark
```

### 3. Light 主题

明亮清新的风格：

- 白色背景
- 柔和色彩
- 清晰易读
- 适合：教学课件、商务汇报

```bash
python slidedown.py input.md output.html --theme light
```

### 4. Clean 主题

专业简约的风格：

- 简洁设计
- 专业配色
- 无多余装饰
- 适合：学术演讲、专业报告

```bash
python slidedown.py input.md output.html --theme clean
```

## 实际案例

### 案例 1：转换技术笔记

```bash
python slidedown.py 3DGS_OpenCVTeam.md 3DGS_Presentation.html --theme cyberpunk
```

这将：
- 在每个 H2 标题处创建新幻灯片
- 自动高亮代码块
- 使用 Cyberpunk 科技主题
- 保留所有数学公式和技术内容

### 案例 2：创建教学课件

```bash
python slidedown.py lecture_notes.md lecture.html --theme light --split-level 2
```

这将：
- 使用明亮的亮色主题
- H2 标题分页
- 适合教室投影展示

### 案例 3：创建简短演示

```bash
python slidedown.py README.md README_presentation.html --split-level 1 --theme dark
```

这将：
- 在每个 H1 标题处创建新幻灯片（更少的幻灯片）
- 使用暗色主题
- 适合快速演示

### 案例 4：在线分享

```bash
python slidedown.py article.md article.html --theme clean
```

生成的 HTML 文件可以：
- 直接上传到网站
- 通过邮件发送
- 在任何浏览器中打开
- 无需任何外部依赖

## 技巧和最佳实践

### 1. 组织 Markdown 内容

为了获得最佳的演示效果：

- 使用清晰的标题层级
- 每个部分不要太长（建议每个 H2 部分 10-30 行）
- 合理使用列表和代码块
- 图片使用相对路径（便于分享）

示例结构：

```markdown
# 演示文稿标题

简短介绍

## 第一部分

主要内容 1

## 第二部分

主要内容 2

### 子部分 2.1

详细说明

## 总结

总结和展望
```

### 2. 代码块优化

- 代码块不要太长（建议不超过 20-30 行）
- 使用语言标识符以启用语法高亮
- 添加注释说明关键代码
- 分段展示复杂代码

示例：

````markdown
```python
# 数据预处理
def preprocess(data):
    # 数据清洗
    data = clean(data)
    # 特征提取
    features = extract_features(data)
    return features
```
````

### 3. 图片处理

- 图片大小建议不超过 1920x1080
- 使用常见格式（PNG、JPG、WebP）
- 确保图片路径正确
- 建议使用相对路径

```markdown
<!-- 推荐：相对路径 -->
![架构图](images/architecture.png)

<!-- 可以：网络图片 -->
![Logo](https://example.com/logo.png)
```

### 4. 主题选择建议

| 场景 | 推荐主题 | 原因 |
|------|---------|------|
| 技术演讲 | Cyberpunk, Dark | 科技感强，代码易读 |
| 教学课件 | Light, Clean | 明亮清晰，长时间观看舒适 |
| 商务汇报 | Clean, Light | 专业正式 |
| 创新项目 | Cyberpunk | 视觉冲击力强 |
| 学术报告 | Clean, Dark | 简洁专业 |

### 5. 分页级别建议

| 内容类型 | 推荐级别 | 说明 |
|---------|---------|------|
| 详细教程 | level 2 (H2) | 内容丰富，需要细分 |
| 快速介绍 | level 1 (H1) | 简短有力，幻灯片少 |
| 复杂文档 | level 3 (H3) | 内容层次多，需要详细分割 |

## 高级技巧

### 1. 混合使用图片和代码

```markdown
## 架构设计

![系统架构](images/architecture.png)

### 核心代码

```python
class System:
    def __init__(self):
        self.initialize()
```
```

### 2. 使用表格展示对比

```markdown
## 方案对比

| 方案 | 优点 | 缺点 | 推荐度 |
|------|-----|------|--------|
| A    | 简单 | 性能低 | ⭐⭐⭐ |
| B    | 高效 | 复杂 | ⭐⭐⭐⭐⭐ |
```

### 3. 使用引用突出重点

```markdown
## 核心观点

> 重要的事情说三遍：
> 测试、测试、测试！
```

### 4. 合理使用空行

```markdown
## 标题

第一段内容

第二段内容（空行分隔，更清晰）
```

## 故障排除

### 问题 1：图片不显示

**原因**：图片路径不正确或文件不存在

**解决**：
- 检查图片路径是否正确
- 使用相对路径时确保路径相对于 Markdown 文件
- 确认图片文件存在
- 网络图片需要确保网络连接

### 问题 2：代码没有高亮

**原因**：未指定语言或语言不支持

**解决**：
- 在代码块中指定语言：````python` 而不是 ````
- 检查语言名称是否正确
- 使用常见的语言别名（如 `py` 代替 `python`）

### 问题 3：中文字体显示异常

**原因**：浏览器字体设置或系统缺少中文字体

**解决**：
- 使用 Cyberpunk 主题（自动加载 Google Fonts 中文字体）
- 确保系统安装了中文字体
- 检查浏览器字体设置

### 问题 4：幻灯片内容过多

**原因**：单个幻灯片内容太长

**解决**：
- 减少每个部分的内容
- 降低 `--split-level` 值以创建更多幻灯片
- 将长代码块分割成多个小块
- 使用子标题进一步分割内容

### 问题 5：翻页不流畅

**原因**：浏览器性能或内容过多

**解决**：
- 优化图片大小
- 减少单个幻灯片的内容
- 使用现代浏览器（Chrome、Firefox、Safari、Edge）
- 关闭不必要的浏览器扩展

## 导出和分享

### 导出为 PDF

1. 在浏览器中打开 HTML 文件
2. 按 `Ctrl+P` (Windows) 或 `Cmd+P` (macOS)
3. 选择"另存为 PDF"
4. 调整页面设置（建议横向）
5. 保存

### 在线分享

1. 将 HTML 文件上传到：
   - GitHub Pages
   - Netlify
   - Vercel
   - 任何静态网站托管服务

2. 或者通过：
   - 邮件附件
   - 云盘分享（Dropbox、OneDrive、Google Drive）
   - 即时通讯工具

### 嵌入网页

```html
<iframe src="presentation.html"
        width="100%"
        height="600px"
        frameborder="0">
</iframe>
```

## 项目结构说明

```
Slidown/
├── slidedown.py           # 主程序（HTML 演示文稿生成器）
├── requirements.txt       # Python 依赖列表
├── README.md              # 项目说明文档
├── QUICKSTART.md          # 快速开始指南
├── USAGE_GUIDE.md         # 使用指南（本文件）
├── CHANGELOG.md           # 版本历史
│
├── utils/                 # 核心功能模块
│   ├── __init__.py        # 模块初始化
│   ├── parser.py          # Markdown 解析器
│   ├── theme.py           # 主题管理器
│   └── code_highlight.py  # 代码高亮器
│
├── templates/             # 主题模板配置（可选）
│   └── *.json             # 主题配置文件
│
└── examples/              # 示例文件
    ├── example.md         # 示例 Markdown 文件
    └── *.html             # 示例输出文件
```

## 技术实现细节

### 架构设计

```
Markdown 文件
    ↓
[解析器] parser.py
    ↓
结构化数据（幻灯片列表）
    ↓
[主题管理] theme.py
    ↓
[代码高亮] code_highlight.py
    ↓
[HTML 生成器] slidedown.py
    ↓
单文件 HTML（内联 CSS/JS）
```

### 关键特性

1. **单文件输出**：所有 CSS 和 JavaScript 都内联在 HTML 中
2. **无外部依赖**：可离线使用，无需网络连接
3. **响应式设计**：自动适配不同屏幕尺寸
4. **代码高亮**：使用 Pygments 进行语法高亮
5. **平滑动画**：CSS3 过渡效果

## 开发和扩展

### 添加自定义样式

可以在生成的 HTML 文件中直接修改 `<style>` 标签内的 CSS。

### 添加自定义 JavaScript

可以在生成的 HTML 文件末尾添加自定义脚本。

### 创建自定义主题

参考 `slidedown.py` 中的主题定义，创建新的主题配置。

## 常见问题 FAQ

**Q1: 生成的 HTML 文件可以离线使用吗？**
A: 是的，所有资源都内联在 HTML 文件中，完全可以离线使用。

**Q2: 支持移动设备吗？**
A: 支持，响应式设计自动适配手机和平板。

**Q3: 可以自定义主题吗？**
A: 可以，目前支持 4 种内置主题，也可以编辑生成的 HTML 文件自定义样式。

**Q4: 支持数学公式吗？**
A: 当前版本不内置数学公式支持，但可以手动在 HTML 中添加 MathJax 或 KaTeX。

**Q5: 文件大小会很大吗？**
A: 不会，纯文本 HTML 文件通常在 100-500KB 左右（取决于内容长度）。

**Q6: 可以嵌入视频吗？**
A: 可以，使用标准的 HTML `<video>` 标签或嵌入 YouTube/Vimeo 链接。

**Q7: 浏览器兼容性如何？**
A: 支持所有现代浏览器（Chrome、Firefox、Safari、Edge），不支持 IE。

**Q8: 可以导出为 PowerPoint 吗？**
A: 不可以直接导出，但可以使用浏览器的"打印为 PDF"功能导出 PDF。

## 联系和反馈

如有问题或建议，欢迎提交 Issue 或 Pull Request。

---

**Version**: 2.1.0
**Last Updated**: 2026-02-13
**Project**: Slidown (Transform Markdown into Beautiful HTML Presentations)
