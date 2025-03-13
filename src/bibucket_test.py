from atlassian import Bitbucket
from settings import settings


def test_bitbucket_connection():
    # Initialize Bitbucket client
    bitbucket = Bitbucket(
        url=settings.BITBUCKET_URL,
        username=settings.BITBUCKET_USERNAME,
        password=settings.BITBUCKET_PASSWORD,
        verify_ssl=False,
    )

    """Test basic Bitbucket API connectivity by getting current user info"""
    try:
        # Get current user info
        current_user = bitbucket.get_current_user()
        print("Successfully connected to Bitbucket!")
        print(f"Current user: {current_user['displayName']}")
        print(f"Email: {current_user['emailAddress']}")
        return True
    except Exception as e:
        print(f"Error connecting to Bitbucket: {e}")
        return False


if __name__ == "__main__":
    test_bitbucket_connection()
