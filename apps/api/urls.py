from tastypie.api import Api
from apps.api.resource import *

v1_api = Api(api_name='v1')

v1_api.register(UsuarioResource())
v1_api.register(LoginResource())
v1_api.register(ClienteResource())
v1_api.register(SucursalResource())
v1_api.register(ClienteFacturacionResource())
#v1_api.register(SucursalInventarioResource())
v1_api.register(ProductoResource())
v1_api.register(CategoriaProductoResource())
v1_api.register(MunicipioResource())
v1_api.register(EstadosResource())
v1_api.register(RangoResource())
v1_api.register(InventarioResource())
v1_api.register(ProductoHasRangoesource())
v1_api.register(VentaResource())
v1_api.register(VentaClienteResource())
v1_api.register(UsuarioSucursalResource())
v1_api.register(UsuarioHasSucursalResource())
v1_api.register(AsignacionSupervisorPlazaResource())
v1_api.register(VentaPublicoResource())
v1_api.register(HistorialVentaResource())
v1_api.register(VentaUsuarioSucursalResource())
v1_api.register(ClienteReporteResource())
v1_api.register(CambioResource())
v1_api.register(AjusteInventarioResource())
#v1_api.register(VentaHasProductoResource())


