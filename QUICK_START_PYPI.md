# PyPI 发布快速指南

> 5 分钟内完成 Slidown 发布到 PyPI

---

## 前提条件

- [x] 包已构建并测试完成
- [x] Git 工作区已提交
- [ ] 拥有 PyPI 账户和 API Token

---

## 发布步骤

### 步骤 1: 获取 API Token (首次)

如果还没有 PyPI API Token:

1. **测试环境** (推荐先测试):
   - 访问: https://test.pypi.org/manage/account/token/
   - 创建 token，命名为 `slidown-upload`

2. **正式环境**:
   - 访问: https://pypi.org/manage/account/token/
   - 创建 token，命名为 `slidown-upload`

### 步骤 2: 运行发布脚本

```bash
cd /Applications/Programming/code/GitProj/Slidown
./scripts/release.sh
```

脚本会自动：
- ✅ 清理旧文件
- ✅ 构建新包
- ✅ 验证完整性
- ✅ 测试安装
- ⏳ 提示上传选择

### 步骤 3: 选择上传目标

脚本会询问上传到：
1. **TestPyPI** (测试环境) - 推荐首次发布先选这个
2. **PyPI** (正式环境) - 测试通过后选这个
3. **跳过上传** (仅构建)

### 步骤 4: 输入凭据

- Username: `__token__`
- Password: 粘贴你的 API Token

### 步骤 5: 验证发布

**TestPyPI**:
```bash
# 查看项目页面
open https://test.pypi.org/project/slidown/

# 测试安装
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ slidown
slidown --help
```

**正式 PyPI**:
```bash
# 查看项目页面
open https://pypi.org/project/slidown/

# 测试安装
pip install slidown
slidown --help
```

---

## 发布后任务

### 1. 创建 Git Tag

```bash
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0
```

### 2. 创建 GitHub Release

```bash
# 直接在浏览器中操作
open https://github.com/dwHou/slidown/releases/new
```

选择刚创建的 tag `v1.0.0`，上传 `dist/` 中的文件。

### 3. 更新 README.md

参考 `README_PYPI_UPDATE.md` 更新安装说明。

---

## 故障排除

### 问题: "File already exists"

**解决**: 版本号已存在，更新 `pyproject.toml` 中的版本号后重新构建。

### 问题: "Invalid or non-existent authentication"

**解决**:
1. 确认 Username 是 `__token__`（不是你的用户名）
2. 确认 Token 完整复制（包括 `pypi-` 前缀）
3. 确认使用了正确环境的 Token (TestPyPI vs PyPI)

### 问题: 包名冲突

**解决**: 如果 `slidown` 已被占用，修改 `pyproject.toml` 中的 `name` 字段。

---

## 完整文档

需要更多细节？查看：
- **详细指南**: `PYPI_RELEASE_GUIDE.md`
- **检查清单**: `PRE_RELEASE_CHECKLIST.md`
- **发布摘要**: `RELEASE_SUMMARY.md`

---

**准备好了吗？运行 `./scripts/release.sh` 开始发布！** 🚀
