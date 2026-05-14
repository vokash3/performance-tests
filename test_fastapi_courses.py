from fastapi.testclient import TestClient

from fastapi_courses import app, store


client = TestClient(app)


def setup_function():
    """
    Очищаем in-memory хранилище перед каждым тестом.
    """
    store.root = []


def test_create_course():
    response = client.post(
        "/api/v1/courses",
        json={
            "title": "Python Basics",
            "max_score": 100,
            "min_score": 60,
            "description": "Introduction to Python"
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert data["id"] == 1
    assert data["title"] == "Python Basics"
    assert data["max_score"] == 100
    assert data["min_score"] == 60
    assert data["description"] == "Introduction to Python"


def test_get_courses():
    client.post(
        "/api/v1/courses",
        json={
            "title": "FastAPI",
            "max_score": 100,
            "min_score": 50,
            "description": "FastAPI course"
        }
    )

    response = client.get("/api/v1/courses")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["title"] == "FastAPI"


def test_get_course_by_id():
    client.post(
        "/api/v1/courses",
        json={
            "title": "Docker",
            "max_score": 90,
            "min_score": 45,
            "description": "Docker course"
        }
    )

    response = client.get("/api/v1/courses/1")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == 1
    assert data["title"] == "Docker"


def test_get_course_not_found():
    response = client.get("/api/v1/courses/999")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Course with id 999 not found"
    }


def test_update_course():
    client.post(
        "/api/v1/courses",
        json={
            "title": "Old Course",
            "max_score": 50,
            "min_score": 20,
            "description": "Old description"
        }
    )

    response = client.put(
        "/api/v1/courses/1",
        json={
            "title": "Updated Course",
            "max_score": 100,
            "min_score": 70,
            "description": "Updated description"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == 1
    assert data["title"] == "Updated Course"
    assert data["max_score"] == 100
    assert data["min_score"] == 70
    assert data["description"] == "Updated description"


def test_update_course_not_found():
    response = client.put(
        "/api/v1/courses/999",
        json={
            "title": "No Course",
            "max_score": 100,
            "min_score": 50,
            "description": "Does not exist"
        }
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Course with id 999 not found"
    }


def test_delete_course():
    client.post(
        "/api/v1/courses",
        json={
            "title": "Delete Me",
            "max_score": 100,
            "min_score": 50,
            "description": "Temporary course"
        }
    )

    response = client.delete("/api/v1/courses/1")

    assert response.status_code == 204

    response = client.get("/api/v1/courses/1")

    assert response.status_code == 404


def test_delete_course_not_found():
    response = client.delete("/api/v1/courses/999")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Course with id 999 not found"
    }