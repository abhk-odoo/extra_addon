# Dev-only: a printer type that "prints" PDF jobs by downloading them.
{
    'name': 'Fake PDF Printer (dev only)',
    'summary': 'Test PDF print jobs of the printer framework without hardware',
    'depends': ['printer'],
    'assets': {
        'web.assets_backend': [
            'fake_pdf_printer/static/src/fake_pdf_printer_handler.js',
        ],
    },
    'license': 'LGPL-3',
}
