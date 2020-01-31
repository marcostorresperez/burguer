# -*- coding: utf-8 -*-

from odoo import models, fields, api, tools
from openerp.exceptions import ValidationError, Warning
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


# class burguer(models.Model):
#     _name = 'burguer.burguer'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100

class productor(models.Model):
    _name = 'burguer.productor'

    name = fields.Char()
    produccion = fields.Integer()
    recurso = fields.Many2one('burguer.recurso')
    description = fields.Text()
    nivel = fields.Integer()
    image = fields.Binary()
    jugador = fields.Many2one('res.partner')
    nombre_jugador = fields.Char(compute='_get_nombre_jugador')
    image_small = fields.Binary(compute="_resize_image", store=True)
    template = fields.Boolean(readonly=True)
    color = fields.Integer(compute='_get_color')

    @api.multi
    def level_up(self):
        for r in self:
            nivel = r.nivel + 1
            produccion = r.produccion + 7
            r.write({'nivel': nivel, 'produccion': produccion})

    @api.multi
    def level_cero(self):
        for r in self:
            nivel = 1
            produccion = 7
            r.write({'nivel': nivel, 'produccion': produccion})

    @api.multi
    def _get_color(self):
        for i in self:
            if i.template:
                i.color = 4
            else:
                i.color = 3

    @api.multi
    def _get_nombre_jugador(self):
        for i in self:
            if i.template == False:
                i.nombre_jugador = i.jugador.name

    @api.depends('image')
    def _resize_image(self):
        for i in self:
            image = i.image
            data = tools.image_get_resized_images(image)
            i.image_small = data["image_small"]

    @api.constrains('nivel')
    def _mira_nivel(self):
        for i in self:
            if i.nivel >= 6:
                raise ValidationError("El nivel del edificio ya está al máximo")

    @api.onchange('nivel')
    def _check_cambio(self):
        anuncio = {
            'title': "¿Estás seguro?",
            'message': "Los recursos usados no se podrán recuperar"
        }
        res = {

        }
        return {'value': res, 'warning': anuncio}


class almacen(models.Model):
    _name = 'burguer.almacen'

    name = fields.Char()
    capacidad = fields.Integer()
    stock = fields.Integer(compute='_compute_stock')
    nivel = fields.Integer()
    nombre_jugador = fields.Char(compute='_get_nombre_jugador')
    raws = fields.One2many('burguer.raws', 'almacen', ondelete='cascade')
    description = fields.Text()
    image = fields.Binary()
    jugador = fields.Many2one('res.partner')
    template = fields.Boolean(readonly=True)
    image_small = fields.Binary(compute="_resize_image", store=True)

    @api.multi
    def level_up(self):
        for r in self:
            nivel = r.nivel + 1
            capacidad = r.capacidad + 50
            r.write({'nivel': nivel, 'capacidad': capacidad})

    @api.multi
    def level_cero(self):
        for r in self:
            nivel = 1
            capacidad = 50
            r.write({'nivel': nivel, 'capacidad': capacidad})

    @api.depends('image')
    def _resize_image(self):
        for i in self:
            image = i.image
            data = tools.image_get_resized_images(image)
            i.image_small = data["image_small"]

    @api.onchange('nivel')
    def _check_cambio(self):
        anuncio = {
            'title': "¿Estás seguro?",
            'message': "Los recursos usados no se podrán recuperar"
        }
        res = {

        }
        return {'value': res, 'warning': anuncio}

    @api.model
    def create(self, values):
        new_id = super(almacen, self).create(values)
        self.env['burguer.raws'].create(
            {'name': 'Vegetales', 'almacen': new_id.id, 'raw': self.env.ref('burguer.lechuga').id, 'cantidad': 20
             }
        )
        self.env['burguer.raws'].create(
            {'name': 'Carne', 'almacen': new_id.id, 'raw': self.env.ref('burguer.cerdo').id, 'cantidad': 15
             }
        )
        self.env['burguer.raws'].create(
            {'name': 'Queso', 'almacen': new_id.id, 'raw': self.env.ref('burguer.cabra').id, 'cantidad': 10
             }
        )
        self.env['burguer.raws'].create(
            {'name': 'Pan', 'almacen': new_id.id, 'raw': self.env.ref('burguer.pan').id, 'cantidad': 30
             }
        )
        self.env['burguer.raws'].create(
            {'name': 'Dinero', 'almacen': new_id.id, 'raw': self.env.ref('burguer.dinero').id, 'cantidad': 100
             }
        )

        return new_id

    @api.multi
    def _compute_stock(self):
        suma = 0
        for record in self:
            for raws in record.raws:
                if not raws.name == 'Dinero':
                    suma += raws.cantidad
            record.stock = suma

    @api.constrains('nivel')
    def _mira_nivel(self):
        for i in self:
            if i.nivel >= 6:
                raise ValidationError("El nivel del edificio ya está al máximo")

    @api.multi
    def _get_nombre_jugador(self):
        for i in self:
            if i.template == False:
                i.nombre_jugador = i.jugador.name


