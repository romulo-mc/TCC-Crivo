import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

class SenhaForteValidator:
    def validate(self, password, user=None):
        if len(password) < 8:
            raise ValidationError(_("A senha deve ter pelo menos 8 caracteres."), code='password_too_short')
        if not re.search(r'[A-Z]', password):
            raise ValidationError(_("A senha deve conter pelo menos uma letra maiúscula."), code='password_no_upper')
        if not re.search(r'[a-z]', password):
            raise ValidationError(_("A senha deve conter pelo menos uma letra minúscula."), code='password_no_lower')
        if not re.search(r'[0-9]', password):
            raise ValidationError(_("A senha deve conter pelo menos um número."), code='password_no_number')

    def get_help_text(self):
        return _("Sua senha deve ter no mínimo 8 caracteres, incluindo uma letra maiúscula, uma minúscula e um número.")

    def __call__(self, value):
        return self.validate(value)