#define MyAppName "UML .FRI"
#define MyAppVersion "2.0"
#define MyAppPublisher "Ján Janech"
#define MyAppURL "http://www.umlfri.org/"
#define MyAppExeName "umlfri2.exe"

[Setup]
AppId={{374E0B55-CD17-4AC4-8C1F-69DC99C3EBEB}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={pf}\{#MyAppName} 2
DefaultGroupName={#MyAppName} 2
AllowNoIcons=yes
LicenseFile=..\out\LICENSE.txt
OutputDir=.
OutputBaseFilename=umlfri-setup-{#MyAppVersion}
Compression=lzma
SolidCompression=yes

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
Name: "slovak"; MessagesFile: "Slovak.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "quicklaunchicon"; Description: "{cm:CreateQuickLaunchIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked; OnlyBelowVersion: 0,6.1
Name: "associate"; Description: "{cm:AssocFileExtension,{#MyAppName},.frip2}"

[Files]
Source: "..\out\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Icons]
Name: "{group}\{#MyAppName} 2"; Filename: "{app}\{#MyAppExeName}"; AppUserModelID: "FriUniza.UmlFri.{#MyAppVersion}"
Name: "{group}\{cm:UninstallProgram,{#MyAppName} 2}"; Filename: "{uninstallexe}"
Name: "{commondesktop}\{#MyAppName} 2"; Filename: "{app}\{#MyAppExeName}"; AppUserModelID: "FriUniza.UmlFri.{#MyAppVersion}"; Tasks: desktopicon
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\{#MyAppName} 2"; Filename: "{app}\{#MyAppExeName}"; AppUserModelID: "FriUniza.UmlFri.{#MyAppVersion}"; Tasks: quicklaunchicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[Registry]
Root: "HKCR"; Subkey: ".frip2"; ValueType: string; ValueData: "UmlFri2Solution"; Flags: uninsdeletevalue; Tasks: associate
Root: "HKCR"; Subkey: "UmlFri2Solution"; ValueType: string; ValueData: "UML .FRI 2 Solution"; Flags: uninsdeletekey; Tasks: associate
Root: "HKCR"; Subkey: "UmlFri2Solution\DefaultIcon"; ValueType: string; ValueData: "{app}\{#MyAppExeName}"; Tasks: associate
Root: "HKCR"; Subkey: "UmlFri2Solution\shell\open\command"; ValueType: string; ValueData: """{app}\{#MyAppExeName}"" ""%1"""; Tasks: associate