# Tots els One2Many deuen tindre les linies CONTEXT


class tienda(models.Model):
    _name = 'burguer.tienda'

    name = fields.Char()
    nivel = fields.Integer()
    produccion = fields.Integer()
    jugador = fields.Many2one('res.partner')
    nombre_jugador = fields.Char(compute='_get_nombre_jugador')
    template = fields.Boolean(readonly=True)
    image = fields.Binary()
    image_small = fields.Binary(compute="_resize_image", store=True)

    @api.multi
    def level_up(self):
        for r in self:
            nivel = r.nivel + 1
            produccion = r.produccion + 10
            r.write({'nivel': nivel, 'produccion': produccion})

    @api.multi
    def level_cero(self):
        for r in self:
            nivel = 1
            produccion = 10
            r.write({'nivel': nivel, 'produccion': produccion})

    @api.onchange('nivel')
    def _check_cambio(self):
        anuncio = {
            'title': "¿Estás seguro?",
            'message': "Los recursos usados no se podrán recuperar"
        }
        res = {

        }
        return {'value': res, 'warning': anuncio}

    @api.depends('image')
    def _resize_image(self):
        for i in self:
            image = i.image
            data = tools.image_get_resized_images(image)
            i.image_small = data["image_small"]

    @api.constrains('nivel')
    def _mira_nivel(self):
        for i in self:
            if i.nivel >= 6:
                raise ValidationError("El nivel del edificio ya está al máximo")

    @api.multi
    def _get_nombre_jugador(self):
        for i in self:
            if i.template == False:
                i.nombre_jugador = i.jugador.name


class raw(models.Model):
    _name = 'burguer.raw'

    name = fields.Char()
    image = fields.Binary()
    image_small = fields.Binary(compute="_resize_image", store=True)
    template = fields.Boolean(readonly=True)
    color = fields.Integer(compute='_get_color')

    @api.multi
    def _get_color(self):
        for i in self:
            if i.template:
                i.color = 4
            else:
                i.color = 3

    @api.depends('image')
    def _resize_image(self):
        for i in self:
            image = i.image
            data = tools.image_get_resized_images(image)
            i.image_small = data["image_small"]


class raws(models.Model):
    _name = 'burguer.raws'

    name = fields.Char()
    almacen = fields.Many2one('burguer.almacen')
    raw = fields.Many2one('burguer.raw')
    cantidad = fields.Integer()
    # clan = fields.Many2many('burguer.clan','raws')
    image = fields.Binary(related='raw.image', store=True)
    image_small = fields.Binary(compute="_resize_image", store=True)

    @api.depends('image')
    def _resize_image(self):
        for i in self:
            image = i.image
            data = tools.image_get_resized_images(image)
            i.image_small = data["image_small"]


class coste_productor(models.Model):
    _name = 'burguer.coste_productor'

    name = fields.Char()
    productor = fields.Many2one('burguer.productor')
    dinero = fields.Many2one('burguer.raw')
    cantidad = fields.Integer()
    tiempo = fields.Integer()


class coste_almacen(models.Model):
    _name = 'burguer.coste_almacen'

    name = fields.Char()
    almacen = fields.Many2one('burguer.almacen')
    dinero = fields.Many2one('burguer.raw')
    cantidad = fields.Integer()
    tiempo = fields.Integer()


class coste_tienda(models.Model):
    _name = 'burguer.coste_tienda'

    name = fields.Char()
    tienda = fields.Many2one('burguer.tienda')
    dinero = fields.Many2one('burguer.raw')
    cantidad = fields.Integer()
    tiempo = fields.Integer()


