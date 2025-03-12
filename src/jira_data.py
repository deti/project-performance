from datetime import datetime
from typing import Dict, List

import matplotlib.pyplot as plt
import pandas as pd
from jira import JIRA
from settings import settings
from utils import make_file_name

# Initialize JIRA client
jira = JIRA(
    server=settings.JIRA_BASE_URL,
    token_auth=settings.JIRA_API_KEY,
    options={"verify": False},
)


def fetch_issues(start_date: str) -> List[Dict]:
    """
    Fetch all issues from JIRA board since start_date, handling pagination
    """
    issues = []
    start_at = 0
    max_results = 100

    jql = f'project = {settings.JIRA_PROJECT_KEY} AND updated >= "{start_date}" ORDER BY updated DESC'

    result = jira.search_issues(
        jql, startAt=start_at, maxResults=max_results, expand=["changelog"]
    )
    print(f"Result: {result}")

    
    # while True:
    #     result = jira.search_issues(
    #         jql, startAt=start_at, maxResults=max_results, expand=["changelog"]
    #     )

    #     if not result.issues:
    #         break

    #     issues.extend(result.issues)
    #     start_at += max_results

    #     if len(result.issues) < max_results:
    #         break

    return issues


def calculate_metrics(issues: List[Dict]) -> pd.DataFrame:
    """
    Calculate cycle time, lead time and other metrics for each issue
    """
    metrics = []

    for issue in issues:
        created = datetime.strptime(issue.fields.created[:10], "%Y-%m-%d")

        # Find start and completion dates from changelog
        start_date = None
        completion_date = None

        for history in issue.changelog.histories:
            for item in history.items:
                if item.field == "status":
                    if item.toString == "In Progress" and not start_date:
                        start_date = datetime.strptime(history.created[:10], "%Y-%m-%d")
                    elif item.toString == "Done":
                        completion_date = datetime.strptime(
                            history.created[:10], "%Y-%m-%d"
                        )

        if completion_date:
            cycle_time = (completion_date - (start_date or created)).days
            lead_time = (completion_date - created).days

            metrics.append(
                {
                    "issue_key": issue.key,
                    "assignee": getattr(
                        issue.fields.assignee, "displayName", "Unassigned"
                    ),
                    "created_date": created,
                    "completion_date": completion_date,
                    "cycle_time": cycle_time,
                    "lead_time": lead_time,
                }
            )

    return pd.DataFrame(metrics)


def calculate_throughput(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate weekly and monthly throughput
    """
    weekly_throughput = df.resample("W", on="completion_date").size()
    monthly_throughput = df.resample("M", on="completion_date").size()

    return weekly_throughput, monthly_throughput


def visualize_metrics(df: pd.DataFrame, start_date: str):
    """
    Create visualizations for the metrics
    """
    # Set up the plotting style
    plt.style.use("seaborn")

    # 1. Cycle Time Distribution
    plt.figure(figsize=(10, 6))
    plt.hist(df["cycle_time"], bins=20, edgecolor="black")
    plt.title("Cycle Time Distribution")
    plt.xlabel("Days")
    plt.ylabel("Frequency")
    plt.savefig(make_file_name(start_date, "cycle_time_distribution.png"))
    plt.close()
    print("cycle_time_distribution.png saved")

    # 2. Throughput Trends
    weekly_tp, monthly_tp = calculate_throughput(df)

    plt.figure(figsize=(12, 6))
    weekly_tp.plot(kind="line")
    plt.title("Weekly Throughput Trend")
    plt.xlabel("Week")
    plt.ylabel("Completed Issues")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(make_file_name(start_date, "weekly_throughput.png"))
    plt.close()
    print("weekly_throughput.png saved")

    # 3. Individual Contributor Metrics
    contributor_metrics = (
        df.groupby("assignee")
        .agg({"issue_key": "count", "cycle_time": "mean"})
        .reset_index()
    )

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))

    contributor_metrics.plot(
        kind="bar",
        x="assignee",
        y="issue_key",
        ax=ax1,
        title="Tasks Completed per Contributor",
    )
    ax1.set_ylabel("Number of Tasks")

    contributor_metrics.plot(
        kind="bar",
        x="assignee",
        y="cycle_time",
        ax=ax2,
        title="Average Cycle Time per Contributor",
    )
    ax2.set_ylabel("Days")

    plt.tight_layout()
    plt.savefig(make_file_name(start_date, "contributor_metrics.png"))
    plt.close()
    print("contributor_metrics.png saved")


def get_jira_metrics(start_date: str = "2025-01-01") -> pd.DataFrame:
    # Fetch issues since January 1, 2025
    issues = fetch_issues(start_date)

    # Calculate metrics
    metrics_df = calculate_metrics(issues)

    # Generate visualizations
    visualize_metrics(metrics_df, start_date)

    # Print summary statistics
    print("\nSummary Statistics:")
    print(f"Total Issues: {len(metrics_df)}")
    print(f"Average Cycle Time: {metrics_df['cycle_time'].mean():.2f} days")
    print(f"Average Lead Time: {metrics_df['lead_time'].mean():.2f} days")

    return metrics_df
