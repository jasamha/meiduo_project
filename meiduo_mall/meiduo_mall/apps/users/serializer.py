"""
 *  @ 创建者      zsh
 *  @ 创建时间    18-6-25 下午12:03
 *  @ 创建描述    
 *  
"""
import re

from django_redis import get_redis_connection
from rest_framework import serializers

from users.models import User
from meiduo_mall.utils import constants


class UserAllSerializer(serializers.ModelSerializer):
    username = serializers.CharField(min_length=5, max_length=20, label="用户名")

    class Meta:
        model = User
        exclude = ('password',)
        extra_kwargs = {
            # 'id': {'read_only': True},
            'mobile': {
                'min_length': 11,
                'max_length': 11,
                'error_messages': {
                    'min_length': '请输入长度为11的手机号',
                    'max_length': '请输入长度为11的手机号',
                }
            },
        }


class CustomFieldSerializer(serializers.Serializer):
    username = serializers.CharField(min_length=5, max_length=20,
                                     label="用户名", error_messages={'min_length': '请求长度为5-20之间的用户名',
                                                                  'max_length': '请求长度为5-20之间的用户名' })
    mobile = serializers.CharField(min_length=11, max_length=11, label="手机号",
                                   error_messages={'min_length': '请输入长度为11的手机号', 'max_length': '请输入长度为11的手机号', })


class CreateUserSerializer(serializers.ModelSerializer):
    """
    创建用户序列化器
    """
    password2 = serializers.CharField(label='确认密码', required=True, allow_null=False, allow_blank=False, write_only=True)
    sms_code = serializers.CharField(label='短信验证码', required=True, allow_null=False, allow_blank=False, write_only=True)
    allow = serializers.CharField(label='同意协议', required=True, allow_null=False, allow_blank=False, write_only=True)

    def validate_mobile(self, value):
        """验证手机号"""
        if not re.match(r'^1[345789]\d{9}$', value):
            raise serializers.ValidationError('手机号格式错误')
        return value

    def validate_allow(self, value):
        """检验用户是否同意协议"""
        if value != 'true':
            raise serializers.ValidationError('请同意用户协议')
        return value

    def validate(self, data):
        # 判断两次密码
        if data['password'] != data['password2']:
            raise serializers.ValidationError('两次密码不一致')
        # 判断短信验证码
        redis_conn = get_redis_connection(constants.VERIFY_CODES)
        mobile = data.get("mobile")

        real_sms_code = redis_conn.get('sms_%s' % mobile)
        if real_sms_code is None:
            raise serializers.ValidationError('无效的短信验证码')
        if data['sms_code'] != real_sms_code.decode():
            raise serializers.ValidationError('短信验证码错误')

        return data

    def create(self, validated_data):
        """
        创建用户
        """
        # 移除数据库模型类中不存在的属性
        del validated_data['password2']
        del validated_data['sms_code']
        del validated_data['allow']
        user = super().create(validated_data)

        # 调用django的认证系统加密密码
        user.set_password(validated_data['password'])
        user.save()

        return user

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'password2', 'sms_code', 'mobile', 'allow')
        extra_kwargs = {
            # 'id': {'read_only': True},
            'username': {
                'min_length': 5,
                'max_length': 20,
                'error_messages': {
                    'min_length': '仅允许5-20个字符的用户名',
                    'max_length': '仅允许5-20个字符的用户名',
                }
            },
            'password': {
                'write_only': True,
                'min_length': 8,
                'max_length': 20,
                'error_messages': {
                    'min_length': '仅允许8-20个字符的密码',
                    'max_length': '仅允许8-20个字符的密码',
                }
            }
        }
