import pytest
from fake_login import fake_login

CASES = [
    ("TC-01", "test01", "abc12345", 0),
    ("TC-02", "test_02", "def67890", 0),
    ("TC-03", "test03", "Abc12345", 0),
    ("TC-04", "notexistuser", "Abc12345", 1001),
    ("TC-05", "test01", "Wrong123", 1001),
    ("TC-06", "test@01", "Abc12345", 1002),
    ("TC-07", "abcdefgh1234_abc", "Abc12345", 1001),
    ("TC-08", "abcdefgh1234_abcd", "Abc12345", 1002),
    ("TC-09", "test01", "Abc12345678901234567", 1001),
]

@pytest.mark.parametrize("case_id, username, password, expect_code", CASES)
def test_login(case_id, username, password, expect_code):
    result = fake_login(username, password)
    assert result["code"] == expect_code, f"{case_id} 期望 {expect_code} 实际 {result['code']}"
