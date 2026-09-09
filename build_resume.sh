#!/bin/sh
# Regenerate resume.pdf from resume.html via headless Chrome or Chromium.
# Run before deploying, then commit the updated resume.pdf:
#     ./build_resume.sh
set -e

CD_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$CD_DIR"

# Search candidates for Chrome/Chromium binary
CHROME_BIN=""
for candidate in   "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"   "/Applications/Chromium.app/Contents/MacOS/Chromium"   "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser"   "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge"   "$(which google-chrome 2>/dev/null)"   "$(which chromium-browser 2>/dev/null)"   "$(which chromium 2>/dev/null)"; do
  if [ -n "$candidate" ] && [ -x "$candidate" ]; then
    CHROME_BIN="$candidate"
    break
  fi
done

if [ -z "$CHROME_BIN" ]; then
  echo "Error: Compatible headless Chrome/Chromium binary not found." >&2
  echo "Please install Google Chrome or Chromium to generate resume.pdf." >&2
  exit 1
fi

echo "Using browser binary: $CHROME_BIN"
"$CHROME_BIN" --headless=new --disable-gpu --no-pdf-header-footer   --print-to-pdf=resume.pdf resume.html >/dev/null 2>&1

if [ -f "resume.pdf" ]; then
  echo "Successfully wrote resume.pdf from resume.html"
else
  echo "Error: Failed to generate resume.pdf" >&2
  exit 1
fi
