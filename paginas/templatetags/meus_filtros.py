from django import template

register = template.Library()


@register.filter(name='categoria_cor')
def categoria_cor(categoria):
    """Retorna a cor hex para uma categoria.

    Usa `categoria.cor` se presente; senão tenta mapear por nome; caso não encontre,
    retorna um cinza padrão.
    """
    # tenta atributo cor
    try:
        if categoria is None:
            return '#6c757d'
        if hasattr(categoria, 'cor') and categoria.cor:
            return categoria.cor
    except Exception:
        pass

    # resolve nome da categoria
    try:
        nome = categoria.nome if hasattr(categoria, 'nome') else str(categoria)
    except Exception:
        nome = str(categoria)

    nome_lower = nome.lower()

    mapping = {
        'educação ambiental': '#2d7f5e',
        'educacao ambiental': '#2d7f5e',
        'amazônia': '#28a745',
        'amazonia': '#28a745',
        'cidadania': '#007bff',
        'cultura': '#6f42c1',
        'saúde': '#dc3545',
        'saude': '#dc3545',
        'economia': '#fd7e14',
        'tecnologia': '#17a2b8',
        'meio ambiente': '#20c997',
    }

    for key, color in mapping.items():
        if key in nome_lower:
            return color

    return '#6c757d'


@register.filter(name='in_group')
def in_group(user, group_name):
    """Retorna True se o usuário pertence ao grupo `group_name`.

    Uso no template: {% if request.user|in_group:"Admin" %}
    """
    try:
        if not user or user.is_anonymous:
            return False
        return user.groups.filter(name=group_name).exists()
    except Exception:
        return False
