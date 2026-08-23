from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('apps.accounts.urls')),
    path('',include('apps.addresses.urls')),
    path('',include('apps.cart.urls')),
    path('',include('apps.categories.urls')),
    path('',include('apps.coupons.urls')),
    path('',include('apps.notifications.urls')),
    path('',include('apps.orders.urls')),
    path('',include('apps.payments.urls')),
    path('',include('apps.products.urls')),
    path('',include('apps.reviews.urls')),
    path('',include('apps.wishlist.urls')),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
