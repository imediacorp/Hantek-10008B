# Push Instructions

## Authentication Options

### Option 1: SSH (Recommended if you have SSH keys set up)

The remote is already configured for SSH:
```bash
git push -u origin main
git push origin v1.0.0
```

### Option 2: HTTPS with Personal Access Token

1. **Create a Personal Access Token**:
   - Go to: https://github.com/settings/tokens
   - Click "Generate new token (classic)"
   - Select scopes: `repo` (full control)
   - Copy the token

2. **Use token for authentication**:
   ```bash
   git remote set-url origin https://github.com/imediacorp/Hantek-10008B.git
   git push -u origin main
   # When prompted for username: your GitHub username
   # When prompted for password: paste your personal access token
   git push origin v1.0.0
   ```

### Option 3: GitHub CLI

If you have GitHub CLI installed:
```bash
gh auth login
git push -u origin main
git push origin v1.0.0
```

## Quick Push Commands

Once authenticated, run:

```bash
cd hantek1008b_standalone

# Push main branch
git push -u origin main

# Push release tag
git push origin v1.0.0
```

## Verify Push

After pushing, check:
- https://github.com/imediacorp/Hantek-10008B
- All files should be visible
- Tag v1.0.0 should appear under Releases

## Next Steps After Push

1. **Create Release**:
   - Go to: https://github.com/imediacorp/Hantek-10008B/releases/new
   - Tag: `v1.0.0`
   - Title: `v1.0.0 - Initial Release`
   - Description: Copy from `RELEASE_NOTES_v1.0.0.md`

2. **Add Topics**: hantek, oscilloscope, python, macos, linux, etc.

3. **Enable Issues**: In repository settings

