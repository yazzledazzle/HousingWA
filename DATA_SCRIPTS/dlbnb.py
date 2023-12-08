import csv
import os
import requests

def download_links_from_csv(csv_file_path, date_column, type_column, url_column, region_column, save_directory):
    try:
        with open(csv_file_path, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                date_value = row[date_column].strip()
                type_value = row[type_column].strip()
                url = row[url_column].strip()
                region = row[region_column].strip()

                if date_value and type_value and url and region:
                    filetype = url.split('.')[-1]
                    #if filetype has ?, split on ? and take first part
                    if filetype.find('?') != -1:
                        filetype = filetype.split('?')[0]
                    
                    if region == 'Tasmania':
                        filename = f"Tas_{date_value}_{type_value}.{filetype}"
                        save_path = os.path.join(save_directory, 'Tas/Listings', filename)
                    elif region == 'Western Australia':
                        filename = f"{date_value}_{type_value}.{filetype}"
                        save_path = os.path.join(save_directory, 'WA/Listings', filename)
                    else:
                        print(f"Invalid region in row {reader.line_num}")
                        continue

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
csv_file_path = '04-DATA WIP (TO CLEAN)/Airbnb/Links/listings_links.csv'
date_column = 'date'
type_column = 'type'
url_column = 'link'
region_column = 'region'
save_directory = '04-DATA WIP (TO CLEAN)/Airbnb'

# Call the function to download links and save files to the specified directory
download_links_from_csv(csv_file_path, date_column, type_column, url_column, region_column, save_directory)
