from django.contrib.auth.models import Group, User, Permission
from django.contrib.contenttypes.models import ContentType

from employee_register.models import Employee
from employee_register.models import Requirement
from employee_register.models import Interviewer

class initialLoad():
    # data = Interviewer(name='NA',skill='NA')
    # data.save()
    # print('Initial data added to interviwer table (name:NA,skill:NA')

    superuser = User.objects.create_superuser(username="super.user", password="superuser")
    print('Super user created with id:super.user pass:superuser')

    developer_group, created = Group.objects.get_or_create(name="Developer")
    manager_group, created = Group.objects.get_or_create(name="Manager")
    interviewer_group, created = Group.objects.get_or_create(name="Interviewer")
    viewer_group, created = Group.objects.get_or_create(name="Viewer")
    print('4 new groups created (Developer,Manager,Interviewer,Viewer)')

    content_type = ContentType.objects.get_for_model(Employee)
    Employee_permission = Permission.objects.filter(content_type=content_type)
    print('Employee table permissions :',[perm.codename for perm in Employee_permission])
    # => ['add_employee', 'change_employee', 'delete_employee', 'view_employee']

    for perm in Employee_permission:
        if perm.codename == "view_employee":
            developer_group.permissions.add(perm)
            manager_group.permissions.add(perm)
            interviewer_group.permissions.add(perm)
            viewer_group.permissions.add(perm)
        elif perm.codename == "add_employee":
            developer_group.permissions.add(perm)
            manager_group.permissions.add(perm)
        elif perm.codename == "change_employee":
            developer_group.permissions.add(perm)
            manager_group.permissions.add(perm)
            interviewer_group.permissions.add(perm)
        elif perm.codename == "delete_employee":
            developer_group.permissions.add(perm)
            manager_group.permissions.add(perm)
    print('Permission related to Employee table is added to groups')

    content_type = ContentType.objects.get_for_model(Requirement)
    Requirement_permission = Permission.objects.filter(content_type=content_type)
    print('Requirement table permissions :',[perm.codename for perm in Requirement_permission])
    # => ['add_requirement', 'change_requirement', 'delete_requirement', 'view_requirement']

    for perm in Requirement_permission:
        if perm.codename == "view_requirement":
            developer_group.permissions.add(perm)
            manager_group.permissions.add(perm)
            viewer_group.permissions.add(perm)
        elif perm.codename == "add_requirement":
            developer_group.permissions.add(perm)
            manager_group.permissions.add(perm)
        elif perm.codename == "change_requirement":
            developer_group.permissions.add(perm)
            manager_group.permissions.add(perm)
        elif perm.codename == "delete_requirement":
            manager_group.permissions.add(perm)
    print('Permission related to Requirement table is added to groups')

    content_type = ContentType.objects.get_for_model(Interviewer)
    Interviewer_permission = Permission.objects.filter(content_type=content_type)
    print('Interviewer table permissions :',[perm.codename for perm in Interviewer_permission])
    # => ['add_interviewer', 'change_interviewer', 'delete_interviewer', 'view_interviewer']

    for perm in Interviewer_permission:
        if perm.codename == "view_interviewer":
            developer_group.permissions.add(perm)
            manager_group.permissions.add(perm)
            viewer_group.permissions.add(perm)
        elif perm.codename == "add_interviewer":
            manager_group.permissions.add(perm)
        elif perm.codename == "change_interviewer":
            manager_group.permissions.add(perm)
        elif perm.codename == "delete_interviewer":
            manager_group.permissions.add(perm)
    print('Permission related to Interviewer table is added to groups')

    content_type = ContentType.objects.get_for_model(User)
    User_permission = Permission.objects.filter(content_type=content_type)
    print('User table permissions :',[perm.codename for perm in User_permission])
    # => ['add_uuser', 'change_user', 'delete_user', 'view_user']

    for perm in User_permission:
        if perm.codename == "view_user":
            manager_group.permissions.add(perm)
            viewer_group.permissions.add(perm)
        elif perm.codename == "add_user":
            manager_group.permissions.add(perm)
        elif perm.codename == "change_user":
            manager_group.permissions.add(perm)
        elif perm.codename == "delete_user":
            manager_group.permissions.add(perm)
    print('Permission related to User table is added to groups')
