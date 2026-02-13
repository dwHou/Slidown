# 快速开始 - Slidown

5 分钟上手 Slidown，将 Markdown 转换为精美演示文稿

## 第 1 步：安装依赖

```bash
cd Slidown
pip install -r requirements.txt
```

只需要两个依赖包：
- `markdown` - Markdown 解析
- `Pygments` - 代码语法高亮

## 第 2 步：准备 Markdown 文件

创建一个简单的 Markdown 文件 `demo.md`：

```markdown
# 我的演示文稿

欢迎使用 Slidown

## 第一部分

- 要点 1
- 要点 2
- 要点 3

## 第二部分

### 代码示例

​```python
def hello():
    print("Hello, World!")
​```

## 总结

感谢观看！
```

## 第 3 步：转换为 HTML

```bash
python slidedown.py demo.md demo.html
```

## 第 4 步：在浏览器中打开

```bash
# macOS
open demo.html

# Linux
xdg-open demo.html

# Windows
start demo.html

# 或直接双击 demo.html 文件
```

## 基本操作

打开后使用以下快捷键：

- **→** 或 **空格**：下一页
- **←**：上一页
- **F11**：全屏模式
- **Home**：第一页
- **End**：最后一页

## 常用选项

### 更改分页规则

```bash
# H1 标题分页（每个 # 创建新幻灯片）
python slidedown.py demo.md demo.html --split-level 1

# H2 标题分页（每个 ## 创建新幻灯片，默认）
python slidedown.py demo.md demo.html --split-level 2

# H3 标题分页（每个 ### 创建新幻灯片）
python slidedown.py demo.md demo.html --split-level 3
```

### 选择主题

```bash
# Cyberpunk 科技风格（默认）
python slidedown.py demo.md demo.html --theme cyberpunk

# 亮色主题
python slidedown.py demo.md demo.html --theme light

# 暗色主题
python slidedown.py demo.md demo.html --theme dark

# 简洁主题
python slidedown.py demo.md demo.html --theme clean
```

## 完整示例

```bash
# 使用示例文件测试
python slidedown.py examples/example.md examples/output.html

# 在浏览器中打开
open examples/output.html
```

## 下一步

- 查看 [README.md](README.md) 了解完整功能
- 查看 [USAGE_GUIDE.md](USAGE_GUIDE.md) 了解高级用法
- 查看 [CHANGELOG.md](CHANGELOG.md) 了解版本历史

## 提示

1. 建议使用 H2 (##) 标题作为主要分页依据
2. 图片使用相对路径更方便分享
3. 代码块会自动应用语法高亮
4. 生成的 HTML 文件可以离线使用
5. 可以通过浏览器"打印为 PDF"导出

祝使用愉快！
