# Slidown

<div align="center">
  <h1 style="font-family: 'Orbitron', sans-serif; font-size: 3rem; letter-spacing: -1px;">
    <span style="font-weight: 700; color: #00D9FF; text-shadow: 0 0 10px rgba(0, 217, 255, 0.5);">Sli</span><span style="font-weight: 300; color: #555; padding: 0 0.2rem;">|</span><span style="font-weight: 300; color: #888888;">down</span>
  </h1>
</div>

**Transform Markdown into Beautiful HTML Presentations**
**将 Markdown 笔记优雅转换为网页版演示文稿**

---

## 特性

### 核心功能
- **Markdown 到 HTML** - 单文件输出，所有 CSS/JS 内联，无外部依赖
- **三种精美主题** - Tech/Cyberpunk、Clean/Fresh、Corporate
- **响应式设计** - 完美适配桌面、平板、手机
- **智能分页** - 自动调整内容，基于视口高度和内容阈值，无需滚动
- **双层导航系统** - 章节进度条（底部）+ 可展开目录面板（左上角）
- **LaTeX 数学公式** - 完整支持行内公式 `$...$` 和块级公式 `$$...$$`，KaTeX 渲染
- **代码高亮** - Pygments 支持，30+ 编程语言
- **极速加载** - 轻量级单文件，本地即可运行
- **灵活图片处理** - 自动拷贝或保留原始路径

### 导航系统
- **章节进度条**（底部）- 显示主要章节（默认 H1-H2），支持快速跳转
- **目录面板**（左上角）- 完整文档大纲（H1-H5），点击展开/收起
- **键盘导航** - 方向键、空格、Home/End 快捷键

### 图片处理
- **默认模式** - 自动拷贝图片到 `assets/images/` 目录
- **路径保留模式** - 使用 `--preserve-image-paths` 保留原始路径（适合 HTML 与 Markdown 同目录）

---

## 快速开始

### 安装依赖

```bash
pip install markdown pygments
```

或使用 requirements.txt：

```bash
pip install -r requirements.txt
```

依赖项：
- `markdown>=3.4.1` - Markdown 解析
- `Pygments>=2.15.0` - 代码语法高亮

### 基本使用

```bash
# 克隆仓库
git clone https://github.com/dwHou/slidown.git
cd Slidown

# 转换 Markdown 文档（自动生成时间戳输出文件夹）
python slidown.py your_notes.md

# 使用指定主题
python slidown.py your_notes.md --theme clean

# 添加自定义页脚
python slidown.py your_notes.md --theme corporate --footer "© 2026 Your Name"
```

### 输出结果

```
your_notes_20260213143025/
├── presentation.html          # 主演示文稿（单文件，所有资源内联）
├── assets/
│   └── images/               # 图片资源（如果使用默认拷贝模式）
└── README.txt                # 使用说明
```

在浏览器中打开 `presentation.html` 即可查看演示文稿。

---

## 主题

### Tech / Cyberpunk（默认）
- 深色背景 + 霓虹色（青色、蓝色、绿色）
- 网格背景效果
- 适合技术演讲、编程教程、产品发布

```bash
python slidown.py document.md --theme tech
```

### Clean / Fresh
- 明亮白色背景
- 柔和配色，清爽简约
- 适合文档、教学讲义、学术演示

```bash
python slidown.py document.md --theme clean
```

### Corporate
- 专业商务风格
- 深蓝/灰色配色
- 适合企业宣讲、正式报告、投资人演示

```bash
python slidown.py document.md --theme corporate
```

---

## 使用指南

### 命令行参数

```bash
python slidown.py INPUT [OPTIONS]

必需参数:
  INPUT                     输入 Markdown 文件路径

输出选项:
  -o, --output DIR          输出基础目录（默认：Markdown 文件同级目录）
                            会在此目录下创建时间戳文件夹
  -t, --theme THEME         主题：tech/cyberpunk, clean/fresh, corporate
                            默认：tech
  -f, --footer TEXT         自定义页脚文本

分页控制:
  --split-level N           标题级别用于分页（1-6，默认：2 = H2）
  --viewport-height PX      视口高度，单位像素（默认：900）
  --content-threshold N     内容阈值，0-1 之间（默认：0.8 = 80%）
  --max-content-length N    每页最大字符数（默认：800）
  --max-elements N          每页最大元素数（默认：15）
  --show-page-numbers       显示页码（如 "标题 (1/3)"）

导航控制:
  --chapter-level N         进度条显示的标题级别（1-6，默认：2 = H2）
  --no-chapter-nav          禁用章节进度条

图片处理:
  --preserve-image-paths    保留原始图片路径（不拷贝到 assets）
  --no-copy-images          同上
```

