from rest_framework.viewsets import ReadOnlyModelViewSet
from .models import Subscription
from .serializers import SubscriptionSerializer
from django.db.models import Sum


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
            "price",
            # "service__full_price",
        )
    )
    serializer_class = SubscriptionSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        response = super().list(request, *args, **kwargs)

        response_data = {"result": response.data}
        response_data["total_amount"] = queryset.aggregate(total=Sum("price")).get(
            "total"
        )
        response.data = response_data
        return response
