from django.shortcuts import render, redirect
from django.views import *
from django.views.generic.edit import *
from .models import *
from .forms import *
from django.contrib.auth.mixins import *
from django.contrib.auth.models import *
from django.contrib.auth import (authenticate, login, logout)


class Login(FormView):
    template_name = 'login.html'
    form_class = Login

    def get_success_url(self):
        # find your next url here
        next_url = self.request.GET.get('next')  # here method should be GET or POST.
        if next_url:
            success_url = next_url
            return success_url  # you can include some query strings as well
        else:
            # success_url = '/accounts/login/'
            success_url = '/login/'
            return success_url  # what url you wish to return'

    def form_valid(self, form):
        user_login = form.cleaned_data["login"]
        password = form.cleaned_data["password"]
        user = authenticate(username=user_login, password=password)
        if user is not None:
            login(self.request, user)
        return super(Login, self).form_valid(form)




class Logout(FormView):

    def get(self, request):
        logout(request)
        return redirect('/login')


class MainPage(View):

    def get(self, request):
        photos = Photo.objects.all()
        context = {
            "title": "Main Page",
            "content": "Main Page!",
            "photos": photos,
        }
        return render(request, "main_page.html", context)


# class AddUser(LoginRequiredMixin, CreateView):
class AddUser(CreateView):
    model = User
    template_name = "user_form.html"
    fields = ['username', 'password', 'email', 'first_name', 'last_name']
    success_url = '/add_user'


class AddPhoto(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'next'

    def get(self, request):
        form = AddPhotoForm()
        context = {"form": form}
        return render(request, "add_photo.html", context)

    def post(self, request):
        form = AddPhotoForm(request.POST, request.FILES)
        if form.is_valid():
            server_path = form.cleaned_data['server_path']
            disk_file = form.cleaned_data['disk_file']
            if not ((server_path and not disk_file) or (not server_path and disk_file)):
                # raise forms.ValidationError('Please fill one of the fields.')
                context = {
                    'message': 'Please fill only one of the fields.',
                    'form': form,
                }
            context = {
                'message': 'Photo added!',
                'form': form,
            }
            # create and save Photo Model!
            new_photo = Photo.objects.create(path=server_path,
                                             my_user=request.user)
            new_photo.save()
        else:
            context = {
                'message': 'Form not valid!',
                'form': form,
            }

        return render(request, "add_photo.html", context)
