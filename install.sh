#!/bin/bash
set -e

echo "========================================="
echo "  Meta AI SDK - Skill Installer"
echo "========================================="
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$HOME/.claude/skills/metaai"

# Step 1: Install Python dependencies
echo -e "${YELLOW}[1/4] Installing Python dependencies...${NC}"
pip3 install metaai-api requests python-dotenv 2>/dev/null || pip install metaai-api requests python-dotenv 2>/dev/null
echo -e "${GREEN}  ✓ Dependencies installed${NC}"

# Step 2: Create skill directory
echo -e "${YELLOW}[2/4] Setting up skill directory...${NC}"
mkdir -p "$SKILL_DIR"
cp "$SCRIPT_DIR/skill/SKILL.md" "$SKILL_DIR/SKILL.md"
cp "$SCRIPT_DIR/skill/metaai_generate.py" "$SKILL_DIR/metaai_generate.py"
chmod +x "$SKILL_DIR/metaai_generate.py"
echo -e "${GREEN}  ✓ Skill files installed to $SKILL_DIR${NC}"

# Step 3: Create .env.metaai if not exists
echo -e "${YELLOW}[3/4] Checking configuration...${NC}"
if [ ! -f "$SKILL_DIR/.env.metaai" ]; then
    cp "$SCRIPT_DIR/.env.example" "$SKILL_DIR/.env.metaai"
    echo -e "${YELLOW}  ⚠ Created .env.metaai — EDIT THIS FILE with your cookies!${NC}"
    echo -e "${YELLOW}  → Open $SKILL_DIR/.env.metaai in your editor${NC}"
else
    echo -e "${GREEN}  ✓ .env.metaai already exists, skipping${NC}"
fi

# Step 4: Open docs
echo -e "${YELLOW}[4/4] Opening documentation...${NC}"
open "$SCRIPT_DIR/docs/index.html"
echo -e "${GREEN}  ✓ Documentation opened in browser${NC}"

echo ""
echo "========================================="
echo -e "${GREEN}  Installation complete!${NC}"
echo "========================================="
echo ""
echo "Next steps:"
echo "  1. Edit $SKILL_DIR/.env.metaai with your cookies"
echo "  2. Restart Claude Code to load the skill"
echo "  3. Use: /metaai to activate"
echo ""
echo "Documentation: $SCRIPT_DIR/docs/index.html"
echo ""