class jugador(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'

    clan = fields.Many2one('burguer.clan')
    productor = fields.One2many('burguer.productor', 'jugador', ondelete='cascade')
    tiendas = fields.One2many('burguer.tienda', 'jugador', ondelete='cascade')
    dinero = fields.Integer(compute='get_dinero', ondelete='cascade')
    almacenes = fields.One2many('burguer.almacen', 'jugador', ondelete='cascade')
    es_jugador = fields.Boolean(default=False)
    evento = fields.Many2many('burguer.evento')

    @api.multi
    def add_tienda(self):
        for i in self:
            template = self.env.ref('burguer.iconburguer')
            self.env['burguer.tienda'].create({
                'name': "Tienda",
                'nivel': 1,
                'produccion': 3,
                'image': template.image,
                'jugador': i.id
            })

    @api.multi
    def get_dinero(self):
        for i in self:
            for almacen in i.almacenes:
                for raw in almacen.raws:
                    if raw.name == 'Dinero':
                        i.dinero = raw.cantidad

    @api.model
    def create(self, values):
        new_id = super(jugador, self).create(values)
        self.env['burguer.tienda'].create(
            {'name': "Tienda", 'jugador': new_id.id, 'nivel': 1, 'produccion': 3,
             'image': self.env.ref('burguer.iconburguer').image
             }
        )

        self.env['burguer.almacen'].create(
            {'name': 'Almacen', 'jugador': new_id.id, 'nivel': 1, 'capacidad': 500,
             'image': self.env.ref('burguer.iconalmacen').image
             }
        )
        self.env['burguer.productor'].create(
            {'name': 'Panaderia', 'jugador': new_id.id, 'produccion': self.env.ref('burguer.pan').id, 'nivel': 1,
             'image': self.env.ref('burguer.panaderia').image
             }
        )
        self.env['burguer.productor'].create(
            {'name': 'Huerta', 'jugador': new_id.id, 'produccion': self.env.ref('burguer.lechuga').id, 'nivel': 1,
             'image': self.env.ref('burguer.huerta').image
             }
        )
        self.env['burguer.productor'].create(
            {'name': 'Queseria', 'jugador': new_id.id, 'produccion': self.env.ref('burguer.cabra').id, 'nivel': 1,
             'image': self.env.ref('burguer.queseria').image
             }
        )
        self.env['burguer.productor'].create(
            {'name': 'Carniceria', 'jugador': new_id.id, 'produccion': self.env.ref('burguer.cerdo').id, 'nivel': 1,
             'image': self.env.ref('burguer.carniceria').image
             }
        )
        return new_id

    def update_raws(self):
        print("Update Raws")
        productor = self.env['burguer.productor'].search([('template', '=', False)])
        for p in productor:
            raws = p.jugador.raws
            for i in raws:
                q = i.cantidad + p.produccion
                if i.raw.id == p.raw.id:
                    i.write({'cantidad': q})


class clan(models.Model):
    _name = 'burguer.clan'

    name = fields.Char()
    players = fields.One2many('res.partner', 'clan')


# raws = fields.Many2many('burguer.raws',compute= '_get_raws')

# MANY2MANY COMPUTED
# @api.depends('raws')
# def _get_raws(self):
#   for r in self:
#      r.raws = r.players.mapped('raws')


class guerra(models.Model):
    _name = 'burguer.guerra'

    name = fields.Char()
    atacante = fields.Many2one('res.partner')
    defensor = fields.Many2one('res.partner')
    defensor = fields.Many2one('res.partner')
    raws_ataque = fields.Many2one('res.partner')
    raws_defensa = fields.Many2one('res.partner')
    estado = fields.Selection([('1', 'Inicio'), ('2', 'Selección de recursos'), ('3', 'Esperando'), ('4', 'Terminado')],
                              compute='_get_state')
    compute_date = fields.Date(compute="calcula_tiempo", store=False)
    compute_datetime = fields.Datetime(compute="calcula_tiempo", store=False)

    def _get_date(self):
        date = datetime.now() + timedelta(hours=3)
        return fields.Datetime.to_string(date)

    date = fields.Datetime(default=_get_date)
    finished = fields.Boolean()

    @api.depends()
    def _calcula_tiempo(self):
        for r in self:
            r.compute_date = fields.date.today()
            r.compute_datetime = fields.date.now()

    @api.model
    def create(self, values):
        new_id = super(clan, self).create(values)
        self.env['burguer.raws'].create({''})
        return new_id

    @api.multi
    def _get_state(self):
        for b in self:
            b.state = '1'
            if len(b.attack) > 0 and len(b.defend) > 0:
                b.state = '2'
            if len(b.characters_attack) > 0 and len(b.characters_defend) > 0:
                b.state = '3'
            if b.finished == True:
                b.state = '4'
            start = datetime.now()
            end = fields.Datetime.from_string(b.date)
            relative = relativedelta(end, start)
            if end > start:
                b.time_remaining = str(relative.hours) + ":" + str(relative.minutes)
            else:
                b.time_remaining = '00:00'


class evento(models.Model):
    _name = 'burguer.evento'

    name = fields.Char()
    fecha_inicio = fields.Date()
    fecha_fin = fields.Date()

    jugador = fields.Many2many('res.partner')