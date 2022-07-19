import factory
from django.utils.timezone import datetime

from backend.core.schema import FirestoreUserProfile

factory.Faker._DEFAULT_LOCALE = "en_GB"


class FirestoreUserProfileFactory(factory.Factory):
    email = factory.Sequence(
        lambda n: "testing+userprofile{0}@startupworx.net".format(n)
    )
    created = factory.Faker(
        "date_time_between",
        start_date=datetime(2022, 4, 20),
    )

    class Meta:
        model = FirestoreUserProfile


class UserProfileFactory(factory.django.DjangoModelFactory):
    firebase_auth_user_id = factory.Sequence(lambda n: "{0}".format(n))
    email = factory.Sequence(
        lambda n: "testing+userprofile{0}@startupworx.net".format(n)
    )

    class Meta:
        model = "core.UserProfile"
        django_get_or_create = (
            "firebase_auth_user_id",
            "email",
        )
