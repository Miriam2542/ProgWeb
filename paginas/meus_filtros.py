from django import template
register = template.Library()

@register.filter
def categoria_cor(categoria):
	"""Retorna a cor (hex) associada a uma categoria.

	- Se o objeto Categoria tiver atributo `cor` preenchido, retorna ele.
	- Caso contrário, usa uma paleta padrão mapeada por nome (valores fornecidos pelo usuário).
	- Se não encontrar nada, retorna um verde padrão.
	"""
	if not categoria:
		return '#28a745'

	# Se houver campo cor no modelo e estiver preenchido, use-o
	cor = getattr(categoria, 'cor', None)
	if cor:
		return cor

	nome = getattr(categoria, 'nome', str(categoria)).strip()
	padrao = {
		'Biodiversidade e Fauna em Risco': '#4C9A2A',
		'Conservação e Recuperação de Biomas': '#2E7D32',
		'Degradação Ambiental': '#8D6E63',
		'Desmatamento': '#C62828',
		'Educação Ambiental': '#81C784',
		'Energias Renováveis e Transição Ecológica': '#F9A825',
		'Mudanças Climáticas e Aquecimento Global': '#29B6F6',
		'Políticas Públicas e Legislação Ambiental': '#1565C0',
	}
	return padrao.get(nome, '#28a745')
 
