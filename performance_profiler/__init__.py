from odoo import api

from .profiler import profile

api.profile = profile
