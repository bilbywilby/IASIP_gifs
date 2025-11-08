☀️ IASIP_gifs: The Golden God's Collection of Always Sunny GIFs
​The definitive source repository for the finest reaction GIFs from Paddy's Pub.
​This repository serves as a centralized, community-driven collection of high-quality, perfectly timed reaction GIFs from the long-running FXX/FX comedy series, It's Always Sunny in Philadelphia. Whether you need Mac's ocular pat-down, Dennis's five-star analysis, or Charlie's illiteracy, we've got you covered.
​📂 Repository Structure
​All GIF files reside in the /gifs directory, and their metadata is cataloged in a central manifest.
## IASIP‑GIF Library

A curated collection of “It’s Always Sunny in Philadelphia” GIFs hosted via GitHub Pages for easy direct URLs. Use these GIFs in email signatures, presentations, or personal branding. Files are descriptively named for quick discovery and versioned with Git.

---

### Repository contents
- gifs/ — all GIF files (descriptive filenames)
- README.md — this file
- LICENSE — MIT License

---

### Quick start
1. Find a GIF source (GIPHY, Tenor) and copy the direct .gif URL.
2. Download and name the file descriptively, e.g.:
- gifs/charlie_explaining_meme.gif
- gifs/frank_reynolds_dance.gif

macOS / Linux:
```bash
curl -L "https://media.giphy.com/media/XYZ/giphy.gif" -o gifs/charlie_explaining_meme.gif
```

Windows PowerShell:
```powershell
Invoke-WebRequest -Uri "https://media.giphy.com/media/XYZ/giphy.gif" -OutFile "gifs\charlie_explaining_meme.gif"
```

3. Commit and push:
```bash
git add gifs/charlie_explaining_meme.gif
git commit -m "Add charlie_explaining_meme.gif"
git push origin main
```

4. Enable GitHub Pages (Settings → Pages → Source: main branch). Your public URLs will be:
```
https://<your-username>.github.io/iasip-gifs/gifs/<filename>.gif
```

5. Insert into your email signature HTML:
```html
<img src="https://<your-username>.github.io/iasip-gifs/gifs/charlie_explaining_meme.gif"
alt="Charlie explaining meme"
width="150" style="display:block;border:0;padding-top:5px;">
```

---

### Naming convention
Use lowercase, underscores, and concise descriptions:
- character_action_context.gif
Examples:
- charlie_explaining_meme.gif
- frank_reynolds_dance.gif
- dee_screaming_reaction.gif

Add optional metadata in a `gifs/README.md` (season, episode, timestamp).

---

### Maintenance tips
- Keep GIF sizes small (<500 KB) to reduce email load times. Use tools like https://ezgif.com/optimize.
- Rename with `git mv` to preserve history:
`git mv gifs/old_name.gif gifs/new_name.gif`
- Remove unused GIFs with `git rm gifs/unwanted.gif`
- Commit messages: “Add”, “Rename”, “Remove” + short descriptor.

---

### Automation (optional)
Example script to add and push a GIF (update <your-username> before use):
  ```bash
  #!/usr/bin/env bash
  URL = "$1"
  NAME = "$2"
  curl -L "$URL" -o "gifs/$NAME"
  git add "gifs/$NAME"
  git commit -m "Add $NAME"
  git push origin main
  echo "Published: https://<your-username>.github.io/iasip-gifs/gifs/$NAME"
  ```

  Usage:
  `./add_gif.sh "https://media.giphy.com/media/XYZ/giphy.gif" "charlie_explaining_meme.gif"`

  ---

  ### Legal & licensing

  License for this repository: MIT License.

  Note: GIF files were sourced from third‑party services (e.g., GIPHY, Tenor) and may remain subject to those services’ terms and the original content owners’ rights. This repository provides hosting convenience only; users are responsible for ensuring their use complies with applicable copyright and terms of service.

  Full license (LICENSE file):
  ```
  MIT License

  Copyright (c) 2025 bilbywilby

  Permission is hereby granted, free of charge, to any person obtaining a copy
  of this software and associated documentation files (the "Software"), to deal
  in the Software without restriction, including without limitation the rights
  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
  copies of the Software, and to permit persons to whom the Software is
  furnished to do so, subject to the following conditions:

  The above copyright notice and this permission notice shall be included in all
  copies or substantial portions of the Software.

  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
  SOFTWARE.
  ```

  ---

  ### Contribution
  - Fork the repo, add GIF(s) to `gifs/`, and open a pull request.
  - Use descriptive filenames and include a one‑line commit message.
  - Maintainers should confirm files are suitable for public hosting.

  ---

  ### Contact
  For questions or help setting up GitHub Pages, open an issue or contact the repo owner.

  — bilbywilby