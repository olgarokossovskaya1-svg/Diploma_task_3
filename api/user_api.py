import requests
from data.urls import Urls
from faker import Faker

fake = Faker()

def create_user():
    user = {
        "email": fake.email(),
        "password": fake.password(),
        "name": fake.name()
    }
    response = requests.post(f"{Urls.BASE_URL}/api/auth/register", data=user)
    response_data = response.json()
    return {
        **user,
        "accessToken": response_data.get("accessToken"),
        "refreshToken": response_data.get("refreshToken"),
        "user": response_data.get("user")
    }

def delete_user(access_token):
    if access_token:
        headers = {"Authorization": access_token}
        requests.delete(f"{Urls.BASE_URL}/api/auth/user", headers=headers)