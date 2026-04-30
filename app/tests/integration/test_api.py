def test_register_response_200(create_client):
    payload = {"username": "lily",
               "password": "12345678"}
    response = create_client.post("/users/register", json=payload)


def test_login_response_401(create_client):
    payload = {"username": "test",
               "password": "12345678"}
    response = create_client.post("/users/login", data=payload)
    assert response.status_code == 401


