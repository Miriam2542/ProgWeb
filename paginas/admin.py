from django.contrib import admin
from django.utils.html import format_html
from .models import Categoria, Noticia, Comentario, Midia


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
	list_display = ('nome', 'descricao')
	search_fields = ('nome',)


@admin.register(Noticia)
class NoticiaAdmin(admin.ModelAdmin):
	list_display = ('titulo', 'categoria', 'postado_por', 'data_publicacao', 'publicado')
	list_filter = ('categoria','publicado')
	search_fields = ('titulo', 'conteudo')


@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
	list_display = ('autor', 'noticia', 'data')
	search_fields = ('texto',)


@admin.register(Midia)
class MidiaAdmin(admin.ModelAdmin):
	list_display = ('imagem_preview', 'titulo', 'descricao', 'fonte', 'arquivo_pdf_link')
	readonly_fields = ('imagem_preview',)
	fields = ('titulo', 'url', 'imagem', 'arquivo_pdf', 'descricao', 'fonte')
	search_fields = ('titulo', 'descricao', 'fonte')
	list_filter = ('fonte',)

	def imagem_preview(self, obj):
		if obj and obj.imagem:
			return format_html('<img src="{}" style="max-height:100px;"/>', obj.imagem.url)
		return "-"
	imagem_preview.short_description = 'Imagem'

	def arquivo_pdf_link(self, obj):
		if obj and obj.arquivo_pdf:
			return format_html('<a href="{}" target="_blank">Download PDF</a>', obj.arquivo_pdf.url)
		return '-'
	arquivo_pdf_link.short_description = 'PDF'
