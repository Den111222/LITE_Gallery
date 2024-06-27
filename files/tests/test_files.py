import pytest
from fastapi.testclient import TestClient
from fastapi import UploadFile
from api.v1.files import get_file_service
from files.main import app

client = TestClient(app)


# Mock FileService and methods
class MockFileService:
    async def get_project_images(self, project_id: int):
        return {"status": "success", "data": ["image1.jpg", "image2.jpg"]}

    async def get_upload_link(self, filename: str, project_id: int):
        return {"status": "success", "data": {"upload_link": "/upload_file/c2d08ba2-fced-417b-838d-30a94a465fbc",
                         "params": {"project_id": 1},
                         "message": "Link valid for 0:30:00 minutes"}
                }

    async def upload_image(self, image_id: str, file: UploadFile):
        return {"status": "success", "data": {"message": "Image uploaded successfully"}}

def get_mock_file_service():
    return MockFileService()


@pytest.fixture(autouse=True)
def override_dependency():
    app.dependency_overrides[get_file_service] = get_mock_file_service
    yield
    app.dependency_overrides.clear()


def test_get_project_images():
    response = client.get("/api/v1/files/projects/1/images")
    assert response.status_code == 200
    assert response.json() == {"data": ["image1.jpg", "image2.jpg"]}


def test_get_upload_link():
    response = client.post("api/v1/files/upload/?filename=testfile&project_id=1")
    assert response.status_code == 200
    assert response.json()['data']['params'] == {'project_id': 1}


def test_upload_image():
    with open("testfile.jpg", "wb") as f:
        f.write(b"this is a test file")

    with open("testfile.jpg", "rb") as f:
        response = client.post("/api/v1/files/upload_file/c2d08ba2-fced-417b-838d-30a94a465fbc", files={"file": f})

    assert response.status_code == 200
    assert response.json() == {'data': {'message': 'Image uploaded successfully'}}
