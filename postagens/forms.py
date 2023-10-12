from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.mail import EmailMessage

from postagens.models import Comentario


class EmailForm(forms.Form):
    nome = forms.CharField(max_length=100)
    email = forms.EmailField(max_length=150)
    destino = forms.EmailField(max_length=150)
    comentario = forms.CharField(required=False, widget=forms.Textarea)

    def send_mail(self, post):
        conteudo = (f'Recomendo ler esta postagem. Você vai gostar!'
                    f'\nTitulo: {post.titulo}\n'
                    f'{self.cleaned_data["comentario"]}')
        mail = EmailMessage(
            subject=f'Recomendação de Post',
            from_email=self.cleaned_data["email"],
            to=[self.cleaned_data["destino"],],
            body=conteudo,
            headers={'Reply-to': self.cleaned_data["email"]},
        )
        mail.send()


class ComentarioModelForm(forms.ModelForm):

    class Meta:
        model = Comentario
        fields = ['nome', 'email', 'corpo']

    def salvar_comentario(self, post):
        novo_coment = self.save(commit=False)
        novo_coment.postagem = post
        novo_coment.nome = self.cleaned_data['nome']
        novo_coment.email = self.cleaned_data['email']
        novo_coment.corpo = self.cleaned_data['corpo']
        return novo_coment.save()


class CadUsuarioForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email', 'first_name', 'last_name', 'password1', 'password2']