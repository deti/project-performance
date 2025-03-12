from jira import JIRA
from settings import settings


def test_jira_connection():
    """Test that we can connect to JIRA and fetch a ticket"""
    # Initialize JIRA client
    jira = JIRA(server=settings.JIRA_BASE_URL, token_auth=settings.JIRA_API_KEY)

    # Create test JQL query to get a single issue
    jql = f"project = {settings.JIRA_PROJECT_KEY} ORDER BY created DESC"

    # Fetch single issue
    issues = jira.search_issues(jql, maxResults=1)

    # Verify we got a result
    assert len(issues) > 0

    # Get the first issue
    issue = issues[0]

    # Verify basic issue fields are accessible
    assert issue.key is not None
    assert issue.fields.summary is not None
    assert issue.fields.created is not None

    # Print issue details for manual verification
    print("\nTest Issue Details:")
    print(f"Key: {issue.key}")
    print(f"Summary: {issue.fields.summary}")
    print(f"Created: {issue.fields.created}")
    print(f"Status: {issue.fields.status}")
    print(f"Assignee: {getattr(issue.fields.assignee, 'displayName', 'Unassigned')}")
