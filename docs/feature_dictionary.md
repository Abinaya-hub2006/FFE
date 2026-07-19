# Candidate Feature Dictionary

## Stage 11.1 - Fundraising Features

| Feature | Description | Formula |
|---------|-------------|---------|
| total_amount | Total amount raised by the candidate | SUM(contribution_receipt_amount) |
| donation_count | Number of receipt records | COUNT(*) |
| avg_donation | Mean contribution amount | AVG(amount) |
| median_donation | Median contribution amount | MEDIAN(amount) |
| min_donation | Smallest contribution | MIN(amount) |
| max_donation | Largest contribution | MAX(amount) |
| std_donation | Standard deviation of contributions | STDDEV(amount) |

---

## Stage 11.2 - Individual Donor Features

| Feature | Description | Formula |
|---------|-------------|---------|
| unique_individual_donors | Number of unique individual donors | COUNT(DISTINCT donor_key) |
| repeat_individual_donors | Donors contributing more than once | COUNT(donation_count > 1) |
| total_individual_donations | Total donations from individuals | SUM(donation_count) |
| total_individual_amount | Total money from individuals | SUM(total_amount) |
| avg_amount_per_donor | Average amount per donor | total_amount / unique_donors |
| max_donations_single_donor | Maximum donations by one donor | MAX(donation_count) |
| largest_single_donor | Largest cumulative donor contribution | MAX(total_amount) |

## Stage 11.3 - Time Features

| Feature | Description | Formula |
|---------|-------------|---------|
| first_donation | Earliest contribution within the 2021–2022 campaign window | MIN(date) |
| last_donation | Latest contribution within the 2021–2022 campaign window | MAX(date) |
| campaign_duration_days | Duration between first and last contribution | DATEDIFF(day) |
| active_months | Number of unique fundraising months | COUNT(DISTINCT month) |
| first30_amount | Amount raised in the first 30 days of campaign activity | SUM(amount) |
| last30_amount | Amount raised in the last 30 days of campaign activity | SUM(amount) |
| first30_ratio | first30_amount ÷ total_amount | Derived |
| last30_ratio | last30_amount ÷ total_amount | Derived |

| Feature           | Description                                          |
| ----------------- | ---------------------------------------------------- |
| donation_q1       | 25th percentile contribution amount                  |
| donation_median   | Median contribution amount                           |
| donation_q3       | 75th percentile contribution amount                  |
| donation_iqr      | Interquartile range (Q3 − Q1)                        |
| donation_std      | Standard deviation of contribution amounts           |
| donation_variance | Variance of contribution amounts                     |
| donation_cv       | Coefficient of variation (standard deviation ÷ mean) |
