# Django REST framework

A personal learning note on the popular Django framework.

## Authentication with Simple JWT

From [Django REST framework documentation](https://www.django-rest-framework.org/api-guide/authentication/#json-web-token-authentication)

> Unlike the built-in TokenAuthentication scheme, JWT Authentication doesn't need to use a database to validate a token. A package for JWT authentication is djangorestframework-simplejwt which provides some features as well as a pluggable token blacklist app.

[Simple JWT documentation](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/)

### Changing the encoded value inside JWT

You can customize the "claims" in JWT by creating a subclass for `TokenObtainPairSerializer` and overriding `get_token` class method where you add extra properties to the `token` and return it. Then, you create the subclass for `TokenObtainPairView` and override `serializer_class` field with the new serializer subclass.

```python
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['name'] = user.name
        # ...

        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
```

### Token authentication with Django Rest Framework

Unlike the usual way where Django attaches `user` object to request object when the user is authenticated, Django Rest Framework's `@api_view` decorator parses the token inside the `Authorization` header (Bearer ACCESS_TOKEN) of the request, then make the data available at `request.user` inside the view function.

```python
@api_view(['GET'])
def getUserProfile(request):
    # This user object will NOT be the usual user object Django attaches to the request.
    # Instead, the @api_view decorator will parse the user data from the token and add to request.
    user = request.user

    serialized_user = UserSerializer(user, many=False).data

    return Response(serialized_user)
```

## DRF Serializers

- Allow complex data (e.g. querysets, model instances, etc...) to be converted to native Python datatypes that can be easily rendered into response content types such as `JSON` and `XML`
- Also allow "deserialization" to validate parsed data and convert back to the complex type.
- DRF's Serializers work similar to Django's `Form` and `ModelForm` classes.
- `Serializer` class gives you a powerful, generic way to control the output of the responses.
- `ModelSerializer` class provides a useful shortcut for creating serializers that deal with model instances and querysets.

- [DRF Serializers Documentation](https://www.django-rest-framework.org/api-guide/serializers/)

## DRF Serializer Fields

> Each field in a Form class is responsible not only for validating data, but also for "cleaning" it - normalizing it to a consistent format.
>
> &mdash; <cite>Django documentation</cite>

DRF serializer fields handle:

- converting between primitive values and internal datatypes
- validating input values
- retrieving and setting the values from their parent objects.

These are the serializer fields available in DRF:

- Boolean fields
  - BooleanField
  - NullBooleanField - also accepts `None` as a valid value.
- String fields
  - CharField
  - EmailField
  - RegexField
  - SlugField
  - URLField
  - UUIDField
  - FilePathField
  - IPAddressField
- Numeric Fields
  - IntegerField
  - FloatField
  - DecimalField
- Date and time fields
  - DateTimeField
  - DateField
  - TimeField
  - DurationField
- Choice selection fields
  - ChoiceField - same as a set of literal types in TS
  - MultipleChoiceField - can choose none, one, or many values from the set
- File upload fields
  - FieldField
  - ImageField
- Composite fields
  - ListField
  - DictField
  - HStoreField - A preconfigured `DictField` that is compatible with Django's postgres `HStoreField`.
  - JSONField
- Miscellaneous fields

  - ReadOnlyField - used by default with `ModelSerializer` when including field names that relate to an attribute rather than a model field
  - HiddenField - does not take a value from a user input, but from a default value or callable.
  - ModelField - generally intended for internal use.
  - SerializerMethodField - a read-only field that gets its value from calling the corresponding method. By default, DRF will call the method named `get_<field_name>`.

    ```python
    from django.contrib.auth.models import User
    from django.utils.timezone import now
    from rest_framework import serializers

    class UserSerializer(serializers.ModelSerializer):
        days_since_joined = serializers.SerializerMethodField()

        class Meta:
            model = User
            fields = '__all__'

        def get_days_since_joined(self, obj):
            return (now() - obj.date_joined).days

    ```

- Custom fields
  - [Examples for creating DRF Serializer custom fields](https://www.django-rest-framework.org/api-guide/fields/#examples)
