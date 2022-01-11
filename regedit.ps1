Get-Item -Path Registry::HKEY_CLASSES_ROOT\Directory\Background\shell |
Select-Object -ExpandProperty Property
Get-Item -Path Registry::HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion |
  Select-Object -ExpandProperty Property