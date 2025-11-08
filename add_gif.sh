#!/bin/bash
# Script to download, optimize, commit, and push a GIF to the repository.

# --- Configuration ---
# Set the default branch name
BRANCH="main"
REPO_DIR="$(dirname "$0")"
GIFS_DIR="$REPO_DIR/gifs"

# Check required environment variables (replace with your actual username and repo)
if [ -z "$GITHUB_USER" ] || [ -z "$REPO_NAME" ]; then
  echo "Error: GITHUB_USER and REPO_NAME environment variables must be set."
  echo "Example: GITHUB_USER=bilbywilby REPO_NAME=IASIP-Signature-Gifs ./add_gif.sh ..."
  exit 1
fi

# Check arguments
if [ "$#" -ne 2 ]; then
  echo "Usage: $0 <URL_TO_GIF> <LOCAL_FILE_NAME.gif>"
  exit 1
fi

URL="$1"
NAME="$2"
TMP_DIR="$(mktemp -d)"

# Ensure the gifs directory exists
mkdir -p "$GIFS_DIR"

echo "Downloading $URL to temporary file..."
curl -sL "$URL" -o "$TMP_DIR/$NAME"

if [ $? -ne 0 ] || [ ! -s "$TMP_DIR/$NAME" ]; then
  echo "Error: Failed to download or downloaded file is empty."
  rm -rf "$TMP_DIR"
  exit 2
fi

# --- Local Optimization (Optional, Controlled by GIFSICLE_SKIP_LOCAL) ---
if [ "$GIFSICLE_SKIP_LOCAL" != "1" ]; then
  echo "Attempting local optimization..."
  
  if command -v gifsicle &> /dev/null; then
    # Optimization with gifsicle for best results
    gifsicle --lossy=80 -O3 "$TMP_DIR/$NAME" > "$TMP_DIR/optimized_$NAME"
    if [ $? -eq 0 ] && [ -s "$TMP_DIR/optimized_$NAME" ]; then
      ORIG_SIZE=$(du -h "$TMP_DIR/$NAME" | awk '{print $1}')
      OPT_SIZE=$(du -h "$TMP_DIR/optimized_$NAME" | awk '{print $1}')
      echo "Gifsicle optimization successful. Size reduced from $ORIG_SIZE to $OPT_SIZE."
      mv "$TMP_DIR/optimized_$NAME" "$TMP_DIR/$NAME"
    else
      echo "Gifsicle optimization failed or resulted in zero size; keeping original."
    fi
  elif command -v ffmpeg &> /dev/null; then
    # Fallback to ffmpeg optimization (less effective for GIFs)
    ffmpeg -i "$TMP_DIR/$NAME" -vf "scale='min(500,iw)':'min(500,ih)':force_original_aspect_ratio=decrease,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" -loop 0 "$TMP_DIR/optimized_$NAME" > /dev/null 2>&1
    if [ $? -eq 0 ] && [ -s "$TMP_DIR/optimized_$NAME" ]; then
      ORIG_SIZE=$(du -h "$TMP_DIR/$NAME" | awk '{print $1}')
      OPT_SIZE=$(du -h "$TMP_DIR/optimized_$NAME" | awk '{print $1}')
      echo "FFmpeg optimization successful. Size reduced from $ORIG_SIZE to $OPT_SIZE."
      mv "$TMP_DIR/optimized_$NAME" "$TMP_DIR/$NAME"
    else
      echo "FFmpeg optimization failed; keeping original."
    fi
  else
    echo "No local optimizer found (gifsicle or ffmpeg). Skipping local optimization."
  fi
fi

# --- Final Checks and Push ---

DEST="$GIFS_DIR/$NAME"
if [ -e "$DEST" ]; then
  echo "Error: destination $DEST already exists. Aborting to avoid overwrite."
  rm -rf "$TMP_DIR"
  exit 3
fi

mv "$TMP_DIR/$NAME" "$DEST"
rm -rf "$TMP_DIR"

cd "$REPO_DIR"

git add "$DEST"
git commit -m "Add $NAME" || {
  echo "Nothing to commit or commit failed."
}
git push origin "$BRANCH"

PUBLIC_URL="https://$GITHUB_USER.github.io/$REPO_NAME/gifs/$NAME"
echo -e "\n------------------------------------------------------------"
echo "Done. Use this public URL for your signature: $PUBLIC_URL"
echo "------------------------------------------------------------"
