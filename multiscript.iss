; Script for generating Windows installer using Inno Setup

#define MyAppName "Multiscript"
#define MyAppVersion "0.10.0"
#define MyAppPublisher "Multiscript"
#define MyAppURL "https://www.multiscript.app/"
#define MyAppExeName "Multiscript_.exe"

#define MyPlanAssocName MyAppName + " Plan"
#define MyPlanAssocExt ".mplan"
#define MyPlanAssocKey StringChange(MyPlanAssocName, " ", "") + MyPlanAssocExt
#define MyPlanIconSubpath "multiscript\icons\multiscript_mplan.ico"

#define MyPluginAssocName MyAppName + " Plugin"
#define MyPluginAssocExt ".mplugin"
#define MyPluginAssocKey StringChange(MyPlanAssocName, " ", "") + MyPluginAssocExt
#define MyPluginIconSubpath "multiscript\icons\multiscript_mplugin.ico"

[Setup]
; NOTE: The value of AppId uniquely identifies this application. Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId=app.multiscript
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
ChangesAssociations=yes
DisableProgramGroupPage=yes
; Remove the following line to run in administrative install mode (install for all users.)
PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog
OutputDir=C:\JamesWorkArea\Code\multiscript\dist\
OutputBaseFilename=multiscript_installer
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "C:\JamesWorkArea\Code\multiscript\dist\multiscript\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\JamesWorkArea\Code\multiscript\dist\multiscript\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Registry]
Root: HKA; Subkey: "Software\Classes\{#MyPlanAssocExt}\OpenWithProgids"; ValueType: string; ValueName: "{#MyPlanAssocKey}"; ValueData: ""; Flags: uninsdeletevalue
Root: HKA; Subkey: "Software\Classes\{#MyPlanAssocKey}"; ValueType: string; ValueName: ""; ValueData: "{#MyPlanAssocName}"; Flags: uninsdeletekey
Root: HKA; Subkey: "Software\Classes\{#MyPlanAssocKey}\DefaultIcon"; ValueType: string; ValueName: ""; ValueData: "{app}\{#MyPlanIconSubpath}"
Root: HKA; Subkey: "Software\Classes\{#MyPlanAssocKey}\shell\open\command"; ValueType: string; ValueName: ""; ValueData: """{app}\{#MyAppExeName}"" ""%1"""
Root: HKA; Subkey: "Software\Classes\Applications\{#MyAppExeName}\SupportedTypes"; ValueType: string; ValueName: "{#MyPlanAssocExt}"; ValueData: ""

Root: HKA; Subkey: "Software\Classes\{#MyPluginAssocExt}\OpenWithProgids"; ValueType: string; ValueName: "{#MyPluginAssocKey}"; ValueData: ""; Flags: uninsdeletevalue
Root: HKA; Subkey: "Software\Classes\{#MyPluginAssocKey}"; ValueType: string; ValueName: ""; ValueData: "{#MyPluginAssocName}"; Flags: uninsdeletekey
Root: HKA; Subkey: "Software\Classes\{#MyPluginAssocKey}\DefaultIcon"; ValueType: string; ValueName: ""; ValueData: "{app}\{#MyPluginIconSubpath}"
Root: HKA; Subkey: "Software\Classes\{#MyPluginAssocKey}\shell\open\command"; ValueType: string; ValueName: ""; ValueData: """{app}\{#MyAppExeName}"" ""%1"""
Root: HKA; Subkey: "Software\Classes\Applications\{#MyAppExeName}\SupportedTypes"; ValueType: string; ValueName: "{#MyPluginAssocExt}"; ValueData: ""


[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

