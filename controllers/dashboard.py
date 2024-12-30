from odoo import http
from odoo.http import request
import json

class DashboardController(http.Controller):

    @http.route('/gema/dashboard/contracts', type='http', auth="user", website=True)
    def dashboard_page(self, **kw):
        contracts = request.env['gema.contracts'].search([])
        return request.render(
            'GEMA.contracts_dashboard',
            {'contracts': contracts}
        )
    
    @http.route('/gema/dashboard/prueba', type='http', auth="user", website=True)
    def dashboard_embebe(self, **kw):
        return request.render(
            'GEMA.embedded_dashboard_view',
        )
