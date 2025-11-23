from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Noticia
from .models import Comentario
from django.forms import Textarea

# Formulário para cadastro de usuários
class UsuarioCadastroForm(UserCreationForm):
 email = forms.EmailField(required=True, help_text="Informe um email válido.")

 class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


# Formulário para cadastro/edição de notícias
class NoticiaForm(forms.ModelForm):
    class Meta:
        model = Noticia
        fields = '__all__'

    def clean_imagem(self):
        imagem = self.cleaned_data.get('imagem')

        # Se o usuário não enviou imagem nova, apenas retorna
        if not imagem:
            return imagem

        # ⚠️ Corrige o erro "'ImageFieldFile' object has no attribute 'content_type'"
        # Só verifica content_type se o objeto for um arquivo enviado (não o já existente)
        if hasattr(imagem, 'content_type'):
            content_type = imagem.content_type
            valid_mime = ['image/jpeg', 'image/png']

            if content_type not in valid_mime:
                raise forms.ValidationError('Formatos permitidos: JPEG e PNG.')

            max_size = 2 * 1024 * 1024  # 2 MB
            if imagem.size > max_size:
                raise forms.ValidationError('A imagem deve ter no máximo 2 MB.')

        # Se for um ImageFieldFile (imagem já existente), apenas retorna
        return imagem


# Formulário simples para criar um comentário (usado em notícias)
class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['texto']
        widgets = {
            'texto': Textarea(attrs={'rows': 3, 'class': 'form-control', 'placeholder': 'Escreva seu comentário...'}),
        }
        labels = {
            'texto': 'Comentário',
        }
