from django.core.exceptions import ValidationError
from django.db import models


def validate_file_extension(value):
    import os
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.pdf', '.doc', '.docx', '.odt']
    if not ext in valid_extensions:
        raise ValidationError('File not supported! Your file should be .pdf, .doc, .docx, .odt format.')

def file_size(value): # add this to some file where you can import it from
    limit = 2 * 1024 * 1024
    if value.size > limit:
        raise ValidationError('File too large. Size should not exceed 2 MiB.')

# def make_custom_datefield(f):
#     formfield = f.formfield()
#     if isinstance(f, models.DateField):
#         formfield.widget.format = '%m/%d/%Y'
#         formfield.widget.attrs.update({'class':'datePicker', 'readonly':'true'})
#     return formfield
