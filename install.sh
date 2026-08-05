#!/usr/bin/env bash
set -euo pipefail

# Installs the Career Corpus Kit without going through a plugin marketplace, by
# symlinking this repo into your Claude Code skills directory. Claude Code loads
# any folder there that contains .claude-plugin/plugin.json as a plugin — here,
# `career-corpus@skills-dir` — so a later `git pull` updates it automatically.
#
# The marketplace install (see README) is the recommended path. Use this one if
# you'd rather track the repo directly. Don't use both: two plugins named
# career-corpus would provide the same /career-corpus:* skills.
#
# Override the destination with CLAUDE_SKILLS_DIR=/path ./install.sh

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEST="${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}"
LINK="$DEST/career-corpus"

mkdir -p "$DEST"

# Clean up dangling links left by pre-1.0 installs, which symlinked each skill
# separately under its old name.
for old in career-corpus-bootstrap career-corpus-interview career-corpus-render; do
  oldlink="$DEST/$old"
  if [ -L "$oldlink" ] && [ ! -e "$oldlink" ]; then
    case "$(readlink "$oldlink")" in
      "$REPO_DIR"/*)
        rm "$oldlink"
        echo "removed stale link from an earlier install: $oldlink"
        ;;
    esac
  fi
done

if [ -L "$LINK" ]; then
  echo "already linked: $LINK -> $(readlink "$LINK")"
elif [ -e "$LINK" ]; then
  echo "skip: $LINK exists and is not a symlink — remove it first to reinstall" >&2
  exit 1
else
  ln -s "$REPO_DIR" "$LINK"
  echo "linked: $LINK -> $REPO_DIR"
fi

cat <<'EOF'

Done. Start a new Claude Code session to pick up the plugin, then:
  1. create a PRIVATE repo with a corpus/ directory
  2. run /career-corpus:bootstrap to seed it from your résumé
  3. run /career-corpus:interview to fill in stories, one at a time
  4. run /career-corpus:render when you need a résumé or cover letter
EOF
