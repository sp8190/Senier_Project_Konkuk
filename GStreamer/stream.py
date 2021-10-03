import os as os

print os.system("ls -al")
print os.system("ls -al | grep System* > ras_gstream")