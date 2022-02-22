# mysite/asgi.py
import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
import chatapp.routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "chat.settings")
# channels 개발 서버와 연결이 이루어질 때 ProtocolTypeRouter를 먼저 조사한다음, 웹소켓연결이면 AuthMiddlewareStack으로 이어진다.
# AuthMiddlewareStack은 현재 인증된 사용자에 대한 참조로 scopre를 결정한다.
# 이것은 Django에서 현재 인증된 사용자의 view함수에서 request 요청을 결정하는 AuthenticationMiddleware와 유사한 방식이며 그 결과 URLRouter로 연결된다.
# URLRouter는 작성한 url패턴을 기반으로, 특정 consumer의 라우팅 연결 http path를 조사한다.
application = ProtocolTypeRouter({
  "http": get_asgi_application(),
  "websocket": AuthMiddlewareStack(
        URLRouter(
            chatapp.routing.websocket_urlpatterns
        )
    ),
})