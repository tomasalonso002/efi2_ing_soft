from .views import UserClienteViewSets, UserVendedorViewSets, UserClienteGetViewSets, UserVendedorGetViewSets, ListaDeseosProductosPostViewSets, ListaDeseosProductosViewSets            
from rest_framework.routers import DefaultRouter
from django.urls import path 
router = DefaultRouter()

router.register('cliente', UserClienteViewSets, basename='user-cliente-api')
router.register('cliente-get', UserClienteGetViewSets, basename='user-cliente-get-api')

router.register('vendedor', UserVendedorViewSets, basename='user-vendedor-api')
router.register('vendedor-get', UserVendedorGetViewSets, basename='user-vendedor-get-api')

router.register('lista-deseos', ListaDeseosProductosPostViewSets, basename='lista-deseos-api')
router.register('lista-deseos-get', ListaDeseosProductosViewSets, basename='lista-deseos-get-api')



urlpatterns = [
    *router.urls,
    path(
        'cliente/1/eliminado_logico/',
        UserClienteViewSets.as_view({'post': 'eliminado_logico'}),
        name='user-cliente-delete-api'
    ),
    path(
        'vendedor/1/eliminado_logico/',
        UserClienteViewSets.as_view({'post': 'eliminado_logico'}),
        name='user-vendedor-delete-api'
    ),

    path(
        'lista-deseos/1/eliminado_logico/',
        ListaDeseosProductosPostViewSets.as_view({'post': 'eliminado_logico'}),
        name='lista-deseos-delete-api'
    ),
]