### 使用示例

#### 1. 基础转换
```bash
python slidown.py lecture.md
# 输出：lecture_20260213143025/presentation.html
```

#### 2. 指定主题和输出目录
```bash
python slidown.py notes.md -o ~/Desktop/presentation --theme clean
```

#### 3. 企业宣讲（带自定义页脚）
```bash
python slidown.py pitch.md --theme corporate --footer "Confidential - © 2026 Company Inc."
```

#### 4. 调整分页和导航
```bash
# 使用 H1 标题分页，显示更多章节（H1-H3）
python slidown.py doc.md --split-level 1 --chapter-level 3

# 调整页面高度和内容阈值
python slidown.py doc.md --viewport-height 1080 --content-threshold 0.75
```

#### 5. 保留图片路径（不拷贝）
```bash
python slidown.py article.md --preserve-image-paths
# HTML 可以直接放到 Markdown 同目录使用
```

#### 6. 智能分页（自定义内容长度）
```bash
python slidown.py long_tutorial.md --max-content-length 600 --max-elements 12
```

---

## LaTeX 数学公式

Slidown 完整支持 LaTeX 数学公式，使用 KaTeX 渲染：

**行内公式：**
```markdown
质能方程 $E=mc^2$ 是物理学的基础。
```

**块级公式：**
```markdown
$$
\int_{-\infty}^{\infty} e^{-x^2} dx = \sqrt{\pi}
$$
```

**示例效果：**
- 行内：质能方程 $E=mc^2$ 是物理学的基础
- 块级：高斯积分公式

$$
\int_{-\infty}^{\infty} e^{-x^2} dx = \sqrt{\pi}
$$

---

## 导航系统

### 章节进度条（底部）
- 显示主要章节（默认 H1-H2）
- 高亮当前位置
- 点击章节名称快速跳转
- 可通过 `--chapter-level` 配置显示级别

### 目录面板（左上角）
- 显示完整文档大纲（H1-H5）
- 层次缩进清晰
- 点击目录图标展开/收起
- 支持精确跳转到任意标题

### 键盘快捷键
- **→** 或 **空格** 或 **PageDown** - 下一页
- **←** 或 **PageUp** - 上一页
- **Home** - 跳转到第一页
- **End** - 跳转到最后一页
- **F11** - 全屏模式

### 触摸/鼠标导航
- 左滑或点击右侧 - 下一页
- 右滑或点击左侧 - 上一页

---

## 高级功能

### 智能分页
- **自动检测内容长度** - 基于视口高度和内容阈值
- **保证无需滚动** - 每页内容不超过配置的最大高度
- **保护完整性** - 不切断代码块、公式、表格
- **可配置** - 通过 `--viewport-height` 和 `--content-threshold` 调整

**工作原理：**
1. 根据标题级别（`--split-level`）初步分页
2. 检测每页内容长度
3. 如果超过阈值，智能拆分为多个子页
4. 保护代码块、表格、公式等不被切断

### 图片处理

**默认模式（拷贝）：**
```bash
python slidown.py doc.md
# 图片拷贝到 doc_20260213143025/assets/images/
# 输出自包含的演示文稿，适合分享和归档
```

**路径保留模式：**
```bash
python slidown.py doc.md --preserve-image-paths
# 保留 Markdown 中的原始路径
# 不拷贝图片文件
# 适合 HTML 与 Markdown 同目录使用
```

### 自定义页脚
```bash
python slidown.py doc.md --footer "© 2026 Your Company - Confidential"
# 页脚居中显示，半透明背景，所有页面统一
```

### 章节级别配置
```bash
# 进度条显示 H1-H3（更详细的章节）
python slidown.py doc.md --chapter-level 3

# 进度条仅显示 H1（顶级章节）
python slidown.py doc.md --chapter-level 1
```

---

## 支持的 Markdown 语法

- **标题**（H1-H6）
- **有序列表和无序列表**
- **代码块**（带语法高亮，支持 30+ 语言）
- **行内代码**
- **粗体、斜体、删除线**
- **链接**
- **图片**（本地和网络图片）
- **表格**
- **引用块**
- **水平分割线**
- **换行**
- **LaTeX 数学公式**（行内和块级）

---

## 项目结构

