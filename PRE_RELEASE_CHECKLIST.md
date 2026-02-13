# PyPI 发布前检查清单

在发布到 PyPI 之前，请确保完成以下所有检查项。

---

## ✅ 代码质量检查

- [ ] 所有功能测试通过
- [ ] 没有已知的严重 bug
- [ ] 代码已经过审查
- [ ] 所有 TODO 和 FIXME 注释已处理

## ✅ 文档检查

- [ ] README.md 内容完整且准确
  - [ ] 安装说明正确
  - [ ] 使用示例可运行
  - [ ] 功能描述准确
  - [ ] 链接有效
- [ ] CHANGELOG.md 已更新当前版本的变更
- [ ] LICENSE 文件存在且正确
- [ ] 所有文档中的版本号一致

## ✅ 配置文件检查

- [ ] `pyproject.toml` 配置正确
  - [x] 版本号正确: `1.0.0`
  - [x] 作者信息完整
  - [x] 依赖项准确
  - [x] 分类器适当
  - [x] 项目 URL 正确
  - [ ] 作者邮箱已更新（当前为占位符）
- [ ] `MANIFEST.in` 包含所有必要文件
- [ ] `.gitignore` 排除构建产物

## ✅ 包结构检查

- [x] 主模块 `slidown.py` 存在且功能正常
- [x] `utils/` 子包完整
  - [x] `__init__.py`
  - [x] `theme.py`
  - [x] `parser.py`
  - [x] `code_highlight.py`
- [x] 命令行入口点 `slidown:main` 正确配置
- [x] 依赖包声明完整

## ✅ 构建和测试

- [x] 构建成功: `python -m build`
- [x] 元数据验证通过: `twine check dist/*`
- [x] 本地安装测试通过
- [x] 命令行工具可用: `slidown --help`
- [x] 功能测试通过（使用 `test_package.sh`）

## ✅ 版本管理

- [ ] Git 工作区干净（无未提交更改）
- [ ] 版本号遵循语义化版本规范
- [ ] CHANGELOG.md 记录了此版本的所有变更
- [ ] 版本号在以下文件中一致：
  - [ ] `pyproject.toml`
  - [ ] CHANGELOG.md
  - [ ] （可选）代码中的 `__version__`

## ✅ 发布准备

### PyPI 账户设置

- [ ] 已注册 PyPI 账户: https://pypi.org/account/register/
- [ ] 已注册 TestPyPI 账户: https://test.pypi.org/account/register/
- [ ] 已创建 PyPI API Token
- [ ] 已创建 TestPyPI API Token
- [ ] 已配置 `~/.pypirc` 文件
- [ ] `~/.pypirc` 文件权限设置为 600

### 发布测试

- [ ] 已上传到 TestPyPI 并验证
- [ ] 从 TestPyPI 安装测试成功
- [ ] TestPyPI 页面显示正常

## ✅ 最终检查

- [ ] 确认包名 `slidown` 在 PyPI 上可用（或已拥有）
- [ ] 确认此版本号未在 PyPI 发布过
- [ ] 准备好回滚方案（如需要）
- [ ] 通知团队即将发布（如适用）

---

## 🚀 执行发布

完成所有检查后，执行发布：

### 方式 1: 使用发布脚本（推荐）

```bash
./scripts/release.sh
```

### 方式 2: 手动发布

```bash
# 1. 清理旧构建
rm -rf build/ dist/ *.egg-info/

# 2. 构建包
python -m build

# 3. 验证
twine check dist/*

# 4. 上传到 TestPyPI
twine upload --repository testpypi dist/*

# 5. 测试安装
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ slidown

# 6. 确认无误后，上传到正式 PyPI
twine upload dist/*
```

---

## 📝 发布后任务

- [ ] 创建 Git Tag
  ```bash
  git tag -a v1.0.0 -m "Release version 1.0.0"
  git push origin v1.0.0
  ```

- [ ] 在 GitHub 创建 Release
  - 访问: https://github.com/dwHou/slidown/releases/new
  - 选择刚创建的 tag
  - 填写 Release notes
  - 上传 `dist/*.whl` 和 `dist/*.tar.gz`

- [ ] 更新 README.md
  - 添加 PyPI 安装说明
  - 添加 PyPI 徽章（可选）
    ```markdown
    ![PyPI](https://img.shields.io/pypi/v/slidown)
    ![Python Version](https://img.shields.io/pypi/pyversions/slidown)
    ```

- [ ] 验证正式安装
  ```bash
  pip install slidown
  slidown --help
  ```

- [ ] 宣布发布
  - 更新项目主页
  - 发布社区公告（如适用）
  - 更新相关文档和链接

---

## ⚠️ 常见问题

### 版本号已存在

如果上传时提示版本号已存在，需要：
1. 更新 `pyproject.toml` 中的版本号
2. 更新 CHANGELOG.md
3. 重新构建和上传

### 包名已被占用

如果包名 `slidown` 已被占用，需要：
1. 选择新的包名（如 `slidown-converter`）
2. 更新 `pyproject.toml` 中的 `name`
3. 更新所有文档中的包名

### 依赖问题

如果用户安装时遇到依赖问题：
1. 检查 `pyproject.toml` 中的依赖版本范围
2. 考虑放宽版本限制（如 `>=3.4.1` 而不是 `==3.4.1`）
3. 发布修复版本（如 1.0.1）

---

**当前状态**:
- ✅ 包已构建
- ✅ 所有测试通过
- ⏳ 等待发布到 PyPI

**下一步**: 使用 `./scripts/release.sh` 或手动上传到 PyPI
