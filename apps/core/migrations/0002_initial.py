# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'CategoriaProducto'
        db.create_table('Categoria_producto', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('categoria', self.gf('django.db.models.fields.CharField')(max_length=45L, db_column='Categoria', blank=True)),
        ))
        db.send_create_signal(u'core', ['CategoriaProducto'])

        # Adding model 'Logged'
        db.create_table('Logged', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('session_key', self.gf('django.db.models.fields.CharField')(max_length=100L, blank=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('access', self.gf('django.db.models.fields.CharField')(max_length=45L, blank=True)),
        ))
        db.send_create_signal(u'core', ['Logged'])

        # Adding model 'Producto'
        db.create_table('Producto', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('categoria_producto', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.CategoriaProducto'], db_column='Categoria_producto_id')),
            ('codigo', self.gf('django.db.models.fields.CharField')(max_length=45L, blank=True)),
            ('descripcion', self.gf('django.db.models.fields.CharField')(max_length=45L, blank=True)),
        ))
        db.send_create_signal(u'core', ['Producto'])

        # Adding model 'Rango'
        db.create_table('Rango', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('min', self.gf('django.db.models.fields.IntegerField')(null=True, db_column='Min', blank=True)),
            ('max', self.gf('django.db.models.fields.IntegerField')(null=True, db_column='Max', blank=True)),
            ('costo', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'core', ['Rango'])

        # Adding model 'Sucursal'
        db.create_table('Sucursal', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=150L, blank=True)),
            ('estado', self.gf('django.db.models.fields.CharField')(max_length=100L, blank=True)),
            ('pais', self.gf('django.db.models.fields.CharField')(max_length=50L, blank=True)),
            ('tel', self.gf('django.db.models.fields.CharField')(max_length=50L, blank=True)),
            ('almacen_admipaq', self.gf('django.db.models.fields.CharField')(max_length=100L, blank=True)),
            ('iva', self.gf('django.db.models.fields.CharField')(max_length=50L, blank=True)),
            ('direccion', self.gf('django.db.models.fields.CharField')(max_length=100L, blank=True)),
            ('num_int', self.gf('django.db.models.fields.CharField')(max_length=50L, blank=True)),
            ('num_ext', self.gf('django.db.models.fields.CharField')(max_length=45L, blank=True)),
            ('folio_sucursal', self.gf('django.db.models.fields.CharField')(max_length=50L, blank=True)),
            ('sucursal_inventario', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.SucursalInventario'])),
            ('descuento', self.gf('django.db.models.fields.CharField')(max_length=10L, blank=True)),
        ))
        db.send_create_signal(u'core', ['Sucursal'])

        # Adding model 'ClienteDatos'
        db.create_table('cliente_datos', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=100L, blank=True)),
            ('telefono', self.gf('django.db.models.fields.CharField')(max_length=100L, db_column='Telefono', blank=True)),
            ('correo', self.gf('django.db.models.fields.CharField')(max_length=100L, blank=True)),
            ('pais', self.gf('django.db.models.fields.CharField')(max_length=50L, blank=True)),
            ('estado', self.gf('django.db.models.fields.CharField')(max_length=50L, blank=True)),
            ('sucursal', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Sucursal'], db_column='Sucursal_id')),
            ('descuentos', self.gf('django.db.models.fields.CharField')(max_length=45L, blank=True)),
        ))
        db.send_create_signal(u'core', ['ClienteDatos'])

        # Adding model 'ClienteFacturacion'
        db.create_table('cliente_facturacion', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('rfc', self.gf('django.db.models.fields.CharField')(max_length=150L, blank=True)),
            ('direccion', self.gf('django.db.models.fields.CharField')(max_length=150L, blank=True)),
            ('calle', self.gf('django.db.models.fields.CharField')(max_length=150L, blank=True)),
            ('colonia', self.gf('django.db.models.fields.CharField')(max_length=150L, blank=True)),
            ('num_int', self.gf('django.db.models.fields.CharField')(max_length=45L, blank=True)),
            ('num_ext', self.gf('django.db.models.fields.CharField')(max_length=45L, blank=True)),
            ('cod_postal', self.gf('django.db.models.fields.CharField')(max_length=45L, blank=True)),
            ('municipio', self.gf('django.db.models.fields.CharField')(max_length=45L, blank=True)),
            ('cliente_datos', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.ClienteDatos'])),
        ))
        db.send_create_signal(u'core', ['ClienteFacturacion'])

        # Adding model 'Eventos'
        db.create_table('eventos', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre_evento', self.gf('django.db.models.fields.CharField')(max_length=45L, blank=True)),
        ))
        db.send_create_signal(u'core', ['Eventos'])

        # Adding model 'Log'
        db.create_table('log', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('usuario', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Usuario'])),
            ('eventos', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Eventos'])),
        ))
        db.send_create_signal(u'core', ['Log'])

        # Adding model 'SucursalInventario'
        db.create_table('sucursal_inventario', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('producto', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Producto'], db_column='Producto_id')),
            ('existencia', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('rango', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Rango'], db_column='Rango_id')),
        ))
        db.send_create_signal(u'core', ['SucursalInventario'])

        # Adding model 'Usuario'
        db.create_table('usuario', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=500L, blank=True)),
            ('rol', self.gf('django.db.models.fields.CharField')(max_length=150L, blank=True)),
            ('email', self.gf('django.db.models.fields.CharField')(max_length=100L, blank=True)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=300L, blank=True)),
            ('tel_cel', self.gf('django.db.models.fields.CharField')(max_length=100L, blank=True)),
            ('logged', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Logged'], db_column='Logged_id')),
        ))
        db.send_create_signal(u'core', ['Usuario'])

        # Adding model 'UsuarioHasSucursal'
        db.create_table('usuario_has_Sucursal', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('usuario', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Usuario'])),
            ('sucursal', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Sucursal'], db_column='Sucursal_id')),
        ))
        db.send_create_signal(u'core', ['UsuarioHasSucursal'])

        # Adding model 'UsuarioSucursal'
        db.create_table('usuario_sucursal', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tel_residencia', self.gf('django.db.models.fields.CharField')(max_length=85L, blank=True)),
            ('bono', self.gf('django.db.models.fields.CharField')(max_length=45L, blank=True)),
            ('porciento_comision', self.gf('django.db.models.fields.CharField')(max_length=45L, blank=True)),
            ('salario_real', self.gf('django.db.models.fields.CharField')(max_length=45L, blank=True)),
            ('num_seguro_social', self.gf('django.db.models.fields.CharField')(max_length=100L, blank=True)),
            ('direccion', self.gf('django.db.models.fields.CharField')(max_length=200L, blank=True)),
            ('nombre_aval', self.gf('django.db.models.fields.CharField')(max_length=200L, blank=True)),
            ('tel_aval', self.gf('django.db.models.fields.CharField')(max_length=100L, blank=True)),
            ('usuario', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Usuario'])),
        ))
        db.send_create_signal(u'core', ['UsuarioSucursal'])

        # Adding model 'UsuarioSucursalHasSucursal'
        db.create_table('usuario_sucursal_has_Sucursal', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('usuario_sucursal', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.UsuarioSucursal'])),
            ('sucursal', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Sucursal'], db_column='Sucursal_id')),
        ))
        db.send_create_signal(u'core', ['UsuarioSucursalHasSucursal'])


    def backwards(self, orm):
        # Deleting model 'CategoriaProducto'
        db.delete_table('Categoria_producto')

        # Deleting model 'Logged'
        db.delete_table('Logged')

        # Deleting model 'Producto'
        db.delete_table('Producto')

        # Deleting model 'Rango'
        db.delete_table('Rango')

        # Deleting model 'Sucursal'
        db.delete_table('Sucursal')

        # Deleting model 'ClienteDatos'
        db.delete_table('cliente_datos')

        # Deleting model 'ClienteFacturacion'
        db.delete_table('cliente_facturacion')

        # Deleting model 'Eventos'
        db.delete_table('eventos')

        # Deleting model 'Log'
        db.delete_table('log')

        # Deleting model 'SucursalInventario'
        db.delete_table('sucursal_inventario')

        # Deleting model 'Usuario'
        db.delete_table('usuario')

        # Deleting model 'UsuarioHasSucursal'
        db.delete_table('usuario_has_Sucursal')

        # Deleting model 'UsuarioSucursal'
        db.delete_table('usuario_sucursal')

        # Deleting model 'UsuarioSucursalHasSucursal'
        db.delete_table('usuario_sucursal_has_Sucursal')


    models = {
        u'core.categoriaproducto': {
            'Meta': {'object_name': 'CategoriaProducto', 'db_table': "'Categoria_producto'"},
            'categoria': ('django.db.models.fields.CharField', [], {'max_length': '45L', 'db_column': "'Categoria'", 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'core.clientedatos': {
            'Meta': {'object_name': 'ClienteDatos', 'db_table': "'cliente_datos'"},
            'correo': ('django.db.models.fields.CharField', [], {'max_length': '100L', 'blank': 'True'}),
            'descuentos': ('django.db.models.fields.CharField', [], {'max_length': '45L', 'blank': 'True'}),
            'estado': ('django.db.models.fields.CharField', [], {'max_length': '50L', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '100L', 'blank': 'True'}),
            'pais': ('django.db.models.fields.CharField', [], {'max_length': '50L', 'blank': 'True'}),
            'sucursal': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Sucursal']", 'db_column': "'Sucursal_id'"}),
            'telefono': ('django.db.models.fields.CharField', [], {'max_length': '100L', 'db_column': "'Telefono'", 'blank': 'True'})
        },
        u'core.clientefacturacion': {
            'Meta': {'object_name': 'ClienteFacturacion', 'db_table': "'cliente_facturacion'"},
            'calle': ('django.db.models.fields.CharField', [], {'max_length': '150L', 'blank': 'True'}),
            'cliente_datos': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.ClienteDatos']"}),
            'cod_postal': ('django.db.models.fields.CharField', [], {'max_length': '45L', 'blank': 'True'}),
            'colonia': ('django.db.models.fields.CharField', [], {'max_length': '150L', 'blank': 'True'}),
            'direccion': ('django.db.models.fields.CharField', [], {'max_length': '150L', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'municipio': ('django.db.models.fields.CharField', [], {'max_length': '45L', 'blank': 'True'}),
            'num_ext': ('django.db.models.fields.CharField', [], {'max_length': '45L', 'blank': 'True'}),
            'num_int': ('django.db.models.fields.CharField', [], {'max_length': '45L', 'blank': 'True'}),
            'rfc': ('django.db.models.fields.CharField', [], {'max_length': '150L', 'blank': 'True'})
        },
        u'core.eventos': {
            'Meta': {'object_name': 'Eventos', 'db_table': "'eventos'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre_evento': ('django.db.models.fields.CharField', [], {'max_length': '45L', 'blank': 'True'})
        },
        u'core.log': {
            'Meta': {'object_name': 'Log', 'db_table': "'log'"},
            'date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'eventos': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Eventos']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'usuario': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Usuario']"})
        },
        u'core.logged': {
            'Meta': {'object_name': 'Logged', 'db_table': "'Logged'"},
            'access': ('django.db.models.fields.CharField', [], {'max_length': '45L', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'session_key': ('django.db.models.fields.CharField', [], {'max_length': '100L', 'blank': 'True'})
        },
        u'core.producto': {
            'Meta': {'object_name': 'Producto', 'db_table': "'Producto'"},
            'categoria_producto': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.CategoriaProducto']", 'db_column': "'Categoria_producto_id'"}),
            'codigo': ('django.db.models.fields.CharField', [], {'max_length': '45L', 'blank': 'True'}),
            'descripcion': ('django.db.models.fields.CharField', [], {'max_length': '45L', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'core.rango': {
            'Meta': {'object_name': 'Rango', 'db_table': "'Rango'"},
            'costo': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'Max'", 'blank': 'True'}),
            'min': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'Min'", 'blank': 'True'})
        },
        u'core.sucursal': {
            'Meta': {'object_name': 'Sucursal', 'db_table': "'Sucursal'"},
            'almacen_admipaq': ('django.db.models.fields.CharField', [], {'max_length': '100L', 'blank': 'True'}),
            'descuento': ('django.db.models.fields.CharField', [], {'max_length': '10L', 'blank': 'True'}),
            'direccion': ('django.db.models.fields.CharField', [], {'max_length': '100L', 'blank': 'True'}),
            'estado': ('django.db.models.fields.CharField', [], {'max_length': '100L', 'blank': 'True'}),
            'folio_sucursal': ('django.db.models.fields.CharField', [], {'max_length': '50L', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iva': ('django.db.models.fields.CharField', [], {'max_length': '50L', 'blank': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '150L', 'blank': 'True'}),
            'num_ext': ('django.db.models.fields.CharField', [], {'max_length': '45L', 'blank': 'True'}),
            'num_int': ('django.db.models.fields.CharField', [], {'max_length': '50L', 'blank': 'True'}),
            'pais': ('django.db.models.fields.CharField', [], {'max_length': '50L', 'blank': 'True'}),
            'sucursal_inventario': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.SucursalInventario']"}),
            'tel': ('django.db.models.fields.CharField', [], {'max_length': '50L', 'blank': 'True'})
        },
        u'core.sucursalinventario': {
            'Meta': {'object_name': 'SucursalInventario', 'db_table': "'sucursal_inventario'"},
            'existencia': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'producto': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Producto']", 'db_column': "'Producto_id'"}),
            'rango': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Rango']", 'db_column': "'Rango_id'"})
        },
        u'core.usuario': {
            'Meta': {'object_name': 'Usuario', 'db_table': "'usuario'"},
            'email': ('django.db.models.fields.CharField', [], {'max_length': '100L', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logged': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Logged']", 'db_column': "'Logged_id'"}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '500L', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '300L', 'blank': 'True'}),
            'rol': ('django.db.models.fields.CharField', [], {'max_length': '150L', 'blank': 'True'}),
            'tel_cel': ('django.db.models.fields.CharField', [], {'max_length': '100L', 'blank': 'True'})
        },
        u'core.usuariohassucursal': {
            'Meta': {'object_name': 'UsuarioHasSucursal', 'db_table': "'usuario_has_Sucursal'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sucursal': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Sucursal']", 'db_column': "'Sucursal_id'"}),
            'usuario': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Usuario']"})
        },
        u'core.usuariosucursal': {
            'Meta': {'object_name': 'UsuarioSucursal', 'db_table': "'usuario_sucursal'"},
            'bono': ('django.db.models.fields.CharField', [], {'max_length': '45L', 'blank': 'True'}),
            'direccion': ('django.db.models.fields.CharField', [], {'max_length': '200L', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre_aval': ('django.db.models.fields.CharField', [], {'max_length': '200L', 'blank': 'True'}),
            'num_seguro_social': ('django.db.models.fields.CharField', [], {'max_length': '100L', 'blank': 'True'}),
            'porciento_comision': ('django.db.models.fields.CharField', [], {'max_length': '45L', 'blank': 'True'}),
            'salario_real': ('django.db.models.fields.CharField', [], {'max_length': '45L', 'blank': 'True'}),
            'tel_aval': ('django.db.models.fields.CharField', [], {'max_length': '100L', 'blank': 'True'}),
            'tel_residencia': ('django.db.models.fields.CharField', [], {'max_length': '85L', 'blank': 'True'}),
            'usuario': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Usuario']"})
        },
        u'core.usuariosucursalhassucursal': {
            'Meta': {'object_name': 'UsuarioSucursalHasSucursal', 'db_table': "'usuario_sucursal_has_Sucursal'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sucursal': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Sucursal']", 'db_column': "'Sucursal_id'"}),
            'usuario_sucursal': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.UsuarioSucursal']"})
        }
    }

    complete_apps = ['core']