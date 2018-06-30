# Create your views here.
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ReadOnlyModelViewSet

from meiduo_mall.utils.logutils import Log
from users.models import User
from users.serializer import UserAllSerializer, CreateUserSerializer, CustomFieldSerializer


class User2View(GenericViewSet, RetrieveModelMixin):
    queryset = User.objects.all()
    serializer_class = UserAllSerializer


class UserView(GenericViewSet, CreateModelMixin, RetrieveModelMixin):
    queryset = User.objects.all()
    serializer_class = UserAllSerializer

    lookup_fields = ["username"]

    def get_serializer_class(self):
        """使用不同的序列化器"""
        if self.action == 'register_user':  # name为自定义的action(修改部门名称)
            return CreateUserSerializer
        elif self.action == "get_on_name":
            return UserAllSerializer
        elif self.action in ["mobile_iscount", "username_iscount"]:
            return CustomFieldSerializer
        else:
            return UserAllSerializer

    # for field in self.multiple_lookup_fields:
    # filter[field] = self.kwargs[field]
    def get_object(self):
        queryset = self.get_queryset()
        filterfield = {}
        for field in self.lookup_fields:
            filterfield[field] = self.kwargs[field]
        obj = get_object_or_404(queryset, **filterfield)
        self.check_object_permissions(self.request, obj)
        return obj

    @action(methods=['get'], detail=False)
    def get_on_name(self, request, username):
        return self.retrieve(request, username)

    @action(methods=['get'], detail=False)
    def get_on_mobile(self, request, mobile):
        """
        根据收据查询
        :param request:
        :param mobile:
        :return:
        """
        return self.retrieve(request, mobile)

    @action(methods=['get'], detail=False)
    def get_on_id(self, request, pk):
        return self.retrieve(request, pk)

    @action(methods=['post'], detail=False)
    def register_user(self, request):
        """
        用户注册功能
        :param request:
        :return:
        """
        # request.data
        # create_user_serializer = self.get_serializer(data=request.data)
        # create_user_serializer.is_valid(raise_exception=True)

        return self.create(request)

    @action(methods=['get'], detail=False)
    def username_iscount(self, request):
        """
        自定义action: 查询用户名是否存在
        """
        username = request.query_params.get("username")
        image_cc_serializer = self.get_serializer(data={"username": username}, partial=True)
        ishas = image_cc_serializer.is_valid()

        if ishas:
            username_count = User.objects.filter(username=username).count()
            Log.error("username_count",username_count)
            data = {
                'username': username,
                'count': username_count
            }
            return Response(data)
        else:
            return Response(image_cc_serializer.errors)

    @action(methods=['get'], detail=False)
    def mobile_iscount(self, request):
        """
        自定义action: 查询手机号是否存在
        """
        mobile = request.query_params.get("mobile")
        Log.error("手机号", mobile)
        image_cc_serializer = self.get_serializer(data={"mobile": mobile}, partial=True)
        ishas = image_cc_serializer.is_valid()
        Log.error("验证手机号", ishas)
        if ishas:
            mobile_count = User.objects.filter(mobile=mobile).count()
            data = {
                'mobile': mobile,
                'count': mobile_count
            }
            return Response(data)
        else:
            return Response(image_cc_serializer.errors)
