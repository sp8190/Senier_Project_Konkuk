#import 하는 부분은 다들 아실테니 넘어가고
import sys
import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GstRtspServer, GObject
#메인이 시작됩니다.
if __name__ == '__main__':
    #루프를 선언하는데 이게 GstRtspServer의 루프입니다.
	loop = GObject.MainLoop()
	GObject.threads_init()
	Gst.init(None)

	class MyFactory(GstRtspServer.RTSPMediaFactory):
		def __init__(self):
			GstRtspServer.RTSPMediaFactory.__init__(self)
        #팩토리에 들어갈 영상의 파이프라인을 설정하는 부분입니다.
        #아래에서 해당 함수를 콜하는 부분이 없지만 init 될때와 서버가
        #기동해서 루프돌고 있을때 참조해서 가동하게 됩니다.
		def do_create_element(self, url):
			#여기에 파이프라인을 형성할 영상의 주소와 그 설정을 넣게 됩니다.
            spec = """
			filesrc location=test.mp4 ! qtdemux name=demux
			demux.video_0 ! queue ! rtph264pay pt=96 name=pay0
			demux.audio_0 ! queue ! rtpmp4apay pt=97 name=pay1
			demux.subtitle_0 ! queue ! rtpgstpay pt=98 name=pay2
			"""
			return Gst.parse_launch(spec)

  	class GstServer():
		def __init__(self):
            #GstRtspServer를 클래스 내에서 선언하고
			self.server = GstRtspServer.RTSPServer()
            #포트를 지정해줍니다.
			self.server.set_service("3002")
            #팩토리를 생성하는데 이 부분은 위의 MyFactory 클래스에서 설명하겠습니다.
			f = MyFactory()
            #이 팩토리를 공유 할것이라 설정하고
			f.set_shared(True)
            #서버 마운트 포인트를 선언하고
			m = self.server.get_mount_points()
            #마운트 포인트에 주소와 공유할 팩토리를 넣어줍니다.
			m.add_factory("/test", f)
			self.server.attach(None)

    # GstServer 클래스로 서버 설정을 마치고
	s = GstServer()
    #서버 루프를 돌립니다.
	loop.run()