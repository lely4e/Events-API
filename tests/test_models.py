from models import User


def test_user_password_hashing_behaves_correctly():
    """Test that the password hashing works as expected"""

    user = User(username='MadMax')
    raw_password = 'MadMaxPassword'

    user.set_password(raw_password)

    # Password hash should be different from the raw password
    assert user.password_hash != raw_password

    # Check that the raw password can be verified
    assert user.check_password(raw_password) is True



def test_user_password_hashing_behaves_wrong():
    """Test that the password hashing works not as expected"""

    user = User(username='MadMax')
    raw_password = 'MadMaxPassword'

    user.set_password(raw_password)

    # Password hash should be different from the raw password
    assert user.password_hash != raw_password

    assert user.check_password('wrong_password') is False