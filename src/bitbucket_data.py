from datetime import datetime
from typing import Dict, List

import matplotlib.pyplot as plt
import pandas as pd
from atlassian import Bitbucket
from settings import settings
from utils import make_file_name

# Initialize Bitbucket client
bitbucket = Bitbucket(
    url=settings.BITBUCKET_URL,
    username=settings.BITBUCKET_USERNAME,
    password=settings.BITBUCKET_PASSWORD,
    verify_ssl=False,
)


def fetch_pull_requests(start_date: str) -> List[Dict]:
    """
    Fetch all pull requests since start_date, handling pagination
    """
    pull_requests = []
    start = 0
    limit = 100

    while True:
        try:
            result = bitbucket.get_pull_requests(
                project=settings.BITBUCKET_PROJECT,
                repository=settings.BITBUCKET_REPO,
                state="all",
                start=start,
                limit=limit,
            )

            if not result:
                break

            # Filter PRs by date
            filtered_prs = [
                pr
                for pr in result
                if datetime.strptime(pr["created_on"][:10], "%Y-%m-%d")
                >= datetime.strptime(start_date, "%Y-%m-%d")
            ]

            pull_requests.extend(filtered_prs)
            start += limit

            if len(result) < limit:
                break

        except Exception as e:
            print(f"Error fetching pull requests: {e}")
            break

    return pull_requests


def calculate_metrics(pull_requests: List[Dict]) -> pd.DataFrame:
    """
    Calculate PR metrics including review time, comments, and approval rates
    """
    metrics = []

    for pr in pull_requests:
        created = datetime.strptime(pr["created_on"][:10], "%Y-%m-%d")
        updated = datetime.strptime(pr["updated_on"][:10], "%Y-%m-%d")

        # Get PR activity details
        try:
            activities = bitbucket.get_pull_request_activities(
                project=settings.BITBUCKET_PROJECT,
                repository=settings.BITBUCKET_REPO,
                pull_request_id=pr["id"],
            )
        except Exception as e:
            print(f"Error fetching PR activities: {e}")
            continue

        comment_count = sum(1 for a in activities if a["action"] == "COMMENTED")
        approvals = [a for a in activities if a["action"] == "APPROVED"]

        metrics.append(
            {
                "pr_id": pr["id"],
                "author": pr["author"]["displayName"],
                "created_date": created,
                "completion_date": updated,
                "review_time_days": (updated - created).days,
                "comment_count": comment_count,
                "approval_count": len(approvals),
                "state": pr["state"],
            }
        )

    return pd.DataFrame(metrics)


def visualize_metrics(df: pd.DataFrame, start_date: str):
    """
    Create visualizations for PR metrics
    """
    plt.style.use("seaborn-v0_8-whitegrid")

    # 1. PRs per Contributor
    plt.figure(figsize=(12, 6))
    df["author"].value_counts().plot(kind="bar")
    plt.title("Pull Requests per Contributor")
    plt.xlabel("Contributor")
    plt.ylabel("Number of PRs")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(make_file_name(start_date, "prs_per_contributor.png"))
    plt.close()

    # 2. Review Time Distribution
    plt.figure(figsize=(10, 6))
    plt.hist(df["review_time_days"], bins=20, edgecolor="black")
    plt.title("PR Review Time Distribution")
    plt.xlabel("Days")
    plt.ylabel("Frequency")
    plt.savefig(make_file_name(start_date, "review_time_distribution.png"))
    plt.close()

    # 3. PR Approval Rate
    approval_rate = (df["state"] == "MERGED").mean() * 100
    plt.figure(figsize=(8, 8))
    plt.pie(
        [approval_rate, 100 - approval_rate],
        labels=["Approved", "Not Approved"],
        autopct="%1.1f%%",
    )
    plt.title("Pull Request Approval Rate")
    plt.savefig(make_file_name(start_date, "pr_approval_rate.png"))
    plt.close()

    # Save metrics to Excel
    excel_file = make_file_name(start_date, "pr_metrics.xlsx")
    with pd.ExcelWriter(excel_file) as writer:
        df.to_excel(writer, sheet_name="PR Metrics", index=False)

        # Summary statistics
        summary = pd.DataFrame(
            {
                "Metric": [
                    "Total PRs",
                    "Average Review Time (days)",
                    "Average Comments per PR",
                    "Approval Rate (%)",
                ],
                "Value": [
                    len(df),
                    df["review_time_days"].mean(),
                    df["comment_count"].mean(),
                    approval_rate,
                ],
            }
        )
        summary.to_excel(writer, sheet_name="Summary", index=False)


def analyze_pull_requests(start_date: str = "2025-01-01"):
    """
    Main function to analyze pull request data
    """
    print(f"Fetching pull requests since {start_date}...")
    pull_requests = fetch_pull_requests(start_date)

    if not pull_requests:
        print("No pull requests found for the specified period.")
        return

    print(f"Calculating metrics for {len(pull_requests)} pull requests...")
    metrics_df = calculate_metrics(pull_requests)

    print("Generating visualizations and saving data...")
    visualize_metrics(metrics_df, start_date)
    print("Analysis complete!")
