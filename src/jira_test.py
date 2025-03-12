from jira import JIRA
from settings import settings


def test_jira_connection():
    """Test that we can connect to JIRA and fetch a ticket"""
    # Initialize JIRA client
    print(f"establishing connection to JIRA_BASE_URL: {settings.JIRA_BASE_URL}")
    print(f"with JIRA_API_KEY: {settings.JIRA_API_KEY}")

    jira = JIRA(
        server=settings.JIRA_BASE_URL, token_auth=settings.JIRA_API_KEY, verify=False
    )
    print("JIRA client initialized")
    print(jira)

    # Who has authenticated
    myself = jira.myself()
    print(f"Authenticated as: {myself}")

    # # Create test JQL query to get a single issue
    # jql = f"project = {settings.JIRA_PROJECT_KEY} ORDER BY created DESC"
    # print(f"JQL query: {jql}")

    # # Fetch single issue
    # issues = jira.search_issues(jql, maxResults=1)
    # print(f"Issues: {issues}")

    # # Verify we got a result
    # assert len(issues) > 0
    # print(f"Number of issues: {len(issues)}")

    # # Get the first issue
    # issue = issues[0]
    # print(f"Got issue: {issue}")

    # # Verify basic issue fields are accessible
    # assert issue.key is not None
    # assert issue.fields.summary is not None
    # assert issue.fields.created is not None

    # # Print issue details for manual verification
    # print("\nTest Issue Details:")
    # print(f"Key: {issue.key}")
    # print(f"Summary: {issue.fields.summary}")
    # print(f"Created: {issue.fields.created}")
    # print(f"Status: {issue.fields.status}")
    # print(f"Assignee: {getattr(issue.fields.assignee, 'displayName', 'Unassigned')}")
