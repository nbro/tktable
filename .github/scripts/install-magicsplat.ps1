<#
.SYNOPSIS
    Installs Magicsplat Tcl/Tk on a GitHub Actions Windows runner, and tells the next steps where its
    Tktable is.

.DESCRIPTION
    Magicsplat 1.x ships Tcl 8.6 and 2.x ships Tcl 9.0, so it installs the latest release whose Tcl
    major version matches the one of the Python on PATH.
#>
$ErrorActionPreference = "Stop"


function Get-PythonTclVersion {
    python -c "import tkinter; print(tkinter.TclVersion)"
}


function Find-MagicsplatVersion {
    param([Parameter(Mandatory)][string]$TclVersion)

    $major = if ($TclVersion -like "8.*") { "1" } else { "2" }

    # Each line of the output is "magicsplat-tcl-tk|<version>".
    $versions = choco search magicsplat-tcl-tk --exact --all-versions --limit-output |
        ForEach-Object { ($_ -split "\|")[1] } |
        Where-Object { $_ -like "$major.*" }

    $latest = $versions | Sort-Object { [version]$_ } -Descending | Select-Object -First 1
    if (-not $latest) { throw "No magicsplat-tcl-tk $major.x package on Chocolatey" }

    return $latest
}


function Install-Magicsplat {
    param([Parameter(Mandatory)][string]$Version)

    choco install magicsplat-tcl-tk --version $Version -y --no-progress
    if ($LASTEXITCODE -ne 0) { throw "choco install failed with exit code $LASTEXITCODE" }
}


function Find-TktableLibrary {
    $roots = @($env:ProgramFiles, ${env:ProgramFiles(x86)}, "C:\Tcl", $env:LOCALAPPDATA) |
        Where-Object { $_ -and (Test-Path $_) }

    $found = Get-ChildItem $roots -Recurse -Filter pkgIndex.tcl -ErrorAction SilentlyContinue |
        Where-Object { $_.DirectoryName -match "Tktable" } |
        ForEach-Object { $_.DirectoryName }
    "All Tktable copies found:" | Write-Host
    $found | ForEach-Object { "  $_" } | Write-Host

    # The runner also has R, which bundles its own Tcl 8 build of Tktable: skip it.
    $magicsplat = $found |
        Where-Object { $_ -notmatch "\\R\\R-" } |
        Sort-Object -Descending |
        Select-Object -First 1
    if (-not $magicsplat) { throw "Magicsplat's Tktable not found after installing Magicsplat" }

    return $magicsplat
}


$tcl = Get-PythonTclVersion
"Python's Tcl version: $tcl"

$version = Find-MagicsplatVersion -TclVersion $tcl
"Installing magicsplat-tcl-tk $version"
Install-Magicsplat -Version $version

$library = Find-TktableLibrary
"Found Tktable: $library"

Add-Content -Path $env:GITHUB_ENV -Value "TKTABLE_LIBRARY=$library"
Add-Content -Path $env:GITHUB_ENV -Value "TKTABLE_REQUIRED=1"
