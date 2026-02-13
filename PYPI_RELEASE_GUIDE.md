# PyPI 发布指南 / PyPI Release Guide

本文档说明如何将 Slidown 发布到 PyPI（Python Package Index）。

---

## 准备工作

### 1. 注册 PyPI 账户

如果还没有 PyPI 账户，需要先注册：

- **正式 PyPI**: https://pypi.org/account/register/
- **测试 PyPI** (推荐先测试): https://test.pypi.org/account/register/

### 2. 配置 API Token

为了安全上传包，建议使用 API Token 而不是密码：

1. 登录 PyPI 账户
2. 进入 Account Settings → API tokens
3. 点击 "Add API token"
4. 选择 Scope (建议先选择特定项目，或者 "Entire account")
5. 复制生成的 token（格式：`pypi-AgEIcHlwaS5vcmc...`）

### 3. 配置 `.pypirc` 文件

在用户主目录创建 `~/.pypirc` 文件：

```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = pypi-AgEIcHlwaS5vcmc...  # 替换为你的 API token

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-AgEIcHlwaS5vcmc...  # 替换为测试环境的 API token
```

**重要**: 保护好这个文件的权限：
```bash
chmod 600 ~/.pypirc
```

---

## 发布流程

### 第 1 步：准备虚拟环境

```bash
cd /Applications/Programming/code/GitProj/Slidown

# 创建虚拟环境（如果还没创建）
python3 -m venv .venv_build

# 激活虚拟环境
source .venv_build/bin/activate

# 安装构建工具
pip install --upgrade build setuptools wheel twine
```

### 第 2 步：清理旧构建文件

```bash
# 删除旧的构建产物
rm -rf build/ dist/ *.egg-info/

# 验证清理完成
ls -la
```

### 第 3 步：更新版本号

编辑 `pyproject.toml` 文件，更新版本号：

```toml
[project]
name = "slidown"
version = "1.0.0"  # 修改为新版本号，如 1.0.1, 1.1.0 等
...
```

**版本号规范** (遵循 Semantic Versioning):
- **主版本号** (Major): 不兼容的 API 变更
- **次版本号** (Minor): 向后兼容的功能新增
- **修订号** (Patch): 向后兼容的问题修复

### 第 4 步：构建发布包

```bash
# 确保在虚拟环境中
source .venv_build/bin/activate

# 构建 wheel 和 source distribution
python -m build

# 验证生成的文件
ls -lh dist/
# 应该看到:
# slidown-1.0.0-py3-none-any.whl
# slidown-1.0.0.tar.gz
```

### 第 5 步：验证包的完整性

```bash
# 检查包的元数据
twine check dist/*

# 输出应该为:
# Checking dist/slidown-1.0.0-py3-none-any.whl: PASSED
# Checking dist/slidown-1.0.0.tar.gz: PASSED
```

### 第 6 步：查看包内容（可选）

```bash
# 查看 wheel 包内容
python -m zipfile -l dist/slidown-1.0.0-py3-none-any.whl

# 查看 tar.gz 包内容
tar -tzf dist/slidown-1.0.0.tar.gz
```

### 第 7 步：本地测试安装

```bash
# 在虚拟环境中测试安装
pip install dist/slidown-1.0.0-py3-none-any.whl

# 验证命令可用
slidown --help

# 测试功能（如果有示例文件）
slidown examples/README.md --theme tech
```

### 第 8 步：上传到测试 PyPI（推荐）

先上传到测试环境验证：

```bash
# 上传到 TestPyPI
twine upload --repository testpypi dist/*

# 输入用户名: __token__
# 输入密码: 你的 TestPyPI API token
```

上传成功后访问: https://test.pypi.org/project/slidown/

### 第 9 步：从测试 PyPI 安装测试

```bash
# 创建新的测试环境
python3 -m venv test_env
source test_env/bin/activate

# 从 TestPyPI 安装
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ slidown

# 验证安装
slidown --help
```

