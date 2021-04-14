import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dinesafelysite.settings")
django.setup()

from user.models import DineSafelyUser  # noqa: E402


TEST_USERS = [
    # Team 1 test users
    {"username": "test.modou", "email": "t1test1@gmail.com", "password": "Test-mo1234"},
    {"username": "hahnTest", "email": "t1test2@gmail.com", "password": "Testing12345"},
    {"username": "test.parth", "email": "t1test3@gmail.com", "password": "Test1234$$"},
    {"username": "testSimay", "email": "t1test4@gmail.com", "password": "Heroku1234"},
    {
        "username": "test.xiaodan",
        "email": "t1test5@gmail.com",
        "password": "123456Test",
    },
    {"username": "test.prof", "email": "t1test6@gmail.com", "password": "123456Test"},
    {"username": "test.jack", "email": "t1test7@gmail.com", "password": "123456Test"},
    # Team 2 test users
    {"username": "testProf", "email": "gcivil@nyu.edu", "password": "Test123456"},
    {"username": "testTa", "email": "test_ta@gmail.com", "password": "Test123456"},
    {"username": "test.Bruce", "email": "test_1@gmail.com", "password": "Test123456"},
    {"username": "test.Ahmed", "email": "test_2@gmail.com", "password": "Test123456"},
    {
        "username": "test.Changheng",
        "email": "test_3@gmail.com",
        "password": "Test123456",
    },
    {"username": "test.Yuhan", "email": "test_4@gmail.com", "password": "Test123456"},
    {"username": "testMember5", "email": "test_5@gmail.com", "password": "Test123456"},
]


def add_test_users():
    for test_user in TEST_USERS:
        # Check if user already exists
        user_query = DineSafelyUser.objects.filter(
            username=test_user.get("username")
        ).first()
        if user_query:
            continue
        # Create user if it doesn't exit
        user = DineSafelyUser(
            username=test_user.get("username"), email=test_user.get("email")
        )
        user.set_password(test_user.get("password"))
        user.save()


if __name__ == "__main__":
    add_test_users()
