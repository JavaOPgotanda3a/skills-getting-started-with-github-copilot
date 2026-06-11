def test_unregister_removes_participant(client):
    # Arrange

    # Act
    response = client.delete(
        "/activities/Chess%20Club/unregister",
        params={"email": "michael@mergington.edu"},
    )

    # Assert
    assert response.status_code == 200
    assert response.json() == {
        "message": "Unregistered michael@mergington.edu from Chess Club"
    }


def test_unregister_rejects_missing_participant(client):
    # Arrange

    # Act
    response = client.delete(
        "/activities/Chess%20Club/unregister",
        params={"email": "not-signed-up@mergington.edu"},
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Student is not signed up for this activity"


def test_unregister_rejects_unknown_activity(client):
    # Arrange

    # Act
    response = client.delete(
        "/activities/Unknown%20Club/unregister",
        params={"email": "michael@mergington.edu"},
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"