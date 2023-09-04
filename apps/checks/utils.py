import json
import base64
import requests

from django.conf import settings
from django.template.loader import render_to_string
from django.core.files.base import ContentFile


def encode_html_to_base64(html_string):
    return base64.b64encode(bytes(html_string, "utf-8"))


def html_to_pdf(check):
    """
    Get pdf from html using wkhtmltopdf service
    """
    html_string = render_to_string("check.html", {"check": check})
    encoded_html = encode_html_to_base64(html_string)

    data = {
        "contents": encoded_html.decode("utf-8"),
    }
    headers = {
        "Content-Type": "application/json",
    }
    response = requests.post(settings.WKHTMLTOPDF_URL, data=json.dumps(data), headers=headers)
    return ContentFile(response.content)
