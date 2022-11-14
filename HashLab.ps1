function Drivers-uno
{
param( 
	[string]$TargetFolder="C:/Windows/System32/drivers/",
	[string]$ResultFile="Drivers.txt"
)

Get-Childitem $TargetFolder -Recurse -Include *.dll | Get-FileHash | Select-Object -Property Hash, Path | Format-Table -HideTableHeaders | Out-File $ResultFile -Encoding utf8 
}


function Drivers-dos
{
param( 
	[string]$TargetFolder="C:/Windows/System32/drivers/",
	[string]$ResultFile="Drivers2.txt"
)

Get-Childitem $TargetFolder -Recurse -Include *.dll | Get-FileHash | Select-Object -Property Hash, Path | Format-Table -HideTableHeaders | Out-File $ResultFile -Encoding utf8 
}

$pepe = Test-Path -path "C:\Users\angel\Desktop\pia\Drivers2.txt" -PathType Leaf

if($pepe -eq $True ) 
{
}
else
{
Drivers-dos
}

Drivers-uno
