class NumberValidator(object):

    def __init__(self, min_length=6):
        self.min_length = min_length

    def validate(self, password, user=None):
        special_characters = "[~\!@#\$%\^&\*\(\)_\+{}\":;'\[\]]"
        if any(char.isdigit() for char in password):
            pass
        if any(char.isalpha() for char in password):
            pass
        if any(char in special_characters for char in password):
            pass

    def get_help_text(self):
        return "Your password must be atleast 6 characters"