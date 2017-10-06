from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from django.db.models import Q
from django.contrib import messages
from acetutors.forms import DetailForm, InfoForm, UserForm, UserProfileInfoForm
from acetutors.models import User, Information1, Song, UserProfileInfo, Feedback

AUDIO_FILE_TYPES = ['wav', 'mp3', 'ogg']
IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg', 'gif']


def tutee(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        userprofileinfo = UserProfileInfo.objects.all()

        print(userprofileinfo)

        if user is not None:
            if user.is_active:
                print(type)
                login(request, user)
                u = User.objects.get(username=username)
                request.session['user_id'] = u.id
                request.session['user_username'] = u.username
                albums = Information1.objects.filter(user=request.user)
                t = UserProfileInfo.objects.get(id=u.id)
                if t.type == "tutee":
                    return render(request, 'webs/index.html', {'albums': albums})
                elif t.type == "tutor":
                    return render(request, 'webs/tutor_profile.html')
                # else:
                #     return render(request, 'music/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'webs/login.html', {'error_message': 'Invalid login'})
    return render(request, 'webs/login.html')


def tutor(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        userprofileinfo = UserProfileInfo.objects.all()
        if user is not None:
            if user.is_active and user.userprofile.type == "Tutor":
                login(request, user)
                u = User.objects.get(username=username)
                request.session['user_id'] = u.id
                request.session['user_username'] = u.username
                albums = UserProfileInfo.objects.filter(user=request.user)
            return render(request, 'webs/tutor_profile.html', {'albums': albums})

                # else:
                #     return render(request, 'music/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'webs/login_tutor.html', {'error_message': 'Invalid login'})
    return render(request, 'webs/login_tutor.html')


def create_album(request):
    # userinfo = User.objects.get(id=request.session['user_id'])
    # userprofileinfo = UserProfileInfo.objects.get(user_id=request.session['user_id'])
    if not request.user.is_authenticated():
        return render(request, 'webs/login.html')
    else:
        form = DetailForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            info = form.save(commit=False)
            info.user = request.user
            info.picture_topic = request.FILES['picture_topic']
            file_type = info.picture_topic.url.split('.')[-1]
            file_type = file_type.lower()
            if file_type not in IMAGE_FILE_TYPES:
                context = {
                    'info': info,
                    'form': form,
                    'error_message': 'Image file must be PNG, JPG, or JPEG',
                }
                return render(request, 'webs/create_album.html', context)
            info.save()
            return render(request, 'webs/detail.html', {'info': info})

        context = {
            "form": form,
        }
        return render(request, 'webs/create_album.html', context)

# Song is for Description


def create_song(request, info_id):
    form = InfoForm(request.POST or None, request.FILES or None)
    info = get_object_or_404(Information1, pk=info_id)
    if form.is_valid():
        infos_songs = info.song_set.all()
        for s in infos_songs:
            if s.song_title == form.cleaned_data.get("song_title"):
                context = {
                    'info': info,
                    'form': form,
                    'error_message': 'You already added that song',
                }
                return render(request, 'webs/create_song.html', context)
        song = form.save(commit=False)
        song.info = info
        song.audio_file = request.FILES['audio_file']
        file_type = song.audio_file.url.split('.')[-1]
        file_type = file_type.lower()
        if file_type not in AUDIO_FILE_TYPES:
            context = {
                'info': info,
                'form': form,
                'error_message': 'Audio file must be WAV, MP3, or OGG',
            }
            return render(request, 'webs/create_song.html', context)

        song.save()
        return render(request, 'webs/detail.html', {'info': info})
    context = {
        'info': info,
        'form': form,
    }
    return render(request, 'webs/create_song.html', context)

# album is for Schedule


def delete_album(request, info_id):
    info = Information1.objects.get(pk=info_id)
    info.delete()
    albums = Information1.objects.filter(user=request.user)
    return render(request, 'webs/index.html', {'albums': albums})


def delete_song(request, info_id, song_id):
    info = get_object_or_404(Information1, pk=info_id)
    song = Song.objects.get(pk=song_id)
    song.delete()
    return render(request, 'webs/detail.html', {'info': info})


def detail(request, info_id):
    if not request.user.is_authenticated():
        return render(request, 'webs/login.html')
    else:
        user = request.user
        info = get_object_or_404(Information1, pk=info_id)
    return render(request, 'webs/detail.html', {'info': info, 'user': user})


def favorite(request, song_id):
    song = get_object_or_404(Song, pk=song_id)
    try:
        if song.is_favorite:
            song.is_favorite = False
        else:
            song.is_favorite = True
        song.save()
    except (KeyError, Song.DoesNotExist):
        return JsonResponse({'success': False})
    else:
        return JsonResponse({'success': True})


def favorite_album(request, info_id):
    info = get_object_or_404(Information1, pk=info_id)
    try:
        if info.is_favorite:
            info.is_favorite = False
        else:
            info.is_favorite = True
        info.save()
    except (KeyError, Information1.DoesNotExist):
        return JsonResponse({'success': False})
    else:
        return JsonResponse({'success': True})


def index(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        message = request.POST['message']

        feed = Feedback(name=name, email=email, message=message)
        feed.save()

    if not request.user.is_authenticated():
        return render(request, 'webs/new_homepage1.html')
    else:
        infos = Information1.objects.filter(user=request.user)
        song_results = Song.objects.all()
        query = request.GET.get("q")
        if query:
            infos = infos.filter(
                Q(email__icontains=query) |
                Q(full_name__icontains=query)
            ).distinct()
            song_results = song_results.filter(
                Q(song_title__icontains=query)
            ).distinct()
            return render(request, 'webs/index.html', {
                'infos': infos,
                'songs': song_results,
            })
        else:
            return render(request, 'webs/index.html', {'infos': infos})


def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'webs/new_homepage1.html', context)


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        type = request.POST['type']
        user = authenticate(username=username, password=password, type=type)
        if user is not None:
            if user.is_active and type == 'Tutee':
                login(request, user)
                albums = Information1.objects.filter(user=request.user)
                return render(request, 'webs/index.html', {'albums': albums})
            elif user.is_active and type == 'Tutor':
                login(request, user)
                albums = UserProfileInfo.objects.filter(user=request.user)
                return render(request, 'webs/tutor_profile.html', {'albums': albums})
        else:
            return render(request, 'webs/login.html', {'error_message': 'Invalid login'})
    return render(request, 'webs/login.html')


def register(request):
    form = UserForm(request.POST or None)
    form1 = UserProfileInfoForm(request.POST or None)
    if form.is_valid() and form1.is_valid():
        user = form.save(commit=False)
        firstname = form.cleaned_data['first_name']
        lastname = form.cleaned_data['last_name']
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        user = authenticate(firstname=firstname, lastname=lastname, username=username, password=password)
        userprofile = form1.save(commit=False)
        userprofile.user = user
        userprofile.save()
        if user is not None and profile is not None:
            if user.is_active:
                login(request, user)
                albums = Information1.objects.filter(user=request.user)
                return render(request, 'webs/login.html', {'albums': albums})
    context = {
        "form": form,
        "form1": form1
    }
    return render(request, 'webs/register.html', context)


# def register(request):
# 		registered = False
# 		if request.method == 'POST':
# 			uform = UserForm(data = request.POST)
# 			pform = UserProfileInfoForm(data = request.POST)
# 			if uform.is_valid() and pform.is_valid():
# 				user = uform.save()
# 				profile = pform.save(commit = False)
# 				profile.user = user
# 				profile.save()
# 				registered = True
#                 return HttpResponseRedirect('tutorial/login.html')
#         else:
# 				print(uform.errors, pform.errors)
#
# 		else:
# 			uform = UserForm()
# 			pform = UserProfileInfoForm()
#
#         return render(request, 'tutorial/register.html', {'uform': uform, 'pform': pform, 'registered': registered })


def songs(request, filter_by):
    if not request.user.is_authenticated():
        return render(request, 'webs/login.html')
    else:
        try:
            song_ids = []
            for info in Information1.objects.filter(user=request.user):
                for song in info.song_set.all():
                    song_ids.append(song.pk)
            users_songs = Song.objects.filter(pk__in=song_ids)
            if filter_by == 'favorites':
                users_songs = users_songs.filter(is_favorite=True)
        except Information1.DoesNotExist:
            users_songs = []
        return render(request, 'webs/songs.html', {
            'song_list': users_songs,
            'filter_by': filter_by,
        })


def profile(request):
    return render(request, 'webs/profile.html')


def index1(request):
    userinfo= User.objects.get(id=request.session['user_id'])
    types = UserProfileInfo.objects.get(user_id=request.session['user_id'])
    # return render(request, 'webs/index.html', {'type': types, 'user': userinfo})


def profiletutor(request):
    return render(request, 'webs/tutor_profile.html')

# def feedback(request):
#     if request.method == 'POST':
#         name = request.POST['name']
#         email = request.POST['email']
#         message = request.POST['message']
#
#         feed = Feedback(name=name, email=email, message=message)
#         feed.save()
#
#     return render(request, 'webs/new_homepage1.html')




















