from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

from .models import Profile, Tweet, Comment
from .forms import ProfileUpdateForm, TweetForm, SignUpForm, ProfilePicForm, UpdateUserForm, CommentForm




# ---------------------------------------------------------
# HOME - FEED
# ---------------------------------------------------------
def home(request):

    # Usuário autenticado → feed dos perfis que segue + ele mesmo
    if request.user.is_authenticated:
        form = TweetForm(request.POST or None)

        # postagem
        if request.method == "POST":
            if form.is_valid():
                tweet = form.save(commit=False)
                tweet.user = request.user
                tweet.save()
                messages.success(request, "Seu tweet foi publicado!")
                return redirect('home')

        # pega os perfis que o user segue
        following_profiles = request.user.profile.follows.all()

        # feed = tweets dessas pessoas + meus próprios tweets
        tweets = Tweet.objects.filter(
            user__profile__in=following_profiles
        ).union(
            Tweet.objects.filter(user=request.user)
        ).order_by('-created_at')

        # sugestões de usuários (não seguiram ainda)
        suggestions = Profile.objects.exclude(
            user=request.user
        ).exclude(
            id__in=following_profiles
        )[:5]

        return render(request, 'home.html', {
            "tweets": tweets,
            "form": form,
            "suggestions": suggestions,
        })

    # visitante → todos tweets (público)
    tweets = Tweet.objects.all().order_by("-created_at")
    return render(request, 'home.html', {"tweets": tweets})


# ---------------------------------------------------------
# LISTA DE PERFIS
# ---------------------------------------------------------
def profile_list(request):
    if request.user.is_authenticated:
        profiles = Profile.objects.exclude(user=request.user)
        return render(request, 'profile_list.html', {"profiles": profiles})
    else:
        messages.error(request, "Você precisa estar conectado para visualizar esta página.")
        return redirect('home')


# ---------------------------------------------------------
# PERFIL
# ---------------------------------------------------------
def profile(request, pk):
    if not request.user.is_authenticated:
        messages.error(request, "Você precisa estar conectado para visualizar esta página.")
        return redirect('home')

    profile = get_object_or_404(Profile, user_id=pk)
    tweets = Tweet.objects.filter(user_id=pk).order_by("-created_at")

    # follow/unfollow via POST
    if request.method == "POST":
        current = request.user.profile
        action = request.POST.get("follow")

        if action == "follow":
            current.follows.add(profile)
        elif action == "unfollow":
            current.follows.remove(profile)

        current.save()

    return render(request, "profile.html", {"profile": profile, "tweets": tweets})


# ---------------------------------------------------------
# FOLLOW / UNFOLLOW (botões externos)
# ---------------------------------------------------------
def follow(request, pk):
    if request.user.is_authenticated:
        target = Profile.objects.get(user_id=pk)
        request.user.profile.follows.add(target)
        request.user.profile.save()
        messages.success(request, f"Você começou a seguir {target.user.username}.")
        return redirect(request.META.get("HTTP_REFERER"))
    messages.error(request, "Por favor faça login primeiro.")
    return redirect('home')


def unfollow(request, pk):
    if request.user.is_authenticated:
        target = Profile.objects.get(user_id=pk)
        request.user.profile.follows.remove(target)
        request.user.profile.save()
        messages.success(request, f"Você deicou de seguir {target.user.username}.")
        return redirect(request.META.get("HTTP_REFERER"))
    messages.error(request, "Por favor faça login primeiro.")
    return redirect('home')


# ---------------------------------------------------------
# FOLLOWERS / FOLLOWS (páginas internas)
# ---------------------------------------------------------
def followers(request, pk):
    if request.user.is_authenticated:
        if request.user.id != pk:
            messages.error(request, "Este não é o seu perfil.")
            return redirect('home')
        profile = Profile.objects.get(user_id=pk)
        return render(request, 'followers.html', {"profiles": profile})
    messages.error(request, "Por favor faça login primeiro.")
    return redirect('home')


