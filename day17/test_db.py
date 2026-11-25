from db import query
def test_users_count():
    rows = query("SELECT COUNT(*) AS c FROM users")
    assert rows[0]["c"] == 20
