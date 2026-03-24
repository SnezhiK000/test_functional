from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from .models import Student, Course, Group


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = Student.objects.get(name=username)
        if user.password == password:
            request.session['user_id'] = user.id
            request.session['user_name'] = user.name
            user.last_login = timezone.now()
            user.save()
            messages.success(request, 'Вход выполнен!')
            return redirect('show_students')
    return render(request, 'login.html')


def logout_view(request):
    request.session.flush()
    return redirect('login_view')


def register_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        password = request.POST.get('password')
        group_id = request.POST.get('group')
        student = Student.objects.create(
            name=name,
            password=password,
            group=Group.objects.get(id=group_id)
        )
        return redirect('login_view')
    groups = Group.objects.all()
    return render(request, 'register.html', {'groups': groups})


def show_students(request):
    students = Student.objects.all()

    search = request.GET.get('search', '')
    if search:
        students = students.filter(Q(name__icontains=search))

    group_id = request.GET.get('group', '')
    if group_id:
        students = students.filter(group_id=group_id)

    sort = request.GET.get('sort', 'name')
    if sort == 'name_desc':
        students = students.order_by('-name')
    else:
        students = students.order_by('name')

    groups = Group.objects.all()
    return render(request, 'show_students.html', {
        'students': students,
        'groups': groups,
        'search': search,
        'group_id': group_id,
        'sort': sort
    })


def show_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        password = request.POST.get('password')
        group_id = request.POST.get('group')
        course_ids = request.POST.getlist('courses')
        student = Student.objects.create(
            name=name,
            password=password,
            group=Group.objects.get(id=group_id)
        )
        student.course.set(Course.objects.filter(id__in=course_ids))

        groups = Group.objects.all()
        courses = Course.objects.all()
        return render(request, 'show_create.html', {
            'groups': groups,
            'courses': courses
        })


def show_edit(request, id):
    student = get_object_or_404(Student, id=id)

    if request.method == 'POST':
        student.id = Student.objects.count() + 1
        student.name = request.POST.get('name')
        student.save()
        messages.success(request, 'Обновлено!')
        return redirect('show_students')

    return render(request, 'show_edit.html', {'student': student})


def show_delete(request, id):
    if request.method == 'POST':
            student = Student.objects.get(id=id)
            student.delete()
    return redirect('show_students')