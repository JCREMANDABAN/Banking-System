from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import FormView, ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView as DjangoLoginView, LogoutView as DjangoLogoutView

from .forms import RegisterForm, LoginForm, AccountForm
from .models import Account

class RegisterView(FormView):
    template_name = 'accounts/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(self.request, 'Welcome! Your account has been created.')
        return super().form_valid(form)

class LoginView(DjangoLoginView):
    template_name = 'accounts/login.html'
    authentication_form = LoginForm

    def form_valid(self, form):
        messages.success(self.request, 'Logged in successfully.')
        return super().form_valid(form)

class LogoutView(DjangoLogoutView):
    next_page = reverse_lazy('home')

class UserListView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'accounts/user_list.html'
    context_object_name = 'users'
    paginate_by = 10
    ordering = ['-date_joined']

    def get_queryset(self):
        qs = super().get_queryset().select_related()
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(username__icontains=q)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = 'Users'
        ctx['query'] = self.request.GET.get('q', '')
        return ctx

class AccountListView(LoginRequiredMixin, ListView):
    model = Account
    template_name = 'accounts/account_list.html'
    context_object_name = 'accounts'
    paginate_by = 10
    ordering = ['-created_at']

    def get_queryset(self):
        qs = super().get_queryset().select_related('owner')
        status = self.request.GET.get('status')
        if status:
            qs = qs.filter(status=status)
        return qs.filter(owner=self.request.user)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = 'My Accounts'
        ctx['status_filter'] = self.request.GET.get('status', '')
        return ctx

class AccountCreateView(LoginRequiredMixin, CreateView):
    model = Account
    form_class = AccountForm
    template_name = 'accounts/user_form.html'
    success_url = reverse_lazy('accounts:account_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        messages.success(self.request, 'Account created.')
        return super().form_valid(form)

class AccountUpdateView(LoginRequiredMixin, UpdateView):
    model = Account
    form_class = AccountForm
    template_name = 'accounts/user_form.html'
    success_url = reverse_lazy('accounts:account_list')

    def get_queryset(self):
        return Account.objects.filter(owner=self.request.user)

    def form_valid(self, form):
        messages.info(self.request, 'Account updated.')
        return super().form_valid(form)

class AccountDeleteView(LoginRequiredMixin, DeleteView):
    model = Account
    template_name = 'accounts/user_form.html'
    success_url = reverse_lazy('accounts:account_list')

    def get_queryset(self):
        return Account.objects.filter(owner=self.request.user)

    def delete(self, request, *args, **kwargs):
        messages.warning(self.request, 'Account deleted.')
        return super().delete(request, *args, **kwargs)
