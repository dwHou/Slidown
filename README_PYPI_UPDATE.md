# README.md 更新建议

在 README.md 的 "快速开始" 部分，将现有的安装说明替换为以下内容：

---

## 快速开始

### 安装

#### 方法 1: 从 PyPI 安装（推荐）

```bash
pip install slidown
```

#### 方法 2: 从源码安装

```bash
# 克隆仓库
git clone https://github.com/dwHou/slidown.git
cd Slidown

# 安装依赖
pip install -r requirements.txt

# 或者直接安装包
pip install .
```

### 基本使用

安装后，可以直接使用 `slidown` 命令：

```bash
# 转换 Markdown 文档（自动生成时间戳输出文件夹）
slidown your_notes.md

# 使用指定主题
slidown your_notes.md --theme clean

# 添加自定义页脚
slidown your_notes.md --theme corporate --footer "© 2026 Your Name"
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

## 注意事项

1. 将上述内容替换到 README.md 的第 38-72 行（"快速开始"部分）
2. 删除原有的 `python slidown.py` 命令示例
3. 将所有命令从 `python slidown.py` 改为 `slidown`
4. 保留其他章节不变（主题、使用指南、LaTeX 等）
