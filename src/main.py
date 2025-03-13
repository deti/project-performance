import argparse
from datetime import datetime

from settings import settings
from jira_data import get_jira_metrics
from utils import make_file_name
from bibucket_test import test_bitbucket_connection


def validate_date(date_str):
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return date_str
    except ValueError:
        raise argparse.ArgumentTypeError("Invalid date format. Please use YYYY-MM-DD")


def parse_args():
    parser = argparse.ArgumentParser(
        description="JIRA and Bitbucket metrics collection tool"
    )

    parser.add_argument(
        "--print-env",
        "-e",
        action="store_true",
        help="Print environment variables",
        default=False,
    )

    parser.add_argument(
        "--test-jira",
        "-tj",
        action="store_true",
        help="Test JIRA connection",
        default=False,
    )

    parser.add_argument(
        "--test-bitbucket",
        "-tb",
        action="store_true",
        help="Test Bitbucket connection",
        default=False,
    )

    parser.add_argument(
        "--start-date",
        "-d",
        type=validate_date,
        help="Start date for metrics collection (YYYY-MM-DD)",
    )

    parser.add_argument(
        "--get-jira",
        "-gj",
        action="store_true",
        help="Get JIRA metrics",
        default=False,
    )

    parser.add_argument(
        "--get-bitbucket",
        "-gb",
        action="store_true",
        help="Get Bitbucket metrics",
        default=False,
    )

    return parser.parse_args()


def main():
    args = parse_args()

    if args.print_env:
        print("\nEnvironment Variables:")
        print(f"JIRA URL: {settings.JIRA_URL}")
        print(f"JIRA Username: {settings.JIRA_USERNAME}")
        print(f"Bitbucket URL: {settings.BITBUCKET_URL}")
        print(f"Bitbucket Username: {settings.BITBUCKET_USERNAME}\n")

    if args.test_jira:
        print("\nTesting JIRA connection...")
        # TODO: Add JIRA connection test
        print("JIRA connection test not implemented yet\n")

    if args.test_bitbucket:
        print("\nTesting Bitbucket connection...")
        test_bitbucket_connection()
        print()

    if args.get_jira:
        if not args.start_date:
            print("Error: --start-date is required for getting JIRA metrics")
            return
        print(f"\nGetting JIRA metrics from {args.start_date}...")
        filename = make_file_name("jira_metrics.xlsx", args.start_date)
        jira_df = get_jira_metrics(start_date=args.start_date)

        # Export the DataFrame to Excel
        jira_df.to_excel(filename, index=False)

        # TODO: Save metrics to file
        print(f"JIRA metrics saved to {filename}\n")

    if args.get_bitbucket:
        if not args.start_date:
            print("Error: --start-date is required for getting Bitbucket metrics")
            return
        print(f"\nGetting Bitbucket metrics from {args.start_date}...")
        # TODO: Add Bitbucket metrics collection
        print("Bitbucket metrics collection not implemented yet\n")


if __name__ == "__main__":
    main()
