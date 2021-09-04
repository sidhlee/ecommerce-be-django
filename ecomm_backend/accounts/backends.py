from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


class CaseInsensitiveModelBackend(ModelBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        if username is None:
            # Get the username from Account.USERNAME_FIELD
            username = kwargs.get(UserModel.USERNAME_FIELD)

        try:
            # TODO: understand what is going on here
            case_insensitive_username_field = '{}__iexact'.format(
                UserModel.USERNAME_FIELD)
            user = UserModel._default_manager.get(
                **{case_insensitive_username_field: username})
        except UserModel.DoesNotExist:
            UserModel().set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
