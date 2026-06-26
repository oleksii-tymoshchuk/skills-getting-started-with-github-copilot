from fastapi.testclient import TestClient


def test_get_activities_returns_activity_list(client: TestClient):
    # Arrange
    expected_keys = {"Chess Club", "Programming Class", "Gym Class", "Soccer Team", "Swimming Club", "Art Studio", "Drama Workshop", "Science Olympiad", "Debate Club"}

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    activities = response.json()
    assert set(activities.keys()) == expected_keys
    assert activities["Chess Club"]["description"] == "Learn strategies and compete in chess tournaments"


def test_signup_for_activity_adds_participant(client: TestClient):
    # Arrange
    activity_name = "Chess Club"
    test_email = "newstudent@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": test_email})

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {test_email} for {activity_name}"}

    refresh_response = client.get("/activities")
    assert refresh_response.status_code == 200
    assert test_email in refresh_response.json()[activity_name]["participants"]


def test_signup_duplicate_participant_returns_400(client: TestClient):
    # Arrange
    activity_name = "Programming Class"
    test_email = "emma@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": test_email})

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_remove_participant_from_activity(client: TestClient):
    # Arrange
    activity_name = "Gym Class"
    participant_email = "john@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/participants/{participant_email}")

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Removed {participant_email} from {activity_name}"}

    refresh_response = client.get("/activities")
    assert refresh_response.status_code == 200
    assert participant_email not in refresh_response.json()[activity_name]["participants"]
