#!/bin/bash
# GitHub Repository Setup Script for Hantek 1008B Driver

# M4: strict mode — exit on error, unbound variable, or failed pipeline
set -euo pipefail

echo "Hantek 1008B - GitHub Repository Setup"
echo "========================================"
echo ""

# M4: validate a GitHub URL before passing it to git
validate_github_url() {
    local url="$1"
    if [[ ! "$url" =~ ^https://github\.com/[A-Za-z0-9._-]+/[A-Za-z0-9._-]+(\.git)?$ ]]; then
        echo "ERROR: '$url' is not a valid GitHub HTTPS URL" >&2
        return 1
    fi
}

# Check if git is initialized
if [ ! -d .git ]; then
    echo "Initializing git repository..."
    git init
    echo "Git repository initialized"
else
    echo "Git repository already initialized"
fi

# Add all files
echo ""
echo "Adding files to git..."
git add .
echo "Files added"

# Check if there are changes to commit
if git diff --staged --quiet; then
    echo "No changes to commit"
else
    echo ""
    echo "Creating initial commit..."
    git commit -m "Initial commit: Hantek 1008B Python driver v1.0.0

- Cross-platform support (macOS ARM64/Intel, Linux)
- USB bridge support
- Multi-channel simultaneous acquisition
- Complete USB protocol implementation
- MIT License"
    echo "Initial commit created"
fi

# Check if remote exists
if git remote | grep -q origin; then
    echo ""
    echo "Remote 'origin' already exists"
    echo "   Current remote URL:"
    git remote get-url origin
    echo ""
    read -p "Update remote URL? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        read -r -p "Enter GitHub repository URL: " repo_url
        validate_github_url "$repo_url"
        git remote set-url origin "$repo_url"
        echo "Remote URL updated"
    fi
else
    echo ""
    echo "Add GitHub remote:"
    echo "   git remote add origin https://github.com/YOUR_USERNAME/hantek1008b.git"
    echo ""
    read -r -p "Enter GitHub repository URL (or press Enter to skip): " repo_url
    if [ -n "$repo_url" ]; then
        validate_github_url "$repo_url"
        git remote add origin "$repo_url"
        echo "Remote added"
    fi
fi

# Create main branch if needed
current_branch=$(git branch --show-current 2>/dev/null || echo "none")
if [ "$current_branch" = "none" ] || [ -z "$current_branch" ]; then
    echo ""
    echo "Creating main branch..."
    git branch -M main
    echo "Main branch created"
fi

# Create tag
echo ""
echo "Creating release tag v1.0.0..."
if git rev-parse v1.0.0 >/dev/null 2>&1; then
    echo "Tag v1.0.0 already exists"
else
    git tag -a v1.0.0 -m "Release version 1.0.0 - Initial release"
    echo "Tag v1.0.0 created"
fi

echo ""
echo "=========================================="
echo "Setup complete!"
echo ""
echo "Next steps:"
echo "1. Push to GitHub:"
echo "   git push -u origin main"
echo ""
echo "2. Push tags:"
echo "   git push origin v1.0.0"
echo ""
echo "3. Create release on GitHub:"
echo "   - Go to repository > Releases > Draft a new release"
echo "   - Select tag: v1.0.0"
echo "   - Title: v1.0.0 - Initial Release"
echo "   - Copy release notes from RELEASE_NOTES_v1.0.0.md"
echo ""
echo "4. Verify GitHub Actions:"
echo "   - Check .github/workflows/ for CI/CD"
echo ""
