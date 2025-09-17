from rest_framework.viewsets import ReadOnlyModelViewSet
from .models import Subscription
from .serializers import SubscriptionSerializer


# Create your views here.
class SubscriptionView(ReadOnlyModelViewSet):
    queryset = Subscription.objects.all().prefetch_related("client")
    serializer_class = SubscriptionSerializer
