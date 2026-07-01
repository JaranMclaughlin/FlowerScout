import pathlib
import subprocess
result = subprocess.run(['grep', '-rn', 'UserSession.currentUser', 'lib'], capture_output=True, text=True, cwd='.')
print(result.stdout)