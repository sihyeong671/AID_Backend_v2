from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import News
from .serializer import NewsSerializer


# 현재는 뉴스 조회만 가능, 생성은 test용으로 로그인하면 생성할 수 있도록 해놓음.
# 이후 CRUD가 모두 필요할 때 mixin 대신 ModelViewSet을 상속하는 것으로 변경.
class NewsViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    # mixins.UpdateModelMixin,
    # mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = News.objects.all()
    serializer_class = NewsSerializer

    permission_classes = [IsAuthenticatedOrReadOnly]
