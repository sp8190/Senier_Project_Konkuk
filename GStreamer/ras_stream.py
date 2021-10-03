import os as os

os.system("raspivid -n -t 0 -h 720 -w 1280 -fps 25 -b 2000000 -o - |gst-launch-1.0 -v fdsrc ! h264parse ! rtph264pay config-interval=1 pt=96 ! gdppay ! tcpserversink host=192.168.1.41 port=5000")