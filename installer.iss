; Inno Setup script to build installer for DTF Print Manager
[Setup]
AppName=DTF Print Manager
AppVersion=1.0
DefaultDirName={pf}\DTF Print Manager
DefaultGroupName=DTF Print Manager
OutputBaseFilename=DTF_Print_Manager_Installer
Compression=lzma
SolidCompression=yes
PrivilegesRequired=admin

[Files]
Source: "dist\DTF Print Manager.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\DTF Print Manager"; Filename: "{app}\DTF Print Manager.exe"
Name: "{commondesktop}\DTF Print Manager"; Filename: "{app}\DTF Print Manager.exe"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Create a &desktop icon"; GroupDescription: "Additional icons:"