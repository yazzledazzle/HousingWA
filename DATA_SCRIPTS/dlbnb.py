import csv
import os
import requests

def download_links_from_csv(csv_file_path, date_column, type_column, url_column):
    try:
        with open(csv_file_path, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                date_value = row[date_column].strip()
                type_value = row[type_column].strip()
                url = row[url_column].strip()

                if date_value and type_value and url:
                    filename = f"{date_value}_{type_value}.csv"
                    download_file(url, filename)
                else:
                    print(f"Missing data in row {reader.line_num}")

    except FileNotFoundError:
        print(f"File not found: {csv_file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

def download_file(url, filename):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            with open(filename, 'wb') as file:
                file.write(response.content)
            print(f"Downloaded: {filename}")
        else:
            print(f"Failed to download {url}. Status code: {response.status_code}")

    except Exception as e:
        print(f"An error occurred while downloading {url}: {e}")

# Specify the path to your CSV file and the column names
csv_file_path = 'wa_links.csv'
date_column = 'date'
type_column = 'type'
url_column = 'link'

# Call the function to download links and create filenames
download_links_from_csv(csv_file_path, date_column, type_column, url_column)
