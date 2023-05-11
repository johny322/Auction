def get_load_text(old_text: str, symbol=".") -> str:
    dots = ['....', '...', '..', '.']
    dots_count = old_text.count(symbol)
    if '⏳' in old_text:
        return old_text.replace('⏳', '⌛')
    if '⌛' in old_text:
        return old_text.replace('⌛', '⏳')

    if dots_count == 0:
        old_text = old_text + symbol
        return old_text
    if dots_count >= 4:
        old_dots = symbol * dots_count
        new_dots = symbol
        old_text = old_text.replace(old_dots, new_dots)
        return old_text
    else:
        old_dots = symbol * dots_count
        new_dots = symbol * (dots_count + 1)
        old_text = old_text.replace(old_dots, new_dots)
        return old_text


def escape(s, quote=True):
    """
    Replace special characters "&", "<" and ">" to HTML-safe sequences.
    If the optional flag quote is true (the default), the quotation mark
    characters, both double quote (") and single quote (') characters are also
    translated.
    """
    s = s.replace("&", "&amp;")  # Must be done first!
    s = s.replace("<", "&lt;")
    s = s.replace(">", "&gt;")
    if quote:
        s = s.replace('"', "&quot;")
        s = s.replace('\'', "&#x27;")
    return s


if __name__ == '__main__':
    print(get_load_text('Ищу номер'))
