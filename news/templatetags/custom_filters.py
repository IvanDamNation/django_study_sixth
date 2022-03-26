from django import template

register = template.Library()


@register.filter(name='censor')
def censor(value):
    value1 = (str(value)).split()
    with open('censor_list.txt') as f:
        censor_list = f.read().split(",\n")

    for i, word in enumerate(censor_list):
        for j, word1 in enumerate(value1):
            if word1 == word:
                value1[j] = "*****"

    value = ' '.join(value1)
    return str(value)


@register.filter(name='update_page')
def update_page(full_path: str, page: int):
    try:
        params_list = full_path.split('?')[1].split('&')
        params = dict([tuple(str(param).split('=')) for param in params_list])
        params.update({'page': page})
        link = ''
        for key, value in params.items():
            link += f'{key}={value}&'

        return link[:-1]

    except:
        return f'page={page}'


@register.filter(name='is_author')
def is_author(user):
    return user.groups.filter(name='authors').exists()
