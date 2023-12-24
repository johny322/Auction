from typing import Iterable


def escape(s, quote=True):
    """
    Replace special characters "&", "<" and ">" to HTML-safe sequences.
    If the optional flag quote is true (the default), the quotation mark
    characters, both double quote (") and single quote (') characters are also
    translated.
    """
    if not s:
        return s
    s = s.replace("&", "&amp;")  # Must be done first!
    s = s.replace("<", "&lt;")
    s = s.replace(">", "&gt;")
    if quote:
        s = s.replace('"', "&quot;")
        s = s.replace('\'', "&#x27;")
    return s


def get_word_form(forms: Iterable[str], count: int) -> str:
    """

    3 формы:
    1) компьютер
    2) компьютера
    3) компьютеров
    если последние 2 цифры числа от 11 до 19 - то используется 3 форма

    если последняя цифра 1 - 1 форма

    если последняя цифра от 2 до 4 - 2 форма

    во всех остальных случаях - 3 форма

    """
    form1, form2, form3 = forms
    if 11 <= count % 100 <= 19:
        current_form = form3
    elif count % 10 == 1:
        current_form = form1
    elif 2 <= count % 10 <= 4:
        current_form = form2
    else:
        current_form = form3
    return current_form
