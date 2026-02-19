import requests
from faker import Faker
from datetime import datetime


def test_health_endpoint_returns_healthy(base_url):
    """Test that the health endpoint returns healthy"""
    response = requests.get(f'{base_url}/api/health')

    assert response.status_code == 200

    data = response.json()

    assert data['status'] == 'healthy'


def test_register_user_creates_new_user(base_url):
    """Test that a new user can be created"""
    fake = Faker()
    username = fake.user_name()
    payload = {'username': username, 'password': fake.password(length=10)}
    response = requests.post(f'{base_url}/api/auth/register', json=payload)

    assert response.status_code == 201

    data = response.json()

    assert 'user' in data
    assert data['user']['username'] == username
    assert data['message'] == 'User created successfully'


def test_register_user_creates_new_user_failed(base_url, registered_user):
    """Test that a new user can not be created with the same username"""
    fake = Faker()

    payload = {'username': registered_user['username'], 'password': fake.password(length=10)}
    response = requests.post(f'{base_url}/api/auth/register', json=payload)
    data = response.json()

    assert response.status_code == 400
    assert data['error'] == 'Username already exists'


def test_login_returns_jwt_token(base_url, registered_user):
    """Test that a user can login and receive a JWT token"""
    payload = {'username': registered_user['username'], 'password': registered_user['password']}
    response = requests.post(f'{base_url}/api/auth/login', json=payload)

    data = response.json()

    assert response.status_code == 200
    assert 'access_token' in data


def test_login_with_invalid_credentials(base_url, registered_user):
    """Test that a user can login and receive a JWT token"""
    payload = {'username': "Alice", 'password': registered_user['password']}
    response = requests.post(f'{base_url}/api/auth/login', json=payload)

    data = response.json()

    assert response.status_code == 401
    assert data['error'] == 'Invalid credentials'


def test_create_public_event_requires_auth_and_succeeds_with_token(base_url, logged_in_user, generated_event_title):
    """Test that a public event can be created with authentication"""
    fake_description = Faker().paragraph(nb_sentences=4)
    title = generated_event_title
    date = datetime.now().isoformat()
    payload = {
              "title": title,
              "description": fake_description,
              "date": date,
              "location": "Tech Hub, Room 101",
              "capacity": 50,
              "is_public": True,
              "requires_admin": False
    }

    response = requests.post(f'{base_url}/api/events', json=payload, headers={'Authorization': f'Bearer {logged_in_user}'})

    data = response.json()

    assert response.status_code == 201
    assert data['title'] == title
    assert data['description'] == fake_description
    assert data['date'] == date
    assert data['location'] == 'Tech Hub, Room 101'
    assert data['capacity'] == 50
    assert data['is_public'] == True
    assert data['requires_admin'] == False


def test_create_public_event_requires_auth_without_title_failed(base_url, logged_in_user):
    """Test that a public event can be created with authentication"""
    fake_description = Faker().paragraph(nb_sentences=4)
    date = datetime.now().isoformat()

    payload = {
              "title": "",
              "description": fake_description,
              "date": date,
              "location": "Tech Hub, Room 101",
              "capacity": 50,
              "is_public": True,
              "requires_admin": False
    }

    response = requests.post(f'{base_url}/api/events', json=payload, headers={'Authorization': f'Bearer {logged_in_user}'})
    assert response.status_code == 400
    data = response.json()
    assert data['error'] == 'Title is required'


def test_create_public_event_requires_auth_without_auth_failed(base_url, generated_event_title):
    """Test that a public event can not be created without authentication"""
    fake_description = Faker().paragraph(nb_sentences=4)
    title = generated_event_title

    date = datetime.now().isoformat()
    payload = {
              "title": title,
              "description": fake_description,
              "date": date,
              "location": "Tech Hub, Room 101",
              "capacity": 50,
              "is_public": True,
              "requires_admin": False
    }

    response = requests.post(f'{base_url}/api/events', json=payload)

    data = response.json()

    assert response.status_code == 401
    assert data['msg'] == 'Missing Authorization Header'


def test_rsvp_to_public_event_succeeds_without_auth(base_url, created_public_event_id):
    """Test that a public event can be RSVPed without authentication"""
    event_id = created_public_event_id
    response = requests.post(f'{base_url}/api/rsvps/event/{event_id}', json={})

    assert response.status_code == 201
    data = response.json()

    assert data['event_id'] == event_id
    assert data['attending'] == True



