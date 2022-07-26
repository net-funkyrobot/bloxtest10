from django.conf import settings
from django.core.paginator import Paginator
from mailerlite import MailerLiteApi

from backend.core.models import MobileAppUser
from backend.core.services.base import ServiceResult, catch_service_errors

_MAILERLITE_API_PAGE_SIZE = 50


class SyncMailingList:
    @catch_service_errors
    def run(self) -> ServiceResult[None]:
        client = MailerLiteApi(settings.MAILERLITE_API_TOKEN)
        group = settings.MAILERLITE_GROUP

        # Check group exists, get ID, create it if necessary
        all_groups = client.groups.all()
        group_matches = [g for g in all_groups if g.name == group]

        if group_matches:
            group_id = group_matches[0].id
        else:
            new_group = client.groups.create(name=group)
            group_id = new_group.id

        # Query for new users, paginate, bulk subscribe users using client
        new_user_emails = MobileAppUser.objects.filter(
            subscribed=False,
            has_unsubscribed=False,
        ).values_list("email", flat=True)

        pages = Paginator(new_user_emails, _MAILERLITE_API_PAGE_SIZE)

        for page_num in range(1, pages.num_pages + 1):
            page = pages.page(page_num)

            new_subscribers = client.groups.add_subscribers(
                group_id=group_id,
                subscribers_data=[{"email": email, "name": email} for email in page],
                autoresponders=False,
                resubscribe=True,
            )

            # Update flag and Mailerlite ID on models for successful subscribe
            for sub in new_subscribers:
                MobileAppUser.objects.update(
                    email=sub.email,
                    susbcribed=True,
                    mailing_list_id=sub.id,
                )

        return ServiceResult(success=True)
