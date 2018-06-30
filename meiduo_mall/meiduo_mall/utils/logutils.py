"""
 *  @ 创建者      zsh
 *  @ 创建时间    18-6-2 上午11:40
 *  @ 创建描述    
 *  
"""
import logging

from meiduo_mall.utils.exceptions import logger


class Log(object):
    """
    自定义的log输出
    """
    logger = logging.getLogger("jasamha")
    _self_sign = "zhang__"

    @classmethod
    def debug(cls, content):
        logger.debug(cls._self_sign + repr(content))

    @classmethod
    def warning(cls, what="", content=None):
        if content is None:
            logger.warning(cls._self_sign + what + "__")
        else:
            logger.warning(cls._self_sign + what + "__" + repr(content))

    @classmethod
    def error(cls, what="", content=None):
        if content is None:
            logger.error(cls._self_sign + what + "__")
        else:
            logger.error(cls._self_sign + what + "__" + repr(content))

    @classmethod
    def info(cls, content):
        logger.info(cls._self_sign + repr(content))
