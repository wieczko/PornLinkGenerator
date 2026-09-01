$ErrorActionPreference = "Stop"

$py = "$env:LOCALAPPDATA\Programs\Python\Python312\python.exe"
if (-not (Test-Path $py)) {
    $py = "python"
}

& $py -m pip install --quiet pyinstaller
& $py -m PyInstaller --onefile --windowed --name PornLinkGenerator .\src\main.py --distpath .\dist --workpath .\build --specpath .

Write-Host "Windows build complete. Output: .\dist\PornLinkGenerator.exe"
