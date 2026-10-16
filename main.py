"""
HR Data Analysis
===============

Human Resources data analysis using Python and Pandas.

This project integrates employee records from two offices with
Human Resources data and performs exploratory data analysis,
statistical aggregations, and pivot table analysis.

Technologies:
    - Python
    - Pandas
    - Requests
    - XML

Project developed as part of the Hyperskill (JetBrains Academy)
learning platform.
"""

import os
from pathlib import Path

import pandas as pd
import requests


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "outputs"

DATASETS = {
    "A_office_data.xml":
        "https://www.dropbox.com/s/jpeknyzx57c4jb2/A_office_data.xml?dl=1",

    "B_office_data.xml":
        "https://www.dropbox.com/s/hea0tbhir64u9t5/B_office_data.xml?dl=1",

    "hr_data.xml":
        "https://www.dropbox.com/s/u6jzqqg1byajy0s/hr_data.xml?dl=1"
}


def download_datasets():
    """Download datasets if they are not available locally."""

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    for filename, url in DATASETS.items():

        filepath = DATA_DIR / filename

        if not filepath.exists():

            print(f"Downloading {filename}...")

            response = requests.get(
                url,
                allow_redirects=True,
                timeout=60
            )

            response.raise_for_status()

            with open(filepath, "wb") as file:
                file.write(response.content)

            print(f"{filename} downloaded successfully.")


def load_datasets():
    """Load XML datasets into Pandas DataFrames."""

    df_a = pd.read_xml(DATA_DIR / "A_office_data.xml")
    df_b = pd.read_xml(DATA_DIR / "B_office_data.xml")
    df_hr = pd.read_xml(DATA_DIR / "hr_data.xml")

    return df_a, df_b, df_hr


def prepare_indexes(df_a, df_b, df_hr):
    """Create unique employee identifiers for each office."""

    df_a = df_a.copy()
    df_b = df_b.copy()
    df_hr = df_hr.copy()

    df_a.index = (
        "A" + df_a["employee_office_id"].astype(str)
    )

    df_b.index = (
        "B" + df_b["employee_office_id"].astype(str)
    )

    df_hr.set_index(
        "employee_id",
        drop=False,
        inplace=True
    )

    return df_a, df_b, df_hr


def merge_datasets(df_a, df_b, df_hr):
    """Combine office records and merge them with HR information."""

    df_offices = pd.concat([df_a, df_b])

    df = df_offices.merge(
        df_hr,
        how="left",
        left_index=True,
        right_index=True,
        indicator=True
    )

    df = df[df["_merge"] == "both"].copy()

    df.drop(
        columns=[
            "employee_office_id",
            "employee_id",
            "_merge"
        ],
        inplace=True
    )

    df.sort_index(inplace=True)

    return df


def explore_data(df):
    """Display basic information about the merged dataset."""

    print("\n" + "=" * 65)
    print("HR DATA ANALYSIS")
    print("=" * 65)

    print("\nDataset shape:")
    print(df.shape)

    print("\nDataset columns:")
    print(df.columns.tolist())

    print("\nDataset information:")
    df.info()

    print("\nMissing values:")
    print(df.isnull().sum())

    print("\nDuplicate records:")
    print(df.duplicated().sum())

    print("\nDescriptive statistics:")
    print(df.describe())

    print("\nEmployee status distribution:")
    print(df["left"].value_counts())

    print("\nDepartment distribution:")
    print(df["Department"].value_counts())

    print("\nSalary distribution:")
    print(df["salary"].value_counts())


def get_employee_insights(df):
    """Calculate employee workload and performance insights."""

    print("\n" + "=" * 65)
    print("EMPLOYEE INSIGHTS")
    print("=" * 65)

    top_departments = (
        df.sort_values(
            by="average_monthly_hours",
            ascending=False
        )
        .head(10)["Department"]
        .tolist()
    )

    print("\nDepartments of the 10 employees")
    print("with the highest monthly working hours:")
    print(top_departments)

    total_projects = df.loc[
        (df["Department"] == "IT") &
        (df["salary"] == "low"),
        "number_project"
    ].sum()

    print("\nTotal projects worked on by")
    print("low-salary IT employees:")
    print(int(total_projects))

    employees = [
        "A4",
        "B7064",
        "A3033"
    ]

    employee_scores = df.loc[
        employees,
        [
            "last_evaluation",
            "satisfaction_level"
        ]
    ]

    print("\nEmployee evaluation and satisfaction:")
    print(employee_scores)

    return {
        "top_departments": top_departments,
        "total_projects": int(total_projects),
        "employee_scores": employee_scores
    }


