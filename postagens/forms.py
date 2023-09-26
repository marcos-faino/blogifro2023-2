from django import forms
from django.core.mail import EmailMessage


class EmailForm(forms.Form):
    nome = forms.CharField(max_length=100)
    email = forms.EmailField(max_length=150)
    destino = forms.EmailField(max_length=150)
    comentario = forms.CharField(required=False, widget=forms.Textarea)

    def send_mail(self, post):
        conteudo = (f'Recomendo ler esta postagem. Você vai gostar!'
                    f'\nTitulo: {post.titulo}\n'
                    f'{self.comentario}')
        mail = EmailMessage(
            subject=f'Recomendação de Post',
            from_email=self.email,
            to=[self.destino],
            body=conteudo,
            headers={'Reply-to': self.email},
        )
        mail.send()