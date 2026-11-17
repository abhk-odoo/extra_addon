import base64

from odoo import api, fields, models


class PrinterPrinter(models.Model):
    _inherit = 'printer.printer'

    type = fields.Selection(selection_add=[('fake_pdf', 'Fake PDF')], ondelete={'fake_pdf': 'set default'})


class IrActionsReport(models.Model):
    _inherit = 'ir.actions.report'

    @api.model
    def get_print_jobs(self, report_name, docids, data):
        # Same as the IoT / Obox PDF printers: render the report and send it as is
        jobs = super().get_print_jobs(report_name, docids, data)
        report = self._get_report(report_name)
        if report.report_type == 'qweb-pdf' and report.printer_ids.filtered(lambda p: p.type == 'fake_pdf'):
            pdf = self._render(report_name, docids, data)[0]
            if pdf:
                jobs.append({'type': 'fake_pdf', 'report': base64.b64encode(pdf).decode()})
        return jobs
