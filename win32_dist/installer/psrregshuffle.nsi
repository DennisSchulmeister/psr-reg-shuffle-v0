#! /usr/bin/env makensis

# psrregshuffle.nsi
# This file is part of PSR Registration Shuffler
#
# Copyright (C) 2009 - Dennis Schulmeister  <dennis -at- ncc-1701a.homelinux.net>
#
# This is free software# you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation# either version 3 of the License, or
# (at your option) any later version.
#
# It is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY# without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this file. If not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor,
# Boston, MA  02110-1301  USA

#-------------------------------------------------------------------------------
# Includes, Macros, Global Variables ...
#-------------------------------------------------------------------------------
# Program name and version
!define VERSION "0.3.2"
!define SHORTNAME "psrregshuffle-${VERSION}"
!define AUTHOR "Dennis Schulmeister"
!define NAME "PSR Registration Shuffler ${VERSION}"

Name "${NAME}"

# Installer file ready to publish
OutFile "psr-reg-shuffle_${VERSION}_win32_setup.exe"
Icon icon.ico
XPStyle On
SetCompressor /FINAL lzma

# Macros for registering the uninstaller
!macro WriteUninstallRegValue RName RValue
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${SHORTNAME}" "${RName}" "${RValue}"
!macroend
!define WriteUninstallRegValue "!insertmacro WriteUninstallRegValue"

# Variables
Var "MY_SMPROGRAMS"
Var "DELDIR"


#-------------------------------------------------------------------------------
# (Un)installer attributes
#-------------------------------------------------------------------------------
# Require admin privileges (don't allow user installation)
RequestExecutionLevel admin

# Replace Nullsoft tag line
BrandingText "${NAME}"

# License text
LicenseData license.txt

# Install each program version to its own directory
InstallDir "$PROGRAMFILES\psrreghusffle-${VERSION}"

# Installer pages
Page license
Page components
Page directory
Page instfiles

# Uninstaller pages
UninstPage uninstConfirm
UninstPage instfiles

# Setup initialization
Function .onInit
  StrCpy $MY_SMPROGRAMS "$SMPROGRAMS\${NAME}"
FunctionEnd


#-------------------------------------------------------------------------------
# Installer sections
#-------------------------------------------------------------------------------
Section "Application Data (required)"
  # Mandatory section
  SectionIn RO

  # Create uninstaller
  SetOutPath $INSTDIR
  WriteUninstaller "$OUTDIR\uninstall.exe"

  ${WriteUninstallRegValue} "DisplayName"     "${NAME}"
  ${WriteUninstallRegValue} "UninstallString" "$OUTDIR\uninstall.exe"
  ${WriteUninstallRegValue} "InstallLocation" "$OUTDIR"
  ${WriteUninstallRegValue} "DisplayIcon"     "$OUTDIR\program.exe"
  ${WriteUninstallRegValue} "Publisher"       "${AUTHOR}"
  ${WriteUninstallRegValue} "URLInfoAbout"    "http://www.psrregshuffle.de"
  ${WriteUninstallRegValue} "DisplayVersion"  "${VERSION}"
  ${WriteUninstallRegValue} "NoModify"         1
  ${WriteUninstallRegValue} "NoRepair"         1

  # Remember installation path
  WriteRegStr HKLM "Software\${SHORTNAME}" "InstallDir" "$OUTDIR"

  # Copy files
  File /a    psrregshuffle.exe
  File /a    README.txt
  File /a    license.txt

  CreateDirectory "$INSTDIR\program"
  SetOutPath "$INSTDIR\program"
  File /a /r program\*.*

  # Create Shortcot
  SetOutPath "$INSTDIR"
  CreateDirectory $MY_SMPROGRAMS
  CreateShortCut "$MY_SMPROGRAMS\PSR Registration Shuffler.lnk" "$OUTDIR\psrregshuffle.exe"
  CreateShortCut "$MY_SMPROGRAMS\Read Me.lnk" "$OUTDIR\README.txt"
  CreateShortCut "$MY_SMPROGRAMS\License.lnk" "$OUTDIR\license.txt"
SectionEnd

Section "Example Files"
  CreateDirectory "$INSTDIR\examples"
  SetOutPath "$INSTDIR\examples"
  File /a /r examples\*.*

  CreateShortCut "$MY_SMPROGRAMS\Example Files" "$OUTDIR\examples\"
SectionEnd

Section "Manual"
  CreateDirectory "$INSTDIR\manual"
  SetOutPath "$INSTDIR\manual"
  File /a /r manual\*.*

  CreateShortCut "$MY_SMPROGRAMS\Documentation.lnk" "$OUTDIR\manual\"
SectionEnd


#-------------------------------------------------------------------------------
# Uninstaller sections
#-------------------------------------------------------------------------------
Section "Uninstall"
  # Determine uninstall directory
  ReadRegStr $DELDIR HKLM "Software\${SHORTNAME}" "InstallDir"
  IfFileExists $DELDIR +3 0
    MessageBox MB_ICONSTOP "Fatal Error: Couldn't find program directory!"
    Return

  # Remove program files
  DeleteRegKey HKLM "Software\${SHORTNAME}"

  SetOutPath $TEMP
  RmDir /r /REBOOTOK $DELDIR

  # Unregister Uninstaller
  DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${SHORTNAME}"

  # Remove shortcuts
  RmDir /r /REBOOTOK $MY_SMPROGRAMS
SectionEnd
