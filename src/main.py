from settings import settings
from jira_data import get_jira_metrics
from utils import make_file_name

if __name__ == "__main__":
    print(f"JIRA_API_KEY: {settings.JIRA_API_KEY}")
    print(f"JIRA_BASE_URL: {settings.JIRA_BASE_URL}")
    print(f"JIRA_PROJECT_KEY: {settings.JIRA_PROJECT_KEY}")
    print(f"BITBUCKET_API_KEY: {settings.BITBUCKET_API_KEY}")
    print(f"BITBUCKET_BASE_URL: {settings.BITBUCKET_BASE_URL}")
    print(f"BITBUCKET_PROJECT_KEY: {settings.BITBUCKET_PROJECT_KEY}")

    # test_jira_connection()

    start_date = "2025-01-01"
    jira_df = get_jira_metrics(start_date=start_date)

    # Export the DataFrame to Excel
    jira_df.to_excel(make_file_name(start_date, "jira_metrics.xlsx"), index=False)
    print("\nData exported to jira_metrics.xlsx")
