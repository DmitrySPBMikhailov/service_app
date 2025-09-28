from rest_framework.viewsets import ReadOnlyModelViewSet
from .models import Subscription
from .serializers import SubscriptionSerializer
from django.db.models import Sum
from django.core.cache import cache
from django.conf import settings


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

        price_cache = cache.get(settings.PRICE_CACHE_NAME)

        if price_cache:
            total_price = price_cache
        else:
            total_price = queryset.aggregate(total=Sum("price")).get("total")
            cache.set(settings.PRICE_CACHE_NAME, total_price, 60 * 60)

        response_data = {"result": response.data}
        response_data["total_amount"] = total_price
        response.data = response_data
        return response
