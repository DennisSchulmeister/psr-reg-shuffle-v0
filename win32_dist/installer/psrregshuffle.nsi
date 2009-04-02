; psrregshuffle.nsi
; This file is part of PSR Registration Shuffler
;
; Copyright (C) 2009 - Dennis Schulmeister  <dennis -at- ncc-1701a.homelinux.net>
;
; This is free software; you can redistribute it and/or modify
; it under the terms of the GNU General Public License as published by
; the Free Software Foundation; either version 3 of the License, or
; (at your option) any later version.
;
; It is distributed in the hope that it will be useful,
; but WITHOUT ANY WARRANTY; without even the implied warranty of
; MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
; GNU General Public License for more details.
;
; You should have received a copy of the GNU General Public License
; along with this file. If not, write to the Free Software
; Foundation, Inc., 51 Franklin St, Fifth Floor,
; Boston, MA  02110-1301  USA

;-------------------------------------------------------------------------------
; Includes, Macros, Global Variables ...
;-------------------------------------------------------------------------------
; Program name and version
!define VERSION "0.3.2"
Name "PSR Registration Shuffler ${VERSION}"

; Installer file ready to publish
OutFile "psr-reg-shuffle_$(VERSION)_win32_setup.exe"
SetCompressor /FINAL lzma


;-------------------------------------------------------------------------------
; (Un)installer attributes
;-------------------------------------------------------------------------------
; License text
LicenseData license.txt

; Install each program version to its own directory
InstallDir "${PROGRAMFILES}\psrreghusffle-${VERSION}"

; Installer pages
Page license
Page components
Page directory
Page instfiles

; Uninstaller pages
UninstPage uninstConfirm
UninstPage instfiles



;-------------------------------------------------------------------------------
; Installer sections
;-------------------------------------------------------------------------------

;; TODO: Translations of section names ??? ;;

Section "Application Data (required)"
  ; TODO
SectionEnd


Section "Example Files"
  ; TODO
SectionEnd

Section "Manual"
  ; TODO
SectionEnd


;-------------------------------------------------------------------------------
; Uninstaller sections
;-------------------------------------------------------------------------------
; Nothing yet
