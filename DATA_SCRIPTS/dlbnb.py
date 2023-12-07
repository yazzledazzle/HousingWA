import csv
import os
import requests

def download_links_from_csv(csv_file_path, date_column, type_column, url_column, save_directory):
    try:
        with open(csv_file_path, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                date_value = row[date_column].strip()
                type_value = row[type_column].strip()
                url = row[url_column].strip()

                if date_value and type_value and url:
                    filename = f"{date_value}_{type_value}"
                    save_path = os.path.join(save_directory, filename)
                    download_file(url, save_path)
                else:
                    print(f"Missing data in row {reader.line_num}")

    except FileNotFoundError:
        print(f"File not found: {csv_file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

def download_file(url, save_path):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            with open(save_path, 'wb') as file:
                file.write(response.content)
            print(f"Downloaded: {save_path}")
        else:
            print(f"Failed to download {url}. Status code: {response.status_code}")

    except Exception as e:
        print(f"An error occurred while downloading {url}: {e}")

# Specify the path to your CSV file, column names, and save directory
csv_file_path = '04-DATA WIP (TO CLEAN)/Airbnb/Links/batch_links.csv'
date_column = 'date'
type_column = 'type'
url_column = 'link'
save_directory = '04-DATA WIP (TO CLEAN)/Airbnb/Tas summary files'

# Call the function to download links and save files to the specified directory
download_links_from_csv(csv_file_path, date_column, type_column, url_column, save_directory)
