import random

from django.http import HttpResponse
from django_redis import get_redis_connection
from rest_framework import serializers, status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from meiduo_mall.libs.captcha.captcha import captcha
from meiduo_mall.libs.yuntongxun.sms import CCP
from meiduo_mall.utils.logutils import Log
from verifications import serializer
# from libs.captcha.captcha import captcha
# from libs.yuntongxun.sms import CCP
from meiduo_mall.utils import constants
# from utils.logutils import Log


class ImageCodeView(APIView):
    """
    图片验证码
    """

    def get(self, request, image_code_id):
        """
        获取图片验证码
        """
        # 生成验证码图片
        name, text, image = captcha.generate_captcha()

        redis_conn = get_redis_connection("verify_codes")
        # redis_conn.setex("img_%s" % code_id, constants.IMAGE_CODE_REDIS_EXPIRES, text)
        redis_conn.setex("img_{}".format(image_code_id), constants.IMAGE_CODE_REDIS_EXPIRES, text)
        Log.error("验证码", text)

        return HttpResponse(image, content_type="images/jpg")


class SmsCodeView(GenericAPIView):
    """
    短信验证码
    """
    serializer_class = serializer.ImageCodeCheckSerializer

    def post(self, request):
        image_cc_serializer = self.get_serializer(data=request.data)
        image_cc_serializer.is_valid(raise_exception=True)
        mobile = request.data.get("mobile")
        text = request.data.get("text")

        # sms_code = "%06d" % random.randint(0, 999999)
        sms_code = str(random.randint(100000, 999999))

        # 保存短信验证码与发送记录
        redis_conn = get_redis_connection('verify_codes')
        pl = redis_conn.pipeline()
        pl.multi()
        pl.setex("sms_%s" % mobile, constants.SMS_CODE_REDIS_EXPIRES, sms_code)
        pl.setex("send_flag_%s" % mobile, constants.SEND_SMS_CODE_INTERVAL, constants.SMS_TEMP_ID)
        pl.execute()

        # 发送短信验证码
        # send_template_sms(mobile, [code, expires], SMS_CODE_TEMP_ID)
        ccp = CCP()
        ccp.send_template_sms(mobile, [sms_code, constants.SMS_CODE_REDIS_EXPIRES / 60], constants.SMS_TEMP_ID)
        return Response({"message": "OK"}, status.HTTP_200_OK)
