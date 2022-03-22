from fastapi.testclient import TestClient

from tps_blog.main import app


client = TestClient(app)

# Test Home (/) Route
def test_get_home():
    response = client.get("/")
    assert response.status_code == 200


# Test /pages/{page_name} route
def test_get_pages_about():
    response = client.get("/pages/about")
    assert response.status_code == 200


def test_get_pages_notfound():
    response = client.get("/pages/non_existant_page")
    assert response.status_code == 404
