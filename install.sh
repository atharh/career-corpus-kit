#!/usr/bin/env bash
set -euo pipefail

# Installs the career-corpus skills into your Claude Code skills directory by
# symlinking them, so a later `git pull` in this repo updates them automatically.
#
# Override the destination with CLAUDE_SKILLS_DIR=/path ./install.sh

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEST="${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}"

mkdir -p "$DEST"

for skill in career-corpus-interview career-corpus-render; do
  src="$REPO_DIR/skills/$skill"
  link="$DEST/$skill"
  if [ -L "$link" ]; then
    echo "skip: $link is already a symlink"
  elif [ -e "$link" ]; then
    echo "skip: $link exists and is not a symlink — remove it first to reinstall"
  else
    ln -s "$src" "$link"
    echo "linked: $link -> $src"
  fi
done

echo
echo "Done. Start a new Claude Code session to pick up the skills, then:"
echo "  1. create a PRIVATE repo with a corpus/ directory"
echo "  2. run /career-corpus-interview to start filling it"
echo "  3. run /career-corpus-render when you need a résumé or cover letter"
