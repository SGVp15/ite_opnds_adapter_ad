import csv

from config import CSV_HEADERS, DELIMITER_CSV


def save_users_csv(users_data, csv_filename: str = 'ldap_users.csv'):
    with open(csv_filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=CSV_HEADERS, delimiter=DELIMITER_CSV)
        writer.writeheader()
        for user in users_data:
            row = {header: user.get(header, '') for header in CSV_HEADERS}
            writer.writerow(row)
