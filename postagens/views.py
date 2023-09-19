from django.views.generic import TemplateView, ListView, DetailView

from postagens.models import Postagem


class HomeView(TemplateView):
    template_name = 'index.html'


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
"""

class DetalhePostView(DetailView):
    template_name = 'postagens/detalhe.html'
    model = Postagem
    context_object_name = 'post'
