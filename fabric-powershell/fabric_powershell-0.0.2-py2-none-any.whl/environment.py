from . import runPowershell


#     runPowershell('''\
# $s=New-PSSession -ComputerName sirgisdev
# Invoke-Command -Session $s -ScriptBlock {
#     [Environment]::SetEnvironmentVariable("Path","D:\Python27\ArcGISx6410.3;D:\Python27\ArcGISx6410.3\Scripts;"+$env:Path,[System.EnvironmentVariableTarget]::Process)}
#     Get-Childitem env:computername
# }''')

# python -m pip -i http://sirpypi/packages/simple/ --trusted-host sirpypi install -U pip
