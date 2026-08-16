#!/bin/sh
# Regenerate resume.pdf from resume.html via headless Chrome.
# Run before deploying, then commit the updated resume.pdf:
#     ./build_resume.sh
set -e
cd "$(dirname "$0")"
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
if [ ! -x "$CHROME" ]; then
  echo "Chrome not found at $CHROME" >&2
  exit 1
fi
"$CHROME" --headless=new --disable-gpu --no-pdf-header-footer \
  --print-to-pdf=resume.pdf resume.html >/dev/null 2>&1
echo "Wrote resume.pdf from resume.html"