def follows(request, pk):
    if request.user.is_authenticated:
        if request.user.id != pk:
            messages.error(request, "Este não é o seu perfil.")
            return redirect('home')
        profile = Profile.objects.get(user_id=pk)
        return render(request, 'follows.html', {"profiles": profile})
    messages.error(request, "Por favor faça login primeiro.")
    return redirect('home')


# ---------------------------------------------------------
# LOGIN / LOGOUT
# ---------------------------------------------------------
def login_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            messages.success(request, "Você foi logado.")
            return redirect('home')

        messages.error(request, "Login invalido! tente novamente.")
        return redirect('login')

    return render(request, "login.html")


def logout_user(request):
    logout(request)
    messages.success(request, "Você foi deslogado.")
    return redirect('home')


# ---------------------------------------------------------
# REGISTER
# ---------------------------------------------------------
def register_user(request):
    form = SignUpForm()

    if request.method == "POST":
        form = SignUpForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Bem vindo! você foi cadastrado.")
            return redirect("home")

    return render(request, "register.html", {'form': form})


# ---------------------------------------------------------
# UPDATE PROFILE
# ---------------------------------------------------------
def update_user(request):
    if not request.user.is_authenticated:
        messages.error(request, "Porfavor faça seu login.")
        return redirect('home')

    current_user = request.user
    profile = current_user.profile

    user_form = UpdateUserForm(request.POST or None, instance=current_user)
    profile_form = ProfileUpdateForm(request.POST or None, request.FILES or None, instance=profile)

    if user_form.is_valid() and profile_form.is_valid():
        user_form.save()
        profile_form.save()
        messages.success(request, "Seu perfil foi atualizado com sucesso!")
        return redirect('profile', current_user.id)

    return render(request, "update_user.html", {
        'user_form': user_form,
        'profile_form': profile_form
    })

# ---------------------------------------------------------
# update senha
# ---------------------------------------------------------
def change_password(request):
    if not request.user.is_authenticated:
        messages.error(request, "Você precisa estar logado.")
        return redirect('login')

    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # mantém logado
            messages.success(request, "Senha alterada com sucesso!")
            return redirect('update_user')
        else:
            messages.error(request, "Erro ao alterar a senha.")
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'change_password.html', {
        'form': form
    })

# ---------------------------------------------------------
# LIKE
# ---------------------------------------------------------
def tweet_like(request, pk):
    if request.user.is_authenticated:
        tweet = get_object_or_404(Tweet, id=pk)
        if request.user in tweet.likes.all():
            tweet.likes.remove(request.user)
        else:
            tweet.likes.add(request.user)
        return redirect(request.META.get("HTTP_REFERER"))

    messages.error(request, "Porfavor faça seu login.")
    return redirect('home')


# ---------------------------------------------------------
# DELETE TWEET
# ---------------------------------------------------------
def delete_tweet(request, pk):
    if not request.user.is_authenticated:
        messages.error(request, "Porfavor faça seu login.")
        return redirect('home')

    tweet = get_object_or_404(Tweet, id=pk)

    if tweet.user != request.user:
        messages.error(request, "Você não pode apagar este tweet..")
        return redirect('home')

    tweet.delete()
    messages.success(request, "Tweet apagado.")
    return redirect(request.META.get("HTTP_REFERER"))


# ---------------------------------------------------------
# EDIT TWEET
# ---------------------------------------------------------
def edit_tweet(request, pk):

    if not request.user.is_authenticated:
        messages.error(request, "Porfavor faça seu login.")
        return redirect('home')

    tweet = get_object_or_404(Tweet, id=pk)

    if tweet.user != request.user:
        messages.error(request, "você não pode editar este tweet.")
        return redirect('home')

    form = TweetForm(request.POST or None, instance=tweet)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Seu tweet foi atualizado!")
            return redirect('home')

    return render(request, "edit_tweet.html", {"form": form, "tweet": tweet})

#---------------------------------------------------------
#COMMENTS
#---------------------------------------------------------
def add_comment(request, pk):
    if not request.user.is_authenticated:
        messages.error(request, "Please log in.")
        return redirect('home')

    tweet = get_object_or_404(Tweet, id=pk)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.tweet = tweet
            comment.save()
            return redirect(request.META.get('HTTP_REFERER'))

    return redirect('home')
