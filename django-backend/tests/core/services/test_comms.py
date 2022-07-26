import pytest
from django.conf import settings

from backend.core.models import MobileAppUser
from backend.core.services import SyncMailingList


@pytest.mark.vcr
@pytest.mark.django_db
def test_sync_mailing_list(user_profile_factory):
    assert settings.MAILERLITE_GROUP == "testing"

    for i in range(5):
        user_profile_factory(subscribed_to_mailing_list=True, mailing_list_id=i)

    for _ in range(5):
        user_profile_factory(subscribed_to_mailing_list=False)

    assert MobileAppUser.objects.count() == 10
    assert MobileAppUser.objects.filter(subscribed=True).count() == 5

    result = SyncMailingList().run()

    assert result.success

    # Now all users should be subscribed
    assert MobileAppUser.objects.filter(subscribed=True).count() == 10

    # All users should have a mailing list ID
    all_users = MobileAppUser.objects.all()
    assert all(
        [
            user.mailing_list_id is not None and user.mailing_list_id != ""
            for user in all_users
        ]
    )
