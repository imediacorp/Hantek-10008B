#!/bin/bash
# Push to GitHub Repository
# Repository: https://github.com/imediacorp/Hantek-10008B

set -e

echo "🚀 Pushing Hantek 1008B Driver to GitHub"
echo "Repository: https://github.com/imediacorp/Hantek-10008B"
echo ""

# Verify we're in the right directory
if [ ! -f "setup.py" ]; then
    echo "❌ Error: setup.py not found. Are you in the hantek1008b_standalone directory?"
    exit 1
fi

# Check git status
echo "📋 Checking git status..."
git status --short

# Push main branch
echo ""
echo "📤 Pushing main branch to GitHub..."
git push -u origin main

# Push tags
echo ""
echo "🏷️  Pushing release tag v1.0.0..."
git push origin v1.0.0

echo ""
echo "✅ Successfully pushed to GitHub!"
echo ""
echo "Next steps:"
echo "1. Visit: https://github.com/imediacorp/Hantek-10008B"
echo "2. Create release: https://github.com/imediacorp/Hantek-10008B/releases/new"
echo "3. Select tag: v1.0.0"
echo "4. Copy release notes from RELEASE_NOTES_v1.0.0.md"
echo "5. Publish release"
echo ""

