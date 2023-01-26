from django import template

register = template.Library()

BAD_WORDS = ['идиот','жирный','дурак','тупой']

@register.filter()
def badwords(value):
    words = value.split()
    words_out = []
    for i in words:
        if i in BAD_WORDS:
            words_out.append(i[0] + '*' * (len(i) - 1))
        else:
            words_out.append(i)
    return ' '.join(words_out)
