# Slidown

<div align="center">
  <h1 style="font-family: 'Orbitron', sans-serif; font-size: 3rem; letter-spacing: -1px;">
    <span style="font-weight: 700; color: #00D9FF; text-shadow: 0 0 10px rgba(0, 217, 255, 0.5);">Sli</span><span style="font-weight: 300; color: #555; padding: 0 0.2rem;">|</span><span style="font-weight: 300; color: #888888;">down</span>
  </h1>
</div>

Transform Markdown into Beautiful HTML Presentations
将 Markdown 笔记优雅转换为网页版演示文稿

## 功能特性

- 完整支持 Markdown 语法（标题、列表、代码块、文本、链接、图片、表格等）
- 自动将内容分页（基于标题层级）
- 精美的 Cyberpunk 科技风格设计
- 键盘/触摸翻页支持（←/→ 或 PageUp/PageDown）
- 单文件输出（CSS/JS 内联，无外部依赖）
- 响应式设计，适配不同屏幕
- 全屏模式和进度条显示
- 代码语法高亮
- 平滑过渡动画
- 保持原文内容完整

## 快速开始

### 安装依赖

```bash
pip install -r requirements.txt
```

依赖项：
- `markdown>=3.4.1` - Markdown 解析
- `Pygments>=2.15.0` - 代码语法高亮

### 基本用法

```bash
# 转换 Markdown 文件为 HTML 演示文稿
python slidedown.py input.md output.html

# 在浏览器中打开
open output.html  # macOS
# 或
xdg-open output.html  # Linux
# 或直接在浏览器中打开文件
```

### 命令行选项

```bash
# 查看帮助
python slidedown.py --help

# 自定义分页层级（使用 H1 标题分页）
python slidedown.py input.md output.html --split-level 1

# 使用 H2 标题分页（默认）
python slidedown.py input.md output.html --split-level 2

# 使用 H3 标题分页
python slidedown.py input.md output.html --split-level 3

# 选择主题
python slidedown.py input.md output.html --theme cyberpunk  # Cyberpunk 主题（默认）
python slidedown.py input.md output.html --theme light      # 亮色主题
python slidedown.py input.md output.html --theme dark       # 暗色主题
python slidedown.py input.md output.html --theme clean      # 简洁主题
```

## 演示文稿操作指南

在浏览器中打开生成的 HTML 文件后：

### 键盘导航
- **→** 或 **空格** 或 **PageDown**：下一页
- **←** 或 **PageUp**：上一页
- **Home**：跳转到第一页
- **End**：跳转到最后一页
- **F11** 或点击全屏按钮：全屏模式

### 触摸导航
- 左滑：下一页
- 右滑：上一页

### 鼠标导航
- 点击右侧区域：下一页
- 点击左侧区域：上一页

## 支持的 Markdown 语法

- **标题**（H1-H6）
- **有序列表和无序列表**
- **代码块**（带语法高亮）
- **行内代码**
- **粗体、斜体、删除线**
- **链接**
- **图片**（支持本地和网络图片）
- **表格**
- **引用块**
- **水平分割线**
- **换行**

## 示例

```bash
# 转换示例文件
python slidedown.py examples/example.md examples/example_presentation.html

# 使用 H1 标题分页（每个 H1 标题创建新幻灯片）
python slidedown.py notes.md notes.html --split-level 1

# 使用暗色主题
python slidedown.py lecture.md lecture.html --theme dark
```

## 设计特点

### Cyberpunk 主题（默认）
- 科技感网格背景
- 扫描线效果
- 霓虹色彩（青色、品红、绿色、黄色）
- 发光文字效果
- 平滑过渡动画
- 专业字体组合（Orbitron + JetBrains Mono + Noto Sans SC）

### 其他主题
- **Light**：明亮干净的亮色主题
- **Dark**：优雅的暗色主题
- **Clean**：简洁专业的主题

