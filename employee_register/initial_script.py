from django.contrib.auth.models import Group, User, Permission
from django.contrib.contenttypes.models import ContentType
from employee_register.models import Employee
from employee_register.models import Requirement
from employee_register.models import Interviewer

class initialLoad():
    developer_group, created = Group.objects.get_or_create(name="Developer")
    manager_group, created = Group.objects.get_or_create(name="Manager")
    interviewer_group, created = Group.objects.get_or_create(name="Interviewer")
    viewer_group, created = Group.objects.get_or_create(name="Viewer")
    print('4 new groups created (Developer,Manager,Interviewer,Viewer)')

    content_type = ContentType.objects.get_for_model(Employee)
    Employee_permission = Permission.objects.filter(content_type=content_type)
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
