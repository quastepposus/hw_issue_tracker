from django.core.exceptions import ValidationError


def summary_validator(string):
    if len(string) < 10:
        raise ValidationError('too short')
    elif len(string) > 100:
        raise ValidationError('too long')

def description_validator(text):
    if len(text) < 50:
        raise ValidationError('too short')
    elif len(text) > 5000:
        raise ValidationError('too long')

def project_title_validator(text):
    if len(text) < 3:
        raise ValidationError('too short')
    elif len(text) > 50:
        raise ValidationError('too long')

def project_description_validator(text):
    if len(text) > 5000:
        raise ValidationError('too long')