```
Slidown/
├── README.md              # 使用说明（本文件）
├── QUICKSTART.md          # 快速开始指南
├── USAGE_GUIDE.md         # 详细使用指南
├── CHANGELOG.md           # 版本历史
├── requirements.txt       # Python 依赖
├── slidown.py             # 主程序（Markdown 转 HTML）
├── examples/              # 示例文件
├── docs/                  # 官方网站
│   └── index.html         # 项目主页
├── templates/             # 主题模板（内部）
└── utils/                 # 工具模块
```

---

## 技术实现

- **解析器** - Python `markdown` 库，支持扩展（fenced_code、tables、toc、nl2br）
- **代码高亮** - `Pygments` 语法高亮
- **数学公式** - KaTeX 渲染引擎（CDN）
- **样式** - 三种主题（Tech、Clean、Corporate）
- **导航** - 纯 JavaScript 实现，无外部库依赖
- **动画** - CSS3 过渡和关键帧动画
- **响应式** - 媒体查询适配移动端

---

## 使用场景

- **技术演讲** - 代码演示、架构讲解
- **教学课件** - 数学公式、图表展示
- **项目汇报** - 进度展示、数据分析
- **文档演示** - API 文档、用户指南
- **博客分享** - 技术文章可视化
- **企业宣讲** - 产品介绍、季度报告

---

## 优势

**相比传统 PowerPoint：**
- 无需安装 Office 软件
- 文件体积更小（纯文本 HTML）
- 易于版本控制（Git 友好）
- 支持代码语法高亮
- 支持 LaTeX 数学公式
- 响应式设计，适配各种设备
- 快速分享（浏览器直接打开）

**相比在线工具（Google Slides、Notion）：**
- 完全离线可用
- 无需登录账号
- 隐私安全（本地存储）
- 加载速度快
- 自定义主题灵活

---

## 常见问题

**Q: 生成的 HTML 文件可以离线使用吗？**
A: 可以。所有 CSS 和 JavaScript 都内联在 HTML 中。数学公式需要网络（KaTeX CDN），但可以下载 KaTeX 到本地使用。

**Q: 支持数学公式吗？**
A: 完整支持！使用 `$...$`（行内）和 `$$...$$`（块级）语法，KaTeX 自动渲染。

**Q: 如何自定义主题？**
A: 当前支持 3 种内置主题（tech、clean、corporate），可通过 `--theme` 参数选择。未来版本将支持自定义主题配置。

**Q: 图片路径怎么处理？**
A: 默认模式下图片会自动拷贝到 `assets/images/` 目录。如果需要保留原始路径，使用 `--preserve-image-paths` 参数。

**Q: 可以导出为 PDF 吗？**
A: 可以。在浏览器中打开 HTML 文件，使用"打印"功能，选择"另存为 PDF"。

**Q: 支持哪些浏览器？**
A: 所有现代浏览器（Chrome、Firefox、Safari、Edge）。不支持 IE。

**Q: 如何分享演示文稿？**
A: 三种方式：
  1. 直接发送 HTML 文件（如果使用默认图片拷贝模式）
  2. 压缩整个输出文件夹（包含 assets）
  3. 上传到静态网站托管服务（GitHub Pages、Netlify 等）

---

## 贡献

欢迎贡献！请：
1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建 Pull Request

**贡献方向：**
- 新增主题设计
- 改进智能分页算法
- 添加动画效果
- 优化性能
- 修复 Bug
- 完善文档

---

## 许可证

MIT License - 详见 LICENSE 文件

---

## 项目说明

**Slidown** = "Slide" (幻灯片) + "Markdown" (标记语言)

本项目专注于将 Markdown 文档转换为精美的 HTML 格式网页演示文稿，让技术内容展示更加优雅和专业。

### Logo 设计

Slidown 采用纯 CSS 实现的 Logo 设计，无需任何图片文件：

```html
<div class="logo">
  <span class="logo-sli">Sli</span><span class="logo-separator">|</span><span class="logo-down">down</span>
</div>
```

**设计理念：**
- **Sli** - 粗体青色 (#00D9FF)，带发光效果 - 代表转换和技术
- **|** - 细体灰色分隔符 - 连接两种格式
- **down** - 细体灰色 (#888888) - 代表 Markdown 基础

完整的 CSS 实现和官方网站请访问 `docs/index.html`

---

## 链接

- **项目主页**: [GitHub Repository](https://github.com/dwHou/slidown)
- **问题反馈**: [Issues](https://github.com/dwHou/slidown/issues)
- **官方网站**: [docs/index.html](docs/index.html)
- **更新日志**: [CHANGELOG.md](CHANGELOG.md)

---

**Made with love by Devonn Hou**