### 布局特点
- 标题幻灯片居中显示
- 内容幻灯片左对齐
- 自动滚动（内容过多时）
- 响应式设计（手机、平板、电脑）

## 输出特点

- **单文件输出**：所有 CSS 和 JavaScript 都内联在 HTML 中
- **无外部依赖**：可以直接在浏览器中打开，无需网络连接
- **体积小**：纯文本 HTML 文件，易于分享
- **兼容性好**：支持所有现代浏览器（Chrome、Firefox、Safari、Edge）
- **易于分享**：通过邮件、云盘、网页托管轻松分享

## 项目结构

```
Slidown/
├── README.md              # 使用说明（本文件）
├── USAGE_GUIDE.md         # 详细使用指南
├── CHANGELOG.md           # 版本历史
├── requirements.txt       # Python 依赖
├── slidedown.py           # HTML 演示文稿转换器（主程序）
├── examples/              # 示例文件
│   ├── example.md         # 示例 Markdown
│   └── *.html             # 示例输出
├── templates/             # 主题配置（可选）
└── utils/                 # 工具模块
    ├── __init__.py
    ├── parser.py          # Markdown 解析器
    ├── theme.py           # 主题配置
    └── code_highlight.py  # 代码高亮
```

## 技术实现

- **解析器**：使用 Python `markdown` 库解析 Markdown
- **代码高亮**：使用 `Pygments` 进行语法高亮
- **渲染器**：自定义 HTML/CSS/JS 生成器
- **样式**：Cyberpunk 科技风格设计
- **导航**：纯 JavaScript 实现，无需外部库
- **动画**：CSS3 过渡和关键帧动画

## 注意事项

1. **图片路径**：支持相对路径和绝对路径，建议使用相对路径
2. **代码块**：自动应用 Pygments 语法高亮
3. **长文本**：自动启用滚动，内容不会被截断
4. **浏览器兼容**：需要现代浏览器（不支持 IE）
5. **中文字体**：自动使用 Noto Sans SC 或系统中文字体

## 使用场景

- 技术演讲和分享
- 教学课件展示
- 项目汇报
- 在线文档演示
- 代码审查演示
- 博客文章可视化

## 优势

相比传统 PowerPoint：
- 无需安装 Office 软件
- 文件体积更小
- 易于版本控制（纯文本）
- 支持代码语法高亮
- 响应式设计，适配各种设备
- 快速分享（浏览器直接打开）

## 常见问题

**Q: 生成的 HTML 文件可以离线使用吗？**
A: 可以，所有资源都内联在 HTML 文件中，无需网络连接。

**Q: 如何自定义主题？**
A: 目前支持 4 种内置主题（cyberpunk/light/dark/clean），可以通过 `--theme` 参数选择。

**Q: 支持数学公式吗？**
A: 当前版本不内置数学公式支持，但可以在 HTML 中手动添加 MathJax 或 KaTeX。

**Q: 图片路径怎么处理？**
A: 建议使用相对路径。如果使用网络图片，确保有网络连接。

**Q: 可以导出为 PDF 吗？**
A: 可以在浏览器中使用"打印为 PDF"功能导出。

## 许可证

MIT License

## 项目说明

**Slidown** - 项目名称结合了 "Slide"（幻灯片）和 "Markdown" 的双关含义。本项目专注于将 Markdown 文档转换为精美的 HTML 格式网页演示文稿，让内容展示更加优雅和专业。

## Logo 设计

Slidown 采用纯 CSS 实现的 Logo 设计，无需任何图片文件：

```html
<div class="logo">
  <span class="logo-sli">Sli</span><span class="logo-separator">|</span><span class="logo-down">down</span>
</div>
```

**设计理念：**
- **Sli** - 粗体青色 (#00D9FF)，带发光效果 - 代表技术与转换
- **|** - 细体灰色分隔符 - 连接两种格式
- **down** - 细体灰色 (#888888) - 代表 Markdown 基础

完整的 CSS 实现和官方网站请访问 `website/index.html`
