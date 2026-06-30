#!/bin/bash
set -e

echo "=== Dangle Axiom v2.0.0 - GitHub Push Script ==="
echo ""

# Check for token
if [ -z "$GH_TOKEN" ]; then
    echo "Please set your GitHub token:"
    echo "export GH_TOKEN=your_token_here"
    exit 1
fi

echo "1. Configuring git..."
git config user.email "artistso@example.com"
git config user.name "artistso"

echo "2. Adding remote..."
git remote remove origin 2>/dev/null || true
git remote add origin https://x-access-token:${GH_TOKEN}@github.com/artistso/gutty.git

echo "3. Pushing to GitHub..."
git push -u origin main --force

echo "4. Enabling GitHub Pages..."
gh auth login --with-token <<< "$GH_TOKEN"
gh repo edit artistso/gutty --enable-pages --pages-source=docs --pages-branch=gh-pages 2>/dev/null || echo "Pages may need manual setup in repo settings"

echo ""
echo "✅ Push complete!"
echo "Repository: https://github.com/artistso/gutty"
echo "GitHub Pages will be available at: https://artistso.github.io/gutty"
