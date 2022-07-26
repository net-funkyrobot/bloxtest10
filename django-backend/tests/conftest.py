import pytest

from tests import factories


@pytest.fixture
def fs_user_profile_factory():
    """Generate fake Firestore user profile documents."""
    return factories.FirestoreUserProfileFactory


@pytest.fixture
def user_profile_factory():
    """Generate database user profile model instances."""
    return factories.MobileAppUserFactory
