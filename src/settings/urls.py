"""
URL configuration for settings project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView 

from usuarios.routers import router as usuarios_routers
from catalogo.routers import router as catalogo_routers
from proveedores.routers import router as proveedores_routers
from compras.routers import router as compras_routers
from ventas.routers import router as ventas_routers

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('admin/', admin.site.urls),

    path('api/usuarios/', include(usuarios_routers.urls)),
    path('api/catalogo/', include(catalogo_routers.urls)),
    path('api/proveedores/', include(proveedores_routers.urls)),
    path('api/compras/', include(compras_routers.urls)),
    path('api/ventas/', include(ventas_routers.urls)),
]

