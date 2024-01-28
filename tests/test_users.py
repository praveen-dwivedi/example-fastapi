import pytest
from jose import jwt
from app import schemas
# from .database import client,session
from app.config import settings


    

def test_root(client, session):
    res = client.get("/")
    # print(res.json().get("message"))
    assert res.json().get("message") == "Hello Explorers, welcome to amazing word of APIs, serving from cloud ubuntu"
    assert res.status_code == 200


def test_create_user(client,session):
    res = client.post("/users", json={"email":"hello123@gmail.com", "password":"password123"}
    )
    new_user = schemas.UserOut(**res.json())   
    # print(res.json())
    assert new_user.email == "hello123@gmail.com"
    assert res.status_code == 201 


def test_login_user(client, test_user):
    res = client.post("/login", data={"username":test_user["email"], "password":test_user["password"]}
    )
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=[settings.algorithm])
    id = payload.get("user_id")
    assert id == test_user['id']
    assert login_res.token_type == "bearer"
    assert res.status_code == 200


@pytest.mark.parametrize("email, password, status_code", [
    ('wromngemail@gmail.com', 'password123', 403),
    ('sample@gmail.com', 'wrongpassword', 403),
    ('wromngemail@gmail.com', 'wrongpassword', 403),
    (None, 'password123', 422),
    ('sample@gmail.com', None, 422),
])
def test_incorrect_login(test_user, client, email, password, status_code):
    res = client.post("/login", data={"username":email, "password":password}
    )

    assert res.status_code == status_code
    # assert res.json().get('detail') == "Invalid Credentials"
