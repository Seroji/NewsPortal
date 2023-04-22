from django import template
from .banned import forbidden_words

register = template.Library()


def type_check(value):
    if isinstance(value, str):
        return value
    else:
        raise ValueError


def replace_with_stars(value:str):
    _list = list(value)
    for i in range(len(value)):
        if _list[-1] != '*':
            _list[i+1] = '*'
        else:
            break
    return "".join(_list)


def checking_letter(value:str, orig:list, num:int):
    if orig[num][0].isupper():
        changed = list(value)
        changed[0] = changed[0].upper()
        changed = "".join(changed)
        return changed
    else:
        return value


@register.filter()
def censor(value):
    try:
        original_str = value.split(' ')
        lower_str = value.lower().split(' ')
        result = []
        i = -1
        for word in lower_str:
            i += 1
            if word in forbidden_words:
                word = replace_with_stars(word)
            word = checking_letter(word, original_str, i)
            result.append(word)
        return " ".join(result)
    except ValueError:
        print("Переданная переменная не является строковой!")
        return value
