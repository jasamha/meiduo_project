"""
 *  @ 创建者      zsh
 *  @ 创建时间    18-6-20 下午9:23
 *  @ 创建描述    
 *  
"""
'''
verifications 应用
'''
# 图片验证码的缓存时间
IMAGE_CODE_REDIS_EXPIRES = 25 * 60
# 短信验证码过期时间
SMS_CODE_REDIS_EXPIRES = 10 * 60

# 发送短信的时间间隔
SEND_SMS_CODE_INTERVAL = 60

# 短信发送模板的编号
SMS_TEMP_ID = 1
# redis短信验证码链接
VERIFY_CODES = "verify_codes"
