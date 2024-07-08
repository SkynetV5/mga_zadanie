import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from tasks.models import Task

@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def create_user():
    user = User.objects.create_user(username='testuser',password='password',email='testuser@gmail.com')
    return user


@pytest.fixture
def create_task(create_user):
    task = Task.objects.create(
        name ="Test task",
        description = 'Test description',
        assigned_user = create_user,
        status = 'Nowy'
    )
    return task


@pytest.fixture
def create_task_2(create_user):
    task = Task.objects.create(
        name ="Test task 2",
        description = 'Test description 2',
        assigned_user = create_user,
        status = 'W toku'
    )
    return task


@pytest.fixture
def authenticate(api_client,create_user):
    response = api_client.post(reverse('token_obtain_pair'), {
        'username': 'testuser',
        'password': 'password'
    })

    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {response.data['access']}')
    return api_client , create_user

@pytest.mark.django_db
class TestTaskHistoryViewSet:

    def test_task_history_view(self,authenticate,create_task,create_task_2, create_user):
        url = reverse('task-history-list')
        api_client , user = authenticate
        response = api_client.get(url)


        assert response.status_code == status.HTTP_200_OK

        assert len(response.data) == 2
        assert response.data[0]['name'] == 'Test task 2'
        assert response.data[0]['description'] == 'Test description 2'
        assert response.data[0]['assigned_user'] == user.id
        assert response.data[0]['status'] == 'W toku'

        assert response.data[1]['name'] == 'Test task'
        assert response.data[1]['description'] == 'Test description'
        assert response.data[1]['assigned_user'] == user.id
        assert response.data[1]['status'] == 'Nowy'


@pytest.mark.django_db
class TestTaskViewSet:

    def test_task_creation(self, authenticate):
        url = reverse('task-list')
        api_client , user = authenticate
        data = {
            'name': 'New Task',
            'description': 'New Description',
            'assigned_user': user.id,
            'status': 'Nowy'
        }

        data2 = {
            'name': 'New Task 2',
            'description': 'New Description 2',
            'assigned_user': user.id,
            'status': 'W toku'
        }

        response = api_client.post(url,data,format='json')
        response2 = api_client.post(url,data2,format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['name'] == 'New Task'
        assert response.data['description'] == 'New Description'

        assert response2.status_code == status.HTTP_201_CREATED
        assert response2.data['name'] == 'New Task 2'
        assert response2.data['description'] == 'New Description 2'


        
    def test_task_view(self,authenticate,create_task, create_task_2, create_user):
        url = reverse('task-list')
        api_client, user = authenticate
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2
        assert response.data[0]['name'] == 'Test task'
        assert response.data[0]['description'] == 'Test description'
        assert response.data[0]['assigned_user'] == user.id
        assert response.data[0]['status'] == 'Nowy'

        assert response.data[1]['name'] == 'Test task 2'
        assert response.data[1]['description'] == 'Test description 2'
        assert response.data[1]['assigned_user'] == user.id
        assert response.data[1]['status'] == 'W toku'