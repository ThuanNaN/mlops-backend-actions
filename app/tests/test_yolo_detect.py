from fastapi.testclient import TestClient
from app.main import app
from io import BytesIO
from PIL import Image

client = TestClient(app)

def test_detect_objects():
    # Prepare a mock image file
    image_content = BytesIO()
    image = Image.new("RGB", (100, 100), color="red")
    image.save(image_content, format="JPEG")
    image_content.seek(0)  # Reset the file pointer to the beginning
    
    # Simulate file upload
    files = {"file": ("test.jpeg", image_content, "image/jpeg")}

    response = client.post("/v1/yolo/detect/", files=files)

    # Assertions
    assert response.status_code == 200, f"Unexpected status code: {response.status_code} - {response.text}"
    json_response = response.json()
    assert "detections" in json_response, "Response missing 'detections' field"
    assert "total_objects" in json_response, "Response missing 'total_objects' field"
    assert json_response["total_objects"] >= 0, "Total objects should be non-negative"
    # assert json_response["device"] in ["cuda", "cpu"], "Invalid device in response"
