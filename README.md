# HR Data Analysis

Human Resources data analysis project developed using Python and Pandas.

This project focuses on integrating multiple employee datasets,
performing exploratory data analysis, generating statistical insights,
and creating pivot tables to support HR decision-making.

The project was developed as part of the Hyperskill (JetBrains Academy)
learning platform.

## Project Overview

The objective of this project is to analyze employee information
from two different company offices and the Human Resources department.

The analysis explores employee performance, workload, salary levels,
promotions, workplace accidents, and employee turnover.

## Technologies Used

- Python
- Pandas
- Requests
- XML
- CSV

## Project Features

### Data Loading and Processing

- Import employee data from XML files.
- Automatically download missing datasets.
- Create unique employee identifiers.
- Standardize DataFrame indexes.
- Inspect dataset structure and missing values.

### Data Integration

- Combine employee records from two offices.
- Merge office information with HR records.
- Identify matching employee records.
- Remove unnecessary columns.
- Sort the consolidated dataset.

### Exploratory Data Analysis

- Examine employee distributions by department.
- Analyze salary categories.
- Investigate employee turnover.
- Calculate descriptive statistics.
- Identify employees with the highest monthly workloads.

### Employee Performance Analysis

- Analyze employee evaluation scores.
- Examine employee satisfaction levels.
- Calculate project workloads.
- Identify low-salary IT employees and their total project count.

### Statistical Aggregation

Compare active employees and employees who left the company using:

- Median number of projects.
- Number of employees working on more than five projects.
- Average and median company tenure.
- Workplace accident rates.
- Mean evaluation scores.
- Standard deviation of evaluation scores.

### Pivot Table Analysis

Generate pivot tables to investigate:

- Median working hours by department, employment status, and salary.
- Employee performance by tenure and promotion status.
- Minimum, maximum, and mean evaluation scores.
- Employee satisfaction across different groups.

## Dataset

The project uses three XML datasets:

- `A_office_data.xml`
- `B_office_data.xml`
- `hr_data.xml`

The datasets contain employee information from two offices
and additional Human Resources records.

Dataset files are downloaded automatically when the program runs.

## Project Structure

```text
hr-data-analysis/
│
├── main.py
├── README.md
├── requirements.txt
├── .gitignore
│
├── data/
│   └── .gitkeep
│
└── outputs/
    └── .gitkeep
```

## Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/hr-data-analysis.git
```

Navigate to the project directory:

```bash
cd hr-data-analysis
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on macOS or Linux:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python main.py
```

The program will download the datasets when necessary, perform
the analyses, display the results, and export CSV files.

## Output Files

After execution, the program generates:

- `merged_hr_data.csv`
- `employee_aggregation.csv`
- `department_pivot_table.csv`
- `promotion_pivot_table.csv`
- `employee_scores.csv`

These files are stored in the `outputs/` directory.

## Skills Demonstrated

- Data Analysis
- Data Cleaning
- Data Integration
- Exploratory Data Analysis
- Data Manipulation
- Statistical Analysis
- Data Aggregation
- Pivot Tables
- Python Programming
- Pandas

## Acknowledgments

Project developed through Hyperskill (JetBrains Academy)
as part of practical training in Python and Data Analysis.
