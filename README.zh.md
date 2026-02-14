<div align="center">

# Slidown

<h3 style="font-family: system-ui, -apple-system, sans-serif; font-size: 2.5rem; font-weight: 300; letter-spacing: -0.5px; margin: 1rem 0;">
  <span style="font-weight: 700; color: #00D9FF;">Sli</span><span style="color: #888; padding: 0 0.3rem;">|</span><span style="color: #666;">down</span>
</h3>

**将 Markdown 笔记优雅转换为网页版演示文稿**

[![PyPI version](https://img.shields.io/pypi/v/slidown-md.svg?color=00D9FF&style=for-the-badge)](https://pypi.org/project/slidown-md/)
[![Python versions](https://img.shields.io/pypi/pyversions/slidown-md.svg?color=0099FF&style=for-the-badge)](https://pypi.org/project/slidown-md/)
[![License](https://img.shields.io/github/license/dwHou/slidown.svg?color=00FF41&style=for-the-badge)](https://github.com/dwHou/slidown/blob/master/LICENSE)

[English](README.md) | [简体中文](#)

---

</div>

## ✨ 特性

<table>
<tr>
<td width="50%">

### 🎯 核心功能
- **单文件输出** - 所有 CSS/JS 内联,无外部依赖
- **智能分页** - 根据视口高度自动调整内容
- **三种精美主题** - Tech、Clean、Corporate
- **LaTeX 数学公式** - 完整支持 KaTeX 渲染
- **代码高亮** - Pygments 支持 30+ 编程语言
- **极速加载** - 轻量级架构,本地即可运行

</td>
<td width="50%">

### 🧭 导航系统
- **章节进度条** - 底部导航,支持快速跳转
- **目录面板** - 可展开侧边栏,完整文档大纲
- **键盘快捷键** - 方向键、空格、Home/End
- **触摸/鼠标支持** - 滑动手势和点击导航
- **响应式设计** - 完美适配任意屏幕尺寸

</td>
</tr>
</table>

---

## 🚀 快速开始

### 安装方式

#### 方式 1:通过 PyPI 安装(推荐)

```bash
pip install slidown-md
```

#### 方式 2:从源码安装

```bash
git clone https://github.com/dwHou/slidown.git
cd Slidown
pip install markdown pygments
```

### 基本使用

```bash
# 转换 Markdown 文档(自动生成时间戳输出文件夹)
slidown your_notes.md

# 使用指定主题
slidown your_notes.md --theme clean

# 添加自定义页脚
slidown your_notes.md --theme corporate --footer "© 2026 Your Company"
```

### 输出结构

```
your_notes_20260213143025/
├── presentation.html          # 自包含的演示文稿
├── assets/
│   └── images/               # 图片资源(默认模式)
└── README.txt                # 使用说明
```

在浏览器中打开 `presentation.html` 即可查看演示文稿。

---

## 🎨 主题

<table>
<tr>
<td width="33%">

### Tech / Cyberpunk
**默认主题**

深色背景搭配霓虹色彩(青、蓝、绿)和网格效果。

**最适合:**
- 技术演讲
- 编程教程
- 产品发布

```bash
slidown doc.md --theme tech
```

</td>
<td width="33%">

### Clean / Fresh

明亮白色背景搭配柔和、简约的设计。

**最适合:**
- 文档说明
- 教学课件
- 学术演示

```bash
slidown doc.md --theme clean
```

</td>
<td width="33%">

### Corporate

专业商务风格搭配深蓝/灰色配色。

**最适合:**
- 企业宣讲
- 正式报告
- 投资人演示

```bash
slidown doc.md --theme corporate
```

</td>
</tr>
</table>

---

## 📖 文档

### 命令行参数

```bash
slidown INPUT [OPTIONS]

必需参数:
  INPUT                     输入 Markdown 文件路径

输出选项:
  -o, --output DIR          输出基础目录(默认:与输入文件同目录)
  -t, --theme THEME         主题:tech/cyberpunk, clean/fresh, corporate
  -f, --footer TEXT         自定义页脚文本

分页控制:
  --split-level N           标题级别用于分页(1-6,默认:2)
  --viewport-height PX      视口高度,单位像素(默认:900)
  --content-threshold N     内容阈值,0-1 之间(默认:0.8)
  --max-content-length N    每页最大字符数(默认:800)
  --max-elements N          每页最大元素数(默认:15)
  --show-page-numbers       显示页码(如 "标题 (1/3)")

导航控制:
  --chapter-level N         进度条显示的标题级别(1-6,默认:2)
  --no-chapter-nav          禁用章节进度条

图片处理:
  --preserve-image-paths    保留原始图片路径(不拷贝)
  --no-copy-images          同上
```

### 使用示例

<details>
<summary><b>📝 基础转换</b></summary>

```bash
slidown lecture.md
# 输出:lecture_20260213143025/presentation.html
```

</details>

<details>
<summary><b>🎨 指定主题和输出目录</b></summary>

```bash
slidown notes.md -o ~/Desktop/presentation --theme clean
```

</details>

<details>
<summary><b>🏢 企业宣讲(带自定义页脚)</b></summary>

```bash
slidown pitch.md --theme corporate --footer "Confidential - © 2026 Company Inc."
```

</details>

<details>
<summary><b>⚙️ 调整分页和导航</b></summary>

```bash
# 使用 H1 标题分页,显示更多章节(H1-H3)
slidown doc.md --split-level 1 --chapter-level 3

# 调整页面高度和内容阈值
slidown doc.md --viewport-height 1080 --content-threshold 0.75
```

</details>

<details>
<summary><b>🖼️ 保留图片路径(不拷贝)</b></summary>

```bash
slidown article.md --preserve-image-paths
# HTML 可以直接放到 Markdown 同目录使用
```

</details>

<details>
<summary><b>📊 智能分页(自定义内容长度)</b></summary>

```bash
slidown long_tutorial.md --max-content-length 600 --max-elements 12
```

</details>

---

## ⚡ 高级功能

### LaTeX 数学公式

Slidown 完整支持 LaTeX 数学公式,使用 KaTeX 渲染:

**行内公式:**
```markdown
质能方程 $E=mc^2$ 是物理学的基础。
```

**块级公式:**
```markdown
$$
\int_{-\infty}^{\infty} e^{-x^2} dx = \sqrt{\pi}
$$
```

### 智能分页

- **自动检测内容长度** - 基于视口高度和内容阈值
- **保证无需滚动** - 每页内容不超过配置的最大高度
- **保护完整性** - 不切断代码块、公式、表格
- **可配置** - 通过 `--viewport-height` 和 `--content-threshold` 调整

**工作原理:**
1. 根据标题级别(`--split-level`)初步分页
2. 检测每页内容长度
3. 如果超过阈值,智能拆分为多个子页
4. 保护代码块、表格、公式等不被切断

### 图片处理

**默认模式(拷贝):**
```bash
slidown doc.md
# 图片拷贝到 doc_20260213143025/assets/images/
# 输出自包含的演示文稿,适合分享和归档
```

**路径保留模式:**
```bash
slidown doc.md --preserve-image-paths
# 保留 Markdown 中的原始路径
# 适合 HTML 与 Markdown 同目录使用
```

### 键盘快捷键

| 快捷键 | 操作 |
|--------|------|
| **→** 或 **空格** 或 **PageDown** | 下一页 |
| **←** 或 **PageUp** | 上一页 |
| **Home** | 跳转到第一页 |
| **End** | 跳转到最后一页 |
| **F11** | 全屏模式 |

---

## 🛠️ 技术实现

<table>
<tr>
<td>

**解析器**
- Python `markdown` 库
- 扩展:fenced_code、tables、toc、nl2br

**代码高亮**
- Pygments 语法高亮
- 支持 30+ 语言

**数学公式**
- KaTeX 渲染引擎
- CDN 交付

</td>
<td>

**样式**
- 三种内置主题
- CSS3 过渡和动画
- 响应式媒体查询

**导航**
- 纯 JavaScript 实现
- 无外部库依赖
- 触摸和键盘支持

</td>
</tr>
</table>

---

## 📋 支持的 Markdown 语法

- **标题**(H1-H6)
- **列表**(有序和无序)
- **代码块**(带语法高亮)
- **行内代码**
- **文本格式**(粗体、斜体、删除线)
- **链接**
- **图片**(本地和网络)
- **表格**
- **引用块**
- **水平分割线**
- **换行**
- **LaTeX 数学公式**(行内和块级)

---

## 💼 使用场景

<table>
<tr>
<td width="50%">

### 专业场景
- 企业宣讲
- 产品演示
- 季度报告
- 投资人演示
- 正式文档

</td>
<td width="50%">

### 技术场景
- 技术演讲
- 代码演示
- 架构讲解
- API 文档
- 教程材料

</td>
</tr>
<tr>
<td width="50%">

### 教育场景
- 教学课件
- 数学/科学讲座
- 学术演示
- 学生项目
- 培训课程

</td>
<td width="50%">

### 个人场景
- 博客可视化
- 笔记分享
- 个人知识库
- 作品集演示
- 创意项目

</td>
</tr>
</table>

---

## 🎯 为什么选择 Slidown?

### 相比传统 PowerPoint
- ✅ 无需安装软件
- ✅ 文件体积更小(纯文本 HTML)
- ✅ 易于版本控制(Git 友好)
- ✅ 内置代码语法高亮
- ✅ 支持 LaTeX 数学公式
- ✅ 响应式设计,适配各种设备
- ✅ 快速分享(浏览器直接打开)

### 相比在线工具(Google Slides、Notion)
- ✅ 完全离线可用
- ✅ 无需登录账号
- ✅ 隐私安全(本地存储)
- ✅ 加载速度快
- ✅ 自定义主题灵活

---

## ❓ 常见问题

<details>
<summary><b>生成的 HTML 文件可以离线使用吗?</b></summary>

可以。所有 CSS 和 JavaScript 都内联在 HTML 中。数学公式需要网络(KaTeX CDN),但可以下载 KaTeX 到本地使用。

</details>

<details>
<summary><b>支持数学公式吗?</b></summary>

完整支持!使用 `$...$`(行内)和 `$$...$$`(块级)语法,KaTeX 自动渲染。

</details>

<details>
<summary><b>如何自定义主题?</b></summary>

当前支持 3 种内置主题(tech、clean、corporate),可通过 `--theme` 参数选择。未来版本将支持自定义主题配置。

</details>

<details>
<summary><b>图片路径怎么处理?</b></summary>

默认模式下图片会自动拷贝到 `assets/images/` 目录。如果需要保留原始路径,使用 `--preserve-image-paths` 参数。

</details>

<details>
<summary><b>可以导出为 PDF 吗?</b></summary>

可以。在浏览器中打开 HTML 文件,使用"打印"功能,选择"另存为 PDF"。

</details>

<details>
<summary><b>支持哪些浏览器?</b></summary>

所有现代浏览器(Chrome、Firefox、Safari、Edge)。不支持 IE。

</details>

<details>
<summary><b>如何分享演示文稿?</b></summary>

三种方式:
1. 直接发送 HTML 文件(如果使用默认图片拷贝模式)
2. 压缩整个输出文件夹(包含 assets)
3. 上传到静态网站托管服务(GitHub Pages、Netlify 等)

</details>

---

## 🤝 贡献

欢迎贡献!请:

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建 Pull Request

**贡献方向:**
- 新增主题设计
- 改进智能分页算法
- 添加动画效果
- 优化性能
- 修复 Bug
- 完善文档

---

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

---

## 🔗 链接

- **GitHub 仓库**: [github.com/dwHou/slidown](https://github.com/dwHou/slidown)
- **问题反馈**: [Issues](https://github.com/dwHou/slidown/issues)
- **PyPI 包**: [pypi.org/project/slidown-md](https://pypi.org/project/slidown-md/)
- **更新日志**: [CHANGELOG.md](CHANGELOG.md)

---

<div align="center">

**Made with ❤️ by [Devonn Hou](https://github.com/dwHou)**

*Slidown = "Slide" (幻灯片) + "Markdown" (标记语言)*

将你的 Markdown 笔记转换为精美的演示文稿

</div>
