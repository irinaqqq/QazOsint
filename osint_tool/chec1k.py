import os
import winreg

theHarvester_path = r'C:\Users\samat\AppData\theHarvester'

# Add the theHarvester path to the system's PATH environment variable
with winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE) as hkey:
    with winreg.OpenKey(hkey, r'SYSTEM\CurrentControlSet\Control\Session Manager\Environment', 0, winreg.KEY_WRITE) as environment_key:
        path_value, _ = winreg.QueryValueEx(environment_key, 'Path')
        path_value += os.pathsep + theHarvester_path
        winreg.SetValueEx(environment_key, 'Path', 0, winreg.REG_EXPAND_SZ, path_value)

# Now you should be able to run theHarvester from any directory

# Example usage
from subprocess import Popen, PIPE

domain = 'example.com'
p = Popen(['theHarvester.py', '-d', domain, '-b', 'google'], stdout=PIPE, stderr=PIPE)
output, error = p.communicate()

# Handle the output and error as needed
