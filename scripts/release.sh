#!/bin/bash
# Slidown PyPI 发布脚本 / Slidown PyPI Release Script
# 自动化构建、测试和发布流程

set -e  # 遇到错误立即退出

# 颜色输出
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 项目根目录
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_DIR"

echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}▸ Slidown PyPI 发布工具${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# 检查是否有未提交的更改
if [[ -n $(git status -s) ]]; then
    echo -e "${RED}错误: 检测到未提交的更改${NC}"
    echo "请先提交所有更改再发布:"
    git status -s
    exit 1
fi

# 读取当前版本号
VERSION=$(grep '^version = ' pyproject.toml | sed 's/version = "\(.*\)"/\1/')
echo -e "当前版本: ${YELLOW}${VERSION}${NC}"
echo ""

# 确认发布
read -p "是否继续发布版本 ${VERSION} 到 PyPI? (y/N) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "已取消发布"
    exit 0
fi

echo ""
echo -e "${GREEN}▶ 步骤 1/7: 清理旧构建文件${NC}"
rm -rf build/ dist/ *.egg-info/
echo "✓ 清理完成"

echo ""
echo -e "${GREEN}▶ 步骤 2/7: 创建虚拟环境${NC}"
if [ ! -d ".venv_build" ]; then
    python3 -m venv .venv_build
    echo "✓ 虚拟环境已创建"
else
    echo "✓ 虚拟环境已存在"
fi

echo ""
echo -e "${GREEN}▶ 步骤 3/7: 安装构建工具${NC}"
source .venv_build/bin/activate
pip install --upgrade build setuptools wheel twine > /dev/null 2>&1
echo "✓ 构建工具已安装"

echo ""
echo -e "${GREEN}▶ 步骤 4/7: 构建发布包${NC}"
python -m build
echo "✓ 构建完成"

echo ""
echo -e "${GREEN}▶ 步骤 5/7: 验证包的完整性${NC}"
twine check dist/*
if [ $? -ne 0 ]; then
    echo -e "${RED}错误: 包验证失败${NC}"
    exit 1
fi
echo "✓ 验证通过"

echo ""
echo -e "${GREEN}▶ 步骤 6/7: 本地测试安装${NC}"
pip install --force-reinstall dist/slidown-${VERSION}-py3-none-any.whl > /dev/null 2>&1
if slidown --help > /dev/null 2>&1; then
    echo "✓ 本地安装测试通过"
else
    echo -e "${RED}错误: 本地安装测试失败${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}▶ 步骤 7/7: 上传到 PyPI${NC}"
echo ""
echo "请选择上传目标:"
echo "  1) TestPyPI (测试环境，推荐)"
echo "  2) PyPI (正式环境)"
echo "  3) 跳过上传（仅构建）"
echo ""
read -p "选择 (1/2/3): " -n 1 -r
echo

case $REPLY in
    1)
        echo ""
        echo -e "${YELLOW}上传到 TestPyPI...${NC}"
        twine upload --repository testpypi dist/*
        echo ""
        echo -e "${GREEN}✓ 已上传到 TestPyPI${NC}"
        echo -e "查看: ${YELLOW}https://test.pypi.org/project/slidown/${VERSION}/${NC}"
        echo ""
        echo "测试安装命令:"
        echo -e "${YELLOW}pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ slidown==${VERSION}${NC}"
        ;;
    2)
        echo ""
        read -p "确认上传到正式 PyPI? 此操作不可撤销 (y/N) " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "已取消上传"
            exit 0
        fi
        echo ""
        echo -e "${YELLOW}上传到正式 PyPI...${NC}"
        twine upload --repository pypi dist/*
        echo ""
        echo -e "${GREEN}✓ 已上传到正式 PyPI${NC}"
        echo -e "查看: ${YELLOW}https://pypi.org/project/slidown/${VERSION}/${NC}"
        echo ""
        echo "安装命令:"
        echo -e "${YELLOW}pip install slidown==${VERSION}${NC}"
        echo ""
        echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
        echo -e "${GREEN}🎉 发布成功！${NC}"
        echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
        echo ""
        echo "后续工作:"
        echo "  1. 创建 Git Tag:"
        echo -e "     ${YELLOW}git tag -a v${VERSION} -m \"Release version ${VERSION}\"${NC}"
        echo -e "     ${YELLOW}git push origin v${VERSION}${NC}"
        echo ""
        echo "  2. 在 GitHub 创建 Release"
        echo -e "     访问: ${YELLOW}https://github.com/dwHou/slidown/releases/new${NC}"
        echo ""
        echo "  3. 更新 README.md 添加 PyPI 安装说明"
        ;;
    3)
        echo ""
        echo -e "${YELLOW}已跳过上传${NC}"
        echo "构建产物位于: dist/"
        ;;
    *)
        echo ""
        echo "无效选择，已取消"
        exit 1
        ;;
esac

echo ""
echo -e "${GREEN}完成！${NC}"
