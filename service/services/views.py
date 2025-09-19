from rest_framework.viewsets import ReadOnlyModelViewSet
from .models import Subscription
from .serializers import SubscriptionSerializer


# Create your views here.
class SubscriptionView(ReadOnlyModelViewSet):
    queryset = (
        Subscription.objects.select_related("client__user", "plan")
        .all()
        .only(
            "id",
            "plan_id",
            "client__company_name",
            "client__user__email",
            "plan__play_type",
            "plan__discount_percent",
        )
    )
    serializer_class = SubscriptionSerializer
