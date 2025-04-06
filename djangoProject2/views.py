

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import CustomUserCreationForm
from .models import CustomUser
from django.contrib.auth.decorators import login_required

def signup(request):
    if request.user.is_authenticated:  # Verifica se o usuário já está autenticado
        return redirect('profile')  # Redireciona para a página de perfil

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()

    context = {
        'form': form,
        'errors': form.errors.values()
    }
    return render(request, 'registration/signup.html', context)

def login_view(request):
    if request.user.is_authenticated:
        return redirect('profile')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
        messages.error(request, "Usuário ou senha incorretos.")
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def home(request):
    return render(request, 'home.html')


def list_users(request):
    # Recupera todos os usuários do banco de dados
    users = CustomUser.objects.all()
    return render(request, 'list_users.html', {'users': users})

@login_required
def profile_view(request):
    user = request.user
    context = {
        'user': user
    }
    return render(request, 'profile.html', context)

def delete_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    user.delete()
    return redirect('list_users')
from django.shortcuts import render, redirect
from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    return redirect('login')

from django.shortcuts import render

def login_redirect_view(request):
    if request.user.is_authenticated:
        return redirect('profile')  # Redireciona para a página de perfil se o usuário estiver autenticado
    else:
        return redirect('login')  # Redireciona para a página de login se o usuário não estiver autenticado


import pandas as pd
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .rpa_cadunico import baixar_e_salvar_csv

@login_required
def profile_view(request):
    tabela_html = None

    if request.method == "POST":
        baixar_e_salvar_csv()
        df = pd.read_csv("cadunico_2023.csv", sep=",", encoding="latin1", skiprows=1)

        # Renomear colunas para exibir no site
        df = df.rename(columns={
            "ibge": "Código IBGE",
            "anomes": "Ano/Mês",
            "cadunico_tot_fam": "Famílias Cadastradas",
            "cadunico_tot_pes": "Pessoas Cadastradas",
            "cadunico_tot_fam_rpc_ate_meio_sm": "Famílias até 0.5 SM",
            "cadunico_tot_pes_rpc_ate_meio_sm": "Pessoas até 0.5 SM",
            "cadunico_tot_fam_pob": "Famílias em Pobreza",
            "cadunico_tot_pes_pob": "Pessoas em Pobreza",
            "cadunico_tot_fam_ext_pob": "Famílias em Extrema Pobreza",
            "cadunico_tot_pes_ext_pob": "Pessoas em Extrema Pobreza",
            "cadunico_tot_fam_pob_e_ext_pob": "Famílias Pobreza + Extrema",
            "cadunico_tot_pes_pob_e_ext_pob": "Pessoas Pobreza + Extrema"
        })

        tabela_html = df.head(50).to_html(classes="display styled-table", index=False, border=0)

    return render(request, "profile.html", {"tabela_html": tabela_html})
