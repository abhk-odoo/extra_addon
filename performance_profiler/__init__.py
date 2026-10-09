from odoo import api

from .profiler import profile_class, profile_method

api.profile_method = profile_method
api.profile_class = profile_class
