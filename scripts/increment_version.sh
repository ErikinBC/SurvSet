#!/usr/bin/env bash
set -euo pipefail

# Increment version in setup.py and SurvSet/__init__.py and optionally commit

SETUP_FILE="setup.py"
INIT_FILE="SurvSet/__init__.py"

# Get current version from setup.py
CURRENT_VERSION=$(grep 'version=' "$SETUP_FILE" | head -1 | sed 's/.*version="\([^"]*\)".*/\1/')
echo "Current version: $CURRENT_VERSION"

# Parse version components
MAJOR=$(echo "$CURRENT_VERSION" | cut -d. -f1)
MINOR=$(echo "$CURRENT_VERSION" | cut -d. -f2)
PATCH=$(echo "$CURRENT_VERSION" | cut -d. -f3)

# Increment patch version
NEW_PATCH=$((PATCH + 1))
NEW_VERSION="$MAJOR.$MINOR.$NEW_PATCH"

echo "New version: $NEW_VERSION"

# Update setup.py
sed -i '' "s/version=\"$CURRENT_VERSION\"/version=\"$NEW_VERSION\"/" "$SETUP_FILE"

# Update SurvSet/__init__.py
sed -i '' "s/__version__ = \"$CURRENT_VERSION\"/__version__ = \"$NEW_VERSION\"/" "$INIT_FILE"

echo "✓ Updated $SETUP_FILE"
echo "✓ Updated $INIT_FILE"

# Optional: commit
if [[ "${1:-}" == "--commit" ]]; then
  git add "$SETUP_FILE" "$INIT_FILE"
  git commit -m "Bump version to $NEW_VERSION"
  echo "✓ Committed version bump"
fi

echo "Done! Testing version update:"
echo "  Running: python3 -m SurvSet"
./surv/bin/python -m SurvSet

echo ""
echo "Next steps:"
echo "  1. rm -rf dist/ && ./surv/bin/python -m build"
echo "  2. ./surv/bin/python -m twine upload dist/*"
echo "  3. git push"