def count_bigger_5(series):
    """Count employees who worked on more than five projects."""

    return (series > 5).sum()


def aggregate_employee_data(df):
    """Aggregate employee metrics by employment status."""

    aggregation = df.groupby("left").agg({

        "number_project": [
            "median",
            count_bigger_5
        ],

        "time_spend_company": [
            "mean",
            "median"
        ],

        "Work_accident": [
            "mean"
        ],

        "last_evaluation": [
            "mean",
            "std"
        ]
    })

    aggregation = aggregation.round(2)

    print("\n" + "=" * 65)
    print("EMPLOYEE STATISTICAL AGGREGATION")
    print("=" * 65)

    print("\nEmployee metrics by employment status:")
    print(aggregation)

    return aggregation


def create_department_pivot_table(df):
    """
    Analyze median monthly working hours by department,
    employee status, and salary.
    """

    pivot = df.pivot_table(
        index="Department",
        columns=[
            "left",
            "salary"
        ],
        values="average_monthly_hours",
        aggfunc="median"
    )

    condition1 = (
        pivot[(0, "high")] <
        pivot[(0, "medium")]
    )

    condition2 = (
        pivot[(1, "low")] <
        pivot[(1, "high")]
    )

    pivot = pivot[
        condition1 | condition2
    ]

    pivot = pivot.round(2)

    print("\n" + "=" * 65)
    print("DEPARTMENT WORKLOAD PIVOT TABLE")
    print("=" * 65)

    print("\nMedian working hours by department:")
    print(pivot)

    return pivot


def create_promotion_pivot_table(df):
    """
    Analyze evaluation and satisfaction metrics by
    years at the company and promotion status.
    """

    pivot = df.pivot_table(
        index="time_spend_company",
        columns="promotion_last_5years",
        values=[
            "last_evaluation",
            "satisfaction_level"
        ],
        aggfunc=[
            "min",
            "max",
            "mean"
        ]
    )

    condition = (
        pivot[("mean", "last_evaluation", 0)] >
        pivot[("mean", "last_evaluation", 1)]
    )

    pivot = pivot[condition]

    pivot = pivot.round(2)

    print("\n" + "=" * 65)
    print("EMPLOYEE PROMOTION PIVOT TABLE")
    print("=" * 65)

    print("\nPerformance and satisfaction by promotion status:")
    print(pivot)

    return pivot


def export_results(
    df,
    insights,
    aggregation,
    department_pivot,
    promotion_pivot
):
    """Export processed datasets and analysis results."""

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    df.to_csv(
        OUTPUT_DIR / "merged_hr_data.csv",
        index_label="employee_id"
    )

    aggregation.to_csv(
        OUTPUT_DIR / "employee_aggregation.csv"
    )

    department_pivot.to_csv(
        OUTPUT_DIR / "department_pivot_table.csv"
    )

    promotion_pivot.to_csv(
        OUTPUT_DIR / "promotion_pivot_table.csv"
    )

    insights["employee_scores"].to_csv(
        OUTPUT_DIR / "employee_scores.csv",
        index_label="employee_id"
    )

    print("\n" + "=" * 65)
    print("EXPORT COMPLETED")
    print("=" * 65)

    print("\nAnalysis results saved to:")
    print(OUTPUT_DIR)


def main():

    download_datasets()

    df_a, df_b, df_hr = load_datasets()

    df_a, df_b, df_hr = prepare_indexes(
        df_a,
        df_b,
        df_hr
    )

    df = merge_datasets(
        df_a,
        df_b,
        df_hr
    )

    explore_data(df)

    insights = get_employee_insights(df)

    aggregation = aggregate_employee_data(df)

    department_pivot = create_department_pivot_table(df)

    promotion_pivot = create_promotion_pivot_table(df)

    export_results(
        df,
        insights,
        aggregation,
        department_pivot,
        promotion_pivot
    )

    print("\n" + "=" * 65)
    print("HR DATA ANALYSIS COMPLETED SUCCESSFULLY")
    print("=" * 65)


if __name__ == "__main__":
    main()
