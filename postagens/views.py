from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, FormView

from postagens.forms import EmailForm
from postagens.models import Postagem


class HomeView(TemplateView):
    template_name = 'index.html'


"""
class PostsListView(TemplateView):
    template_name = 'postagens/listar.html'

    def get_context_data(self, **kwargs):
        cont = super().get_context_data(**kwargs)
        cont['posts'] = Postagem.publicados.all()
        return cont
"""


class PostsListView(ListView):
    template_name = 'postagens/listar.html'
    queryset = Postagem.objects.all()
    context_object_name = 'posts'
    paginate_by = 2


class DetalhePostView(DetailView):
    template_name = 'postagens/detalhe.html'
    model = Postagem
    context_object_name = 'post'


class EnviarPostFormView(FormView):
    template_name = "postagens/enviar.html"
    form_class = EmailForm
    success_url = reverse_lazy('listarposts')

    def _get_postagem(self, idpost):
        try:
            return Postagem.publicados.get(id=idpost)
        except Postagem.DoesNotExist:
            messages.error(self.request, 'A postagem não existe!')
            reverse_lazy('listarposts')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['post'] = self._get_postagem(self.kwargs['pk'])
        return ctx

    def form_valid(self, form):
        form.cleaned_data
        post = self.get_context_data()['post']
        form.send_mail(post)
        messages.success(self.request, f'Postagem {post.titulo} '
                                       f'enviado com sucesso!!!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Não foi possível enviar a Postagem')
        return super().form_invalid(form)