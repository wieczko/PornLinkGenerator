#!/usr/bin/env bash
set -euo pipefail

python3 -m pip install --quiet pyinstaller
python3 -m PyInstaller --onefile --name PornLinkGenerator src/main.py --distpath dist --workpath build --specpath .

echo "Linux build complete. Output: ./dist/PornLinkGenerator"
