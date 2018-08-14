import uuid
from django.db import models
from django.utils.crypto import salted_hmac

from django.contrib.auth.hashers import (
    check_password, make_password
)


class LogUser(models.Model):
    """Log 用户表 """

    uid = models.UUIDField(default=uuid.uuid4, db_index=True, unique=True)
    account = models.CharField('账号', max_length=32, unique=True)
    name = models.CharField('姓名', max_length=32)
    password = models.CharField('密码', max_length=80)

    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True)

    is_active = models.BooleanField('是否可用', default=True)

    def get_session_auth_hash(self):
        """
        Return an HMAC of the password field.
        """
        key_salt = "django.contrib.auth.models.AbstractBaseUser.get_session_auth_hash"
        return salted_hmac(key_salt, self.password).hexdigest()

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        def setter(raw_password):
            self.set_password(raw_password)
            self.save(update_fields=['password'])

        return check_password(raw_password, self.password, setter)

    class Meta:
        verbose_name = 'Log用户'
        verbose_name_plural = 'Log用户'

    def __str__(self):
        return self.account
