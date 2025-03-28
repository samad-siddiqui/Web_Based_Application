from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from django.views.generic.edit import UpdateView
from .models import Profile, Project, Task
from django.urls import reverse_lazy
from .forms import (
    UserRegisterForm, LoginForm,
    ProjectForm, TaskForm, CommentForm,
    UserUpdateForm, UserProfileForm
)
from django.views.generic import (
    TemplateView, ListView, DetailView, CreateView
)
from django.contrib import messages
from django.contrib.auth import get_user_model


User = get_user_model()


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'home.html'

    def get(self, request):
        return render(request, self.template_name, {'title': 'Home'})


class ProfileView(LoginRequiredMixin, View):
    login_url = reverse_lazy('user-login')
    template_name = 'profile.html'

    def get(self, request):
        u_form = UserUpdateForm(instance=request.user)
        p_form = UserProfileForm(instance=request.user.profile)
        return render(
            request, self.template_name, {'u_form': u_form, 'p_form': p_form})

    def post(self, request):
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = UserProfileForm(
            request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, "Your profile has been updated!")
            return redirect('profile')

        return render(
            request, self.template_name, {'u_form': u_form, 'p_form': p_form})


class LoginView(View):
    """Class-based view for handling user login."""

    def get(self, request):
        """Handles GET requests and renders the login form."""
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        """Handles POST requests for user authentication."""
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(request, username=email, password=password)
            if user:
                login(request, user)
                return redirect('profile')
            else:
                return render(
                    request, 'login.html',
                    {"form": form, 'error': 'Invalid credentials'
                     }
                    )

        return render(request, 'login.html', {"form": form})


class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return redirect('login')


class RegisterView(View):
    def get(self, request):
        form = UserRegisterForm()
        return render(request, 'register.html', {'form': form})

    def post(self, request):
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        return render(request, 'register.html', {'form': form})


class UpdateProfileView(LoginRequiredMixin, UpdateView):
    model = Profile
    fields = ['user_bio', 'status', 'user_img']
    template_name = 'profile.html'
    success_url = reverse_lazy('profile')

    def get_object(self):
        return self.request.user.profile


# --- Projects ---
class ProjectListView(LoginRequiredMixin, ListView):
    model = Project
    template_name = 'project_list.html'
    context_object_name = 'projects'


class ProjectDetailView(LoginRequiredMixin, DetailView):
    model = Project
    template_name = 'project_detail.html'
    context_object_name = 'project'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = self.object.tasks.all()
        return context


class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'create_project.html'
    success_url = reverse_lazy('project_list')

    def form_valid(self, form):
        messages.success(self.request, "Project created successfully!")
        return super().form_valid(form)


# --- Tasks ---
class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'task_list.html'
    context_object_name = 'tasks'


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'task_detail.html'
    context_object_name = 'task'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.all()
        context['form'] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        task = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.task = task
            comment.author = request.user
            comment.save()
            messages.success(request, "Comment added successfully!")
            return redirect('task_detail', pk=task.pk)

        context = self.get_context_data()
        context['form'] = form
        return render(request, self.template_name, context)


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    template_name = 'create_task.html'
    form_class = TaskForm
    success_url = reverse_lazy('task_list')

    def form_valid(self, form):
        messages.success(self.request, "Task created successfully!")
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    template_name = 'edit_task.html'
    form_class = TaskForm

    def get_success_url(self):
        return reverse_lazy('task_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        messages.success(self.request, "Task updated successfully!")
        return super().form_valid(form)
