from odoo import api, fields, models
from odoo.exceptions import ValidationError


class ManufacturingModelInherit(models.Model):
    _inherit = 'mrp.production'

    production_in_meters = fields.Float('Production In Meters')
    no_of_reels = fields.Integer('No. of Reels')
    reel_detail_ids = fields.One2many('reel.detail', 'mrp_id')

    # This function is used to create manufacturing reel detail
    def create_reel(self):
        if not self.reel_detail_ids:
            raise ValidationError('Please add at least one reel detail')
        elif not self.lot_producing_id:
            raise ValidationError('Please first create lot serial number !')
        else:
            for line in self.reel_detail_ids:
                line.sequence_no = str(self.lot_producing_id.name) + "-" + str(
                    self.env['ir.sequence'].next_by_code('reel.detail'))


# reel detail model defined here
class ReelDetail(models.Model):
    _name = 'reel.detail'

    sequence_no = fields.Char('Sequence')
    worker_id = fields.Many2one('res.partner', 'Worker')
    weight = fields.Float('Weight')
    description = fields.Text('Description')
    mrp_id = fields.Many2one('mrp.production')
