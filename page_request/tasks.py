import io

import time

from weasyprint import HTML
from django.core.files import File
from .models import PageRequest




def pdf(page):
    # post_save is triggered after the model is saved
    time.sleep(1)
    if page.status != page.Status.PENDING:
        return
    page.status = page.Status.GENERATING
    page.save()
    try:
        html = HTML(url=page.url)
    except Exception as e:
        return _extracted_from_pdf_11(page, e)
    try:
        pdf_in_memory = io.BytesIO()
        html.write_pdf(target=pdf_in_memory)
    except Exception as e:
        return _extracted_from_pdf_11(page, e)
    page.pdf_file = File(pdf_in_memory, f"{page.pk}.pdf")
    page.status = PageRequest.Status.READY
    page.save()


# TODO Rename this here and in `pdf`
def _extracted_from_pdf_11(page, e):
    page.status = PageRequest.Status.ERROR
    page.error_msg = str(e)
    page.save()
    return
