from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser, PermissionsMixin
# AbstractBaseUser：デフォルトのユーザーモデルをカスタマイズするために使うモデル
# PermissionsMixin：パーミッションの機能を利用したい場合は、これを継承しておく必要がある。


class MyUserManager(BaseUserManager):
    def create_user(self, email, account, username, password = None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError("メールアドレスは必ず入力してください。")


        user = self.model(
            email = self.normalize_email(email),
            username = username,
        )


        user.set_password(password)
        user.save(using = self._db)
        return user

    def create_superuser(self, email, account, username, password = None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password = password,
            username = username,
            account = account,
        )
        user.is_admin = True
        user.save(using = self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        verbose_name = "ユーザー名",
        max_length = 25
    )
    account = models.CharField(
        verbose_name = "アカウント",
        max_length = 25,
    )
    email = models.EmailField(
        verbose_name = "メールアドレス",
        max_length = 100,
        unique = True,
    )
    description = models.TextField(
        verbose_name = "説明",
        max_length = 250
    )
    created_date = models.DateTimeField(auto_now_add = True)
    updated_date = models.DateTimeField(auto_now = True)
    is_active = models.BooleanField(default = True)
    is_admin = models.BooleanField(default = False)


    objects = MyUserManager()


    USERNAME_FIELD = 'email' # ユーザーモデルの中でユーザーを一意に識別できる項目
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['username'] # 管理者がターミナル上でユーザーを作成する際に入力が求められる項目
# USERNAME_FIELDに指定した項目やパスワードはここに追加しなくても必ず入力を求められる


    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True


    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

# モデルのクラス内に配置できる特別なクラスで、モデルの設定を変えられる
    class Meta:
        db_table = 'users'
