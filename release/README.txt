PornLinkGenerator Release Pack

This package contains the Windows executable build.

Files:
- PornLinkGenerator.exe

Usage:
- Double-click the .exe file to launch the app.
- If Windows blocks the file, click "More info" and then "Run anyway".

Build scripts for other platforms are included in the project root:
- build_windows.ps1
- build_macos.sh
- build_linux.sh

macOS build instructions:
- Open a terminal on macOS.
- Run: chmod +x build_macos.sh
- Run: ./build_macos.sh
- Result: dist/PornLinkGenerator.app

Linux build instructions:
- Open a terminal on Linux.
- Run: chmod +x build_linux.sh
- Run: ./build_linux.sh
- Result: dist/PornLinkGenerator

Windows build instructions:
- Run: powershell -ExecutionPolicy Bypass -File .\build_windows.ps1
- Result: dist\PornLinkGenerator.exe

Note:
- macOS and Linux builds must be created on their respective operating systems.
- The Windows executable here is already built and ready to run.
