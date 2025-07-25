import os
import tempfile
from odoo import models,fields

class AccountMove(models.Model):
    _inherit = "account.move"

    def action_print_direct(self):
        """Print the multiple invoice copies report directly to the default printer on Linux."""

        # Ensure the appropriate report is available
        report = self.env.ref('base_accounting_kit.report_multiple_invoice', False)
        if not report:
            raise ValueError("Report not found: base_accounting_kit.report_multiple_invoice")

        # Generate the report content
        report = self.env['ir.actions.report']
        context = dict(self.env.context)
        docids = self.ids
        reportname = 'base_accounting_kit.report_multiple_invoice'
        converter = 'pdf'
        report

        # if self.ids:
        #     docids = [int(i) for i in self.ids.split(',') if i.isdigit()]
        if converter == 'html':
            report = report.with_context(context)._render_qweb_html(reportname, docids, data=context)[0]
        elif converter == 'pdf':
            report = report.with_context(context)._render_qweb_pdf(reportname, docids, data=context)[0]
        elif converter == 'text':
            report = report.with_context(context)._render_qweb_text(reportname, docids, data=context)[0]

        # Save the report content to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            pdf_path = tmp_file.name
            with open(pdf_path, 'wb') as f:
                f.write(report)

        # Print the file using lp command on Linux
        print("==============>" + pdf_path)
        os.system(f"lp {pdf_path}")


    



