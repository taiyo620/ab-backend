from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model


UserModel = get_user_model()

class MyBackend(BaseBackend):
    def authenticate(self,request,username=None):
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)
        if username is None:
            return

        try:
            user = UserModel._default_manager.get_by_natural_key(username)
        except UserModel.DoesNotExist:
            return None
        return user

    def get_user(self,user_id):
        try:
            user = UserModel._default_manager.get(pk=user_id)
        except:
            return None
        return user
