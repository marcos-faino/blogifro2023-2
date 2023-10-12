from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LogoutView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, FormView, CreateView

from postagens.forms import EmailForm, ComentarioModelForm, CadUsuarioForm
from postagens.models import Postagem, Comentario


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

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['coments'] = Comentario.objects.all().filter(postagem=self.object, ativo=True)
        return ctx


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


class ComentarioCreateView(CreateView):
    template_name = "postagens/comentarios.html"
    form_class = ComentarioModelForm

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['post'] = Postagem.objects.get(id=self.kwargs['pk'])
        return ctx

    def form_valid(self, form):
        post = Postagem.objects.get(id=self.kwargs['pk'])
        form.salvar_comentario(post)
        return redirect('detalhepost', post.id, post.slug)


class CadUsuarioView(CreateView):
    template_name = 'usuarios/cadastro.html'
    form_class = CadUsuarioForm
    success_url = reverse_lazy('loginuser')

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Usuário Cadastrado!!!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Não foi possível cadastrar!')
        redirect('cadusuario')


class LoginUserView(FormView):
    template_name = 'usuarios/login.html'
    model = User
    form_class = AuthenticationForm
    success_url = reverse_lazy('listarposts')

    def form_valid(self, form):
        username = form.cleaned_data['username']
        senha = form.cleaned_data['password']
        usuario = authenticate(self.request, username=username, password=senha)
        if usuario is not None:
            login(self.request, usuario)
            return redirect('listarposts')
        messages.error(self.request, 'Usuário não existe')
        return redirect('loginuser')

    def form_invalid(self, form):
        messages.error(self.request, 'Não foi possível logar.')
        return redirect('loginuser')


class LogoutUserView(LoginRequiredMixin, LogoutView):

    def get(self, request):
        logout(request)
        return redirect('listarposts')
