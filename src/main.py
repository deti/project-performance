from settings import settings

if __name__ == "__main__":
    print(f"JIRA_API_KEY: {settings.JIRA_API_KEY}")
    print(f"JIRA_BASE_URL: {settings.JIRA_BASE_URL}")
    print(f"JIRA_PROJECT_KEY: {settings.JIRA_PROJECT_KEY}")
    print(f"BITBUCKET_API_KEY: {settings.BITBUCKET_API_KEY}")
    print(f"BITBUCKET_BASE_URL: {settings.BITBUCKET_BASE_URL}")
    print(f"BITBUCKET_PROJECT_KEY: {settings.BITBUCKET_PROJECT_KEY}")