**注意**: 使用 `--extra-index-url` 是因为依赖包（markdown, Pygments）在正式 PyPI 上。

### 第 10 步：上传到正式 PyPI

确认测试无误后，上传到正式 PyPI：

```bash
# 上传到正式 PyPI
twine upload dist/*

# 或者如果已配置 .pypirc
twine upload --repository pypi dist/*
```

上传成功后访问: https://pypi.org/project/slidown/

### 第 11 步：验证正式发布

```bash
# 创建新环境测试
python3 -m venv final_test
source final_test/bin/activate

# 从正式 PyPI 安装
pip install slidown

# 验证功能
slidown --help
python -c "import slidown; print(slidown.__file__)"
```

---

## 发布后的工作

### 1. 创建 Git Tag

```bash
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0
```

### 2. 创建 GitHub Release

1. 访问 GitHub 仓库
2. 点击 "Releases" → "Create a new release"
3. 选择刚创建的 tag (v1.0.0)
4. 填写 Release notes（从 CHANGELOG.md 复制）
5. 上传构建好的 `dist/*.whl` 和 `dist/*.tar.gz` 文件

### 3. 更新 README.md

在 README.md 中添加 PyPI 安装说明：

```markdown
## 安装

### 从 PyPI 安装（推荐）

```bash
pip install slidown
```

### 从源码安装

```bash
git clone https://github.com/dwHou/slidown.git
cd Slidown
pip install .
```
```

---

## 常见问题

### Q: 上传时提示 "File already exists"

**原因**: PyPI 不允许覆盖已上传的版本。

**解决方案**:
1. 更新 `pyproject.toml` 中的版本号
2. 重新构建: `python -m build`
3. 重新上传新版本

### Q: 如何撤回已发布的版本？

PyPI 不允许删除已发布的版本（保证依赖稳定性），但可以：

1. 使用 "yank" 功能隐藏版本（不会破坏现有安装）：
   ```bash
   # 在 PyPI 网站操作，或使用 API
   ```
2. 发布新的修复版本（如 1.0.1）

### Q: 如何测试不同 Python 版本的兼容性？

使用 `tox` 或 `nox` 进行多版本测试：

```bash
pip install tox

# 创建 tox.ini 配置测试 Python 3.8-3.12
tox
```

### Q: 包太大怎么办？

检查是否包含了不必要的文件：

```bash
# 查看包内容
tar -tzf dist/slidown-1.0.0.tar.gz

# 在 MANIFEST.in 中排除不需要的文件
# 在 .gitignore 和 pyproject.toml 中配置
```

---

## 最佳实践

1. **版本管理**: 遵循语义化版本规范 (Semantic Versioning)
2. **变更日志**: 在 CHANGELOG.md 中记录每个版本的变更
3. **测试优先**: 总是先上传到 TestPyPI 测试
4. **API Token**: 使用 API Token 而不是密码
5. **自动化**: 考虑使用 GitHub Actions 自动化发布流程
6. **文档同步**: 确保 README.md、文档和代码版本一致

---

## 自动化发布（可选）

使用 GitHub Actions 自动化发布流程：

创建 `.github/workflows/publish.yml`:

```yaml
name: Publish to PyPI

on:
  release:
    types: [created]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - uses: actions/setup-python@v4
      with:
        python-version: '3.x'
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install build twine
    - name: Build package
      run: python -m build
    - name: Publish to PyPI
      env:
        TWINE_USERNAME: __token__
        TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
      run: twine upload dist/*
```

在 GitHub 仓库设置中添加 Secret: `PYPI_API_TOKEN`

---

## 参考资源

- [Python Packaging User Guide](https://packaging.python.org/)
- [PyPI Help](https://pypi.org/help/)
- [Semantic Versioning](https://semver.org/)
- [Twine Documentation](https://twine.readthedocs.io/)

---

**最后更新**: 2026-02-13
**维护者**: Devonn Hou
