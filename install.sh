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

Done. Start a new Claude Code session to pick up the plugin.

Two lanes. Build the corpus:
  1. create a PRIVATE repo with a corpus/ directory
  2. /career-corpus:bootstrap  seed it from your résumé, and rank what to extract
  3. /career-corpus:interview  fill in stories, one at a time
  4. /career-corpus:compact    prune old history out of story files, when they get heavy

Then spend it, once you've found a role:
  5. /career-corpus:apply      open the application and check the corpus against the JD
  6. /career-corpus:render     the résumé and the cover letter
  7. /career-corpus:prep       an interview pack, once a round is booked
EOF
