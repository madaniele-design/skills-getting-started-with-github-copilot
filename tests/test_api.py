def test_root_redirect(client):
    """Test que la raíz sirve la página HTML (redirect seguido por StaticFiles)."""
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "<!DOCTYPE html>" in response.text


def test_get_activities(client):
    """Test obtener todas las actividades."""
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "Programming Class" in data
    # Verificar estructura de una actividad
    chess_club = data["Chess Club"]
    assert "description" in chess_club
    assert "schedule" in chess_club
    assert "max_participants" in chess_club
    assert "participants" in chess_club
    assert isinstance(chess_club["participants"], list)


def test_signup_success(client, sample_email):
    """Test registro exitoso en una actividad."""
    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": sample_email}
    )
    assert response.status_code == 200
    result = response.json()
    assert "message" in result
    assert sample_email in result["message"]
    # Verificar que se agregó a la lista
    get_response = client.get("/activities")
    activities = get_response.json()
    assert sample_email in activities["Chess Club"]["participants"]


def test_signup_duplicate(client, existing_email):
    """Test intentar registrarse dos veces (debe fallar)."""
    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": existing_email}
    )
    assert response.status_code == 400
    result = response.json()
    assert "detail" in result
    assert "Already signed up" in result["detail"]


def test_signup_non_existent_activity(client, sample_email, non_existent_activity):
    """Test registrarse en actividad que no existe."""
    response = client.post(
        f"/activities/{non_existent_activity}/signup",
        params={"email": sample_email}
    )
    assert response.status_code == 404
    result = response.json()
    assert "detail" in result
    assert "Activity not found" in result["detail"]


def test_remove_participant_success(client, sample_email):
    """Test remover participante exitosamente."""
    # Primero registrar
    client.post("/activities/Chess Club/signup", params={"email": sample_email})
    # Luego remover
    response = client.delete(f"/activities/Chess Club/participants/{sample_email}")
    assert response.status_code == 200
    result = response.json()
    assert "message" in result
    assert sample_email in result["message"]
    # Verificar que se removió
    get_response = client.get("/activities")
    activities = get_response.json()
    assert sample_email not in activities["Chess Club"]["participants"]


def test_remove_participant_not_signed_up(client, sample_email):
    """Test remover participante que no está registrado."""
    response = client.delete(f"/activities/Chess Club/participants/{sample_email}")
    assert response.status_code == 404
    result = response.json()
    assert "detail" in result
    assert "Participant not found" in result["detail"]


def test_remove_participant_non_existent_activity(client, sample_email, non_existent_activity):
    """Test remover participante de actividad que no existe."""
    response = client.delete(f"/activities/{non_existent_activity}/participants/{sample_email}")
    assert response.status_code == 404
    result = response.json()
    assert "detail" in result
    assert "Activity not found" in result["detail"]