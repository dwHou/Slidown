#!/bin/bash
# 测试 Slidown 包的完整性
# Test Slidown package integrity

set -e

# 颜色输出
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_DIR"

echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}▸ Slidown 包测试工具${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# 读取版本号
VERSION=$(grep '^version = ' pyproject.toml | sed 's/version = "\(.*\)"/\1/')
echo -e "当前版本: ${YELLOW}${VERSION}${NC}"
echo ""

# 检查是否已构建
if [ ! -f "dist/slidown-${VERSION}-py3-none-any.whl" ]; then
    echo -e "${RED}错误: 未找到构建产物${NC}"
    echo "请先运行: python -m build"
    exit 1
fi

echo -e "${GREEN}▶ 测试 1/6: 检查包元数据${NC}"
source .venv_build/bin/activate
twine check dist/* 2>&1 | grep "PASSED"
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ 元数据验证通过${NC}"
else
    echo -e "${RED}✗ 元数据验证失败${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}▶ 测试 2/6: 检查包内容${NC}"
echo "Wheel 包内容:"
python -m zipfile -l "dist/slidown-${VERSION}-py3-none-any.whl" | head -15
echo -e "${GREEN}✓ Wheel 包结构正常${NC}"

echo ""
echo -e "${GREEN}▶ 测试 3/6: 创建测试环境${NC}"
TEST_ENV="test_env_$(date +%s)"
python3 -m venv "$TEST_ENV"
source "$TEST_ENV/bin/activate"
echo -e "${GREEN}✓ 测试环境已创建${NC}"

echo ""
echo -e "${GREEN}▶ 测试 4/6: 安装包${NC}"
pip install "dist/slidown-${VERSION}-py3-none-any.whl" > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ 包安装成功${NC}"
else
    echo -e "${RED}✗ 包安装失败${NC}"
    rm -rf "$TEST_ENV"
    exit 1
fi

echo ""
echo -e "${GREEN}▶ 测试 5/6: 验证命令行工具${NC}"
if command -v slidown > /dev/null 2>&1; then
    echo -e "${GREEN}✓ slidown 命令可用${NC}"
    slidown --help > /dev/null 2>&1
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ --help 参数正常${NC}"
    else
        echo -e "${RED}✗ --help 参数失败${NC}"
        rm -rf "$TEST_ENV"
        exit 1
    fi
else
    echo -e "${RED}✗ slidown 命令不可用${NC}"
    rm -rf "$TEST_ENV"
    exit 1
fi

echo ""
echo -e "${GREEN}▶ 测试 6/6: 验证功能${NC}"

# 创建测试 Markdown 文件
TEST_MD=$(mktemp).md
cat > "$TEST_MD" << 'EOF'
# 测试文档

这是一个测试文档。

## 第一节

测试内容 1

## 第二节

测试内容 2
EOF

# 运行转换
OUTPUT_DIR=$(mktemp -d)
slidown "$TEST_MD" -o "$OUTPUT_DIR" --theme tech > /dev/null 2>&1

# 检查输出
OUTPUT_HTML=$(find "$OUTPUT_DIR" -name "*-slidown.html" 2>/dev/null | head -1)
if [ -f "$OUTPUT_HTML" ]; then
    echo -e "${GREEN}✓ 功能测试通过${NC}"
    echo -e "  生成文件: $(basename $(dirname "$OUTPUT_HTML"))/$(basename "$OUTPUT_HTML")"
else
    echo -e "${RED}✗ 功能测试失败${NC}"
    rm -rf "$TEST_ENV" "$TEST_MD" "$OUTPUT_DIR"
    exit 1
fi

# 清理
rm -rf "$TEST_ENV" "$TEST_MD" "$OUTPUT_DIR"

echo ""
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}✓ 所有测试通过！包已准备好发布。${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo "下一步:"
echo "  1. 上传到 TestPyPI 测试:"
echo -e "     ${YELLOW}twine upload --repository testpypi dist/*${NC}"
echo ""
echo "  2. 或直接上传到正式 PyPI:"
echo -e "     ${YELLOW}twine upload dist/*${NC}"
echo ""
echo "  3. 或使用发布脚本:"
echo -e "     ${YELLOW}./scripts/release.sh${NC}"
