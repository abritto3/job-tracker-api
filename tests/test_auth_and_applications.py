def register(client, email="test@example.com", password="strongpassword123"):
    r = client.post("/auth/register", json={"email": email, "password": password})
    assert r.status_code in (201, 400)  # 400 if already exists
    return r


def login(client, email="test@example.com", password="strongpassword123"):
    r = client.post("/auth/login", data={"username": email, "password": password})
    assert r.status_code == 200, r.text
    token = r.json()["access_token"]
    return token


def auth_headers(token: str):
    return {"Authorization": f"Bearer {token}"}


def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_register_login_me(client):
    register(client)
    token = login(client)
    r = client.get("/me", headers=auth_headers(token))
    assert r.status_code == 200
    assert r.json()["email"] == "test@example.com"


def test_applications_crud(client):
    register(client)
    token = login(client)

    # Create
    payload = {
        "company": "Monzo",
        "role_title": "Backend Engineer",
        "status": "applied",
        "location": "London",
        "link": "https://example.com/job",
        "notes": "Applied via company site",
    }
    r = client.post("/applications", json=payload, headers=auth_headers(token))
    assert r.status_code == 201, r.text
    app_id = r.json()["id"]

    # List
    r = client.get("/applications", headers=auth_headers(token))
    assert r.status_code == 200
    assert len(r.json()) >= 1

    # Filter
    r = client.get("/applications?status=applied", headers=auth_headers(token))
    assert r.status_code == 200
    assert all(a["status"] == "applied" for a in r.json())

    # Update
    r = client.patch(f"/applications/{app_id}", json={"status": "interview"}, headers=auth_headers(token))
    assert r.status_code == 200
    assert r.json()["status"] == "interview"

    # Soft delete
    r = client.delete(f"/applications/{app_id}", headers=auth_headers(token))
    assert r.status_code == 204

    # Confirm it disappears (default include_inactive=false)
    r = client.get("/applications", headers=auth_headers(token))
    assert r.status_code == 200
    assert all(a["id"] != app_id for a in r.json())
