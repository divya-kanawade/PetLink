from __future__ import annotations

from rest_framework.routers import DefaultRouter

from . import api_views

router = DefaultRouter()
router.register("pets", api_views.PetListingViewSet)
router.register("lost", api_views.LostPetViewSet)
router.register("health-records", api_views.HealthRecordViewSet)
router.register("products", api_views.ProductViewSet)
router.register("posts", api_views.BlogPostViewSet)

urlpatterns = router.urls


