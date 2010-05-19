; Turn off old selected section
; 12 06 2005: Luis Wong
; Template voor het genereren van een installer.
; speciaal voor het genereren van EasyPlayer installers.
; Trimedia Interactive Projects
 
 ;--------------------------------
;Include Modern UI

  !include "MUI.nsh"

;--------------------------------
;General

  ;Name and file
  Name "Sendinel Bluetooth Server"
  OutFile "InstallBluetoothServer.exe"

  !define MUI_ICON "sendinel.ico"
  !define MUI_PRODUCT "SendinelBluetoothServer"
  !define MUI_UNICON "sendinel.ico"
  !define MUI_SPECIALBITMAP "sendinel.bmp"
  
  
  ;Default installation folder
  InstallDir "$PROGRAMFILES\SendinelBluetoothServer"
  
  ;Get installation folder from registry if available
  InstallDirRegKey HKCU "Software\SendinelBluetoothServer" ""

;--------------------------------
;Interface Settings

  !define MUI_ABORTWARNING

;--------------------------------
;Pages

 
  ;!insertmacro MUI_UNPAGE_CONFIRM
  !insertmacro MUI_UNPAGE_INSTFILES
  
;--------------------------------
;Languages
 
  !insertmacro MUI_LANGUAGE "English"

;--------------------------------
;Installer Sections

Section "Dummy Section" SecDummy



SetOutPath "$INSTDIR"
 
  File "BluetoothServer.jar"
  File "start_unix.sh"
  File "start_win.cmd"
  
 ; CreateShortCut "$INSTDIR\${MUI_PRODUCT}.lnk" "$INSTDIR\start_win.cmd" "" "" SW_SHOWMINIMIZED
  CreateShortCut "$INSTDIR\${MUI_PRODUCT}.lnk" "$INSTDIR\start_win.cmd" \
  "" "$INSTDIR\start_win.cmd" 2 SW_SHOWMINIMIZED 

  ;create autostart shortcut
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Run" "StartBluetoothServer" "$INSTDIR\${MUI_PRODUCT}.lnk"
  
  
  SetOutPath "$INSTDIR\lib"
  File "lib\bluecove-2.1.0.jar"
  File "lib\bluecove-gpl-2.1.0.jar"
  File "lib\commons-logging-1.1.jar"
  File "lib\ws-commons-util-1.0.2.jar"  
  File "lib\xmlrpc-client-3.1.3.jar"
  File "lib\xmlrpc-common-3.1.3.jar"
  File "lib\xmlrpc-server-3.1.3.jar"


 
;create desktop shortcut
  ;CreateShortCut "$DESKTOP\${MUI_PRODUCT}.lnk" "$INSTDIR\start_win.cmd" ""
  CreateShortCut "$DESKTOP\${MUI_PRODUCT}.lnk" "$INSTDIR\start_win.cmd" \
  "" "$INSTDIR\start_win.cmd" 2 SW_SHOWMINIMIZED 

 
;create start-menu items
  CreateDirectory "$SMPROGRAMS\${MUI_PRODUCT}"
  CreateShortCut "$SMPROGRAMS\${MUI_PRODUCT}\Uninstall.lnk" "$INSTDIR\Uninstall.exe" "" "$INSTDIR\Uninstall.exe" 0
  CreateShortCut "$SMPROGRAMS\${MUI_PRODUCT}\${MUI_PRODUCT}.lnk" "$INSTDIR\start_win.cmd" "" "$INSTDIR\start_win.cmd" 0
  
  
  

	
;write uninstall information to the registry
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${MUI_PRODUCT}" "DisplayName" "${MUI_PRODUCT} (remove only)"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${MUI_PRODUCT}" "UninstallString" "$INSTDIR\Uninstall.exe"
 
  WriteUninstaller "$INSTDIR\Uninstall.exe"
  
  
  ;Store installation folder
  WriteRegStr HKCU "Software\Modern UI Test" "" $INSTDIR
  
SectionEnd

;--------------------------------
;Descriptions

  ;Language strings
  LangString DESC_SecDummy ${LANG_ENGLISH} "A test section."

  ;Assign language strings to sections
  !insertmacro MUI_FUNCTION_DESCRIPTION_BEGIN
    !insertmacro MUI_DESCRIPTION_TEXT ${SecDummy} $(DESC_SecDummy)
  !insertmacro MUI_FUNCTION_DESCRIPTION_END

;--------------------------------
;Uninstaller Section

Section "Uninstall"

  ;ADD YOUR OWN FILES HERE...

  Delete "$INSTDIR\Uninstall.exe"

  RMDir "$INSTDIR"
  
  
  
  
;Delete Files 
  RMDir /r "$INSTDIR\*.*"    
 
;Remove the installation directory
  RMDir "$INSTDIR"
 
;Delete Start Menu Shortcuts
  Delete "$DESKTOP\${MUI_PRODUCT}.lnk"
  Delete "$SMPROGRAMS\${MUI_PRODUCT}\*.*"
  RmDir  "$SMPROGRAMS\${MUI_PRODUCT}"
 
;Delete Uninstaller And Unistall Registry Entries
  DeleteRegKey HKEY_LOCAL_MACHINE "SOFTWARE\${MUI_PRODUCT}"
  DeleteRegKey HKEY_LOCAL_MACHINE "SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\${MUI_PRODUCT}"  
 ;create autostart shortcut
  DeleteRegKey HKEY_LOCAL_MACHINE "Software\Microsoft\Windows\CurrentVersion\Run\StartBluetoothServer"
    


SectionEnd