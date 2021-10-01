# 1. 설치하기

```
$ sudo apt install libgstreamer1.0-0 gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly gstreamer1.0-libav gstreamer1.0-doc gstreamer1.0-tools gstreamer1.0-x gstreamer1.0-alsa gstreamer1.0-gl gstreamer1.0-gtk3 gstreamer1.0-pulseaudio
```

_에러 발생시_
```
$ sudo apt-get install gstreamer1.0
```

설치가 잘 되었는지 확인은 다음 명령으로 알 수 있다.
```
$ gst-launch-1.0 --version
```

# 2. 실행하기

1. 쉘 스크립트 생성
```
$ nano gst_test.sh
```

_gst_test.sh 파일 안에다가 입력_
```
#!/bin/bash

MY_IP=$(hostname -I)
echo "My IP Addr is $MY_IP"
raspivid -t 0 -h 720 -w 1280 -fps 25 -hf -b 2000000 -o - | gst-launch-1.0 -v fdsrc ! h264parse ! rtph264pay config-interval=1 pt=96 ! gdppay ! tcpserversink host=$MY_IP port=5000
```
_아래 명령어를 통해 gst_test 파일 속성 변경_
```
$ chmod +x gst_test.sh
```

**실행**
```
$ ./gst_test.sh
```
