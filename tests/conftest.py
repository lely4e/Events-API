import pytest
from faker import Faker
import requests
import random
from datetime import datetime


BASE_URL = "http://127.0.0.1:5005/"


@pytest.fixture(scope="session")
def base_url():
    return BASE_URL


@pytest.fixture()
def registered_user(base_url):
    """Register a new user"""
    fake = Faker()
    username = fake.user_name()
    password = fake.password(length=10)

    response = requests.post(f'{base_url}/api/auth/register', json={'username': username, 'password': password})
    assert response.status_code in [200, 201], f'Registration failed: {response.text}'

    return {
        'username': username,
        'password': password
    }


@pytest.fixture()
def logged_in_user(base_url, registered_user):
    """Log in a registered user and return the JWT token"""
    payload = {'username': registered_user['username'], 'password': registered_user['password']}

    response = requests.post(f'{base_url}/api/auth/login', json=payload)
    assert response.status_code == 200, f'Registration failed: {response.text}'

    data = response.json()
    return data['access_token']


@pytest.fixture()
def generated_event_title():
    """Generate a random event title"""
    adjectives = ["Global", "NextGen", "Future", "Creative", "Innovative"]
    topics = ["AI", "Healthcare", "Marketing", "Tech", "Finance", "Education"]
    nouns = ["Summit", "Conference", "Workshop", "Expo", "Forum", "Meetup"]

    return f"{random.choice(adjectives)} {random.choice(topics)} {random.choice(nouns)}"


@pytest.fixture()
def created_public_event_id(base_url, logged_in_user, generated_event_title):
    """Create a public event and return its ID"""
    fake_description = Faker().paragraph(nb_sentences=4)
    payload = {
        "title": generated_event_title,
        "description": fake_description,
        "date": datetime.now().isoformat(),
        "location": "Tech Hub, Room 101",
        "capacity": 50,
        "is_public": True,
        "requires_admin": False
    }

    response = requests.post(f'{base_url}/api/events', json=payload,
                             headers={'Authorization': f'Bearer {logged_in_user}'})

    assert response.status_code == 201

    return response.json()['id']