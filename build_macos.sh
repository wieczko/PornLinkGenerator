#!/usr/bin/env bash
set -euo pipefail

python3 -m pip install --quiet pyinstaller
python3 -m PyInstaller --onefile --windowed --name PornLinkGenerator src/main.py --distpath dist --workpath build --specpath .

echo "macOS build complete. Output: ./dist/PornLinkGenerator.app or binary in dist/"
