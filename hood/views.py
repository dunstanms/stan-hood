from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Neighborhood,Profile,Join,Post,Business
from .forms import EditProfileForm,NewPostForm,NewBussForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User



# Create your views here.


def home(request):

    if request.user.is_authenticated:
        if Join.objects.filter(user=request.user).exists():
            hoods = Neighborhood.objects.get(pk=request.user.join.hood.id)
            posts = Post.objects.filter(hood=request.user.join.hood.id)
            businesses = Business.objects.filter(hood=request.user.join.hood.id)

            return render(request, 'hoods.html', {"hoods": hoods, "businesses": businesses, "posts": posts})
        else:
            hoods = Neighborhood.objects.all()
            return render(request, 'home.html', {"hoods": hoods})
    else:
        hoods = Neighborhood.objects.all()
        return render(request, 'home.html', {"hoods": hoods})

   return render(request, 'profile.html', {"profile": profile, "hoods": hoods, "businesses": businesses,"posts":posts})

@login_required(login_url='/accounts/login/')
def profile(request, user):
    current_user = request.user
    user = User.objects.get(pk=user)
    posts = Post.objects.filter(user=user)
    profile = Profile.objects.filter(user = user)
    business = Business.objects.filter(user = user)

    return render (request, 'profile.html', {'posts':posts,'current_user': current_user,'profile':profile,"business":business})

@login_required(login_url='/accounts/login/')
def edit_profile(request):
    current_user = request.user
    if request.method == 'POST':
        if Profile.objects.filter(user=current_user).exists():
            form = EditProfileForm(request.POST, request.FILES,instance=Profile.objects.get(user=current_user))
        else:
            form = EditProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = current_user
            profile.save()
        return redirect('home')

    else:
        if Profile.objects.filter(user=current_user).exists():
            form = EditProfileForm(instance = Profile.objects.get(user=current_user))
        else:
            form = EditProfileForm()
    return render(request, 'edit_profile.html', {"form": form})


def hoods(request):

    hood = Neighborhood.objects.filter(user=request.user)

    return render(request, 'hood.html', {"hood": hood})


@login_required(login_url='/accounts/login/')
def join(request, hood):

    hood = Neighborhood.objects.get(pk=hood)
    if Join.objects.filter(user=request.user).exists():
        Join.objects.filter(user=request.user).update(hood=hood)
    else:

        Join(user=request.user, hood=hood).save()
    return redirect('home')


@login_required(login_url='/accounts/login/')
def exitHood(request, hood):

    if Join.objects.filter(user=request.user).exists():
        Join.objects.get(user=request.user).delete()
        return redirect('home')


def search_results(request):

    if 'name' in request.GET and request.GET["name"]:
        search_term = request.GET.get("name")
        searched_names = Business.search_by_name(search_term)
        message = f"{search_term}"

        return render(request, 'search.html',{"message":message,"businesses": searched_names})

    else:
        message = "You haven't searched for any term"
        return render(request, 'search.html',{"message":message})


@login_required(login_url='/accounts/login/')
def new_post(request):
    current_user = request.user
    if request.method == 'POST':
        form = NewPostForm(request.POST, request.FILES)
        if form.is_valid():
            print('jkknl')
            post = form.save(commit=False)
            post.user = current_user
            post.save()
        return redirect('home')

    else:
        form = NewPostForm()
    return render(request, 'newpost.html', {"form": form})

@login_required(login_url='/accounts/login/')
def new_buss(request):
    current_user = request.user
    if request.method == 'POST':
        form = NewBussForm(request.POST, request.FILES)
        if form.is_valid():
            Buss = form.save(commit=False)
            Buss.user = current_user
            Buss.hood = request.user.join.hood
            Buss.save()
        return redirect('home')

    else:
        form = NewBussForm()
    return render(request, 'newbuss.html', {"form": form})


def occupants(request, id):
    occupants = Join.objects.filter(id=hood).count()

    return redirect('home')


    #editprofile,add business,etc