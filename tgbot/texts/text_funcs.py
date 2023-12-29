from typing import List


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


def logger_text_formatter(texts: List[str], join_str: str = None) -> str:
    if join_str is None:
        join_str = "\n" + " " * 37
    return join_str.join(texts)


if __name__ == '__main__':
    print(get_load_text('Ищу номер'))
