import os
import requests
from datetime import datetime
import pandas as pd
from tqdm import tqdm
import concurrent.futures
from argparse import ArgumentParser

import warnings
warnings.filterwarnings('ignore')

base_url = 'https://ewapi.cloudapi.pge.com/aggregate-outage-data?level='

def load_cities(file_path):
    processed_cities = []
    try:
        with open(file_path, 'r') as file:
            for city in file:
                # Strip whitespace and replace spaces with %20
                processed_city = city.strip().replace(" ", "%20")
                processed_cities.append(processed_city)
    except FileNotFoundError:
        print(file_path)
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")
    return processed_cities

def get_time():
    current_time = datetime.now()
    formatted_time = current_time.strftime("%m_%d_%Y_%H.%M")
    return formatted_time

def scrape_city(city_name):
    city_url = base_url + city_name
    response = requests.get(city_url)
    if response.status_code == 200:
        data = response.json()[-1]
        df = pd.json_normalize(data, 'value', ['display', 'level']).sort_values('count')
        return df
    else:
        return pd.DataFrame()  # Return an empty DataFrame on failure

def scrape_cities_concurrently(cities, n_cpus=20):
    summarized_df = pd.DataFrame()
    with concurrent.futures.ThreadPoolExecutor(max_workers=n_cpus) as executor:
        # Use executor to map the scrape_city function to all cities
        future_to_city = {executor.submit(scrape_city, city): city for city in cities}
        for future in tqdm(concurrent.futures.as_completed(future_to_city), total=len(cities), desc=f"Scraping with {n_cpus} CPUs"):
            try:
                city_df = future.result()
                summarized_df = pd.concat([summarized_df, city_df], ignore_index=True)
            except Exception as e:
                print(f"An error occurred: {e}")
    return summarized_df

if __name__ == '__main__':
    root_path = '/home/grads/l/lipai.huang/CA_outage/'
    parser = ArgumentParser()
    parser.add_argument('--n-cpus', default=1)
    opt = parser.parse_args()

    ca_cities = load_cities(root_path+'cities_in_california.txt')
    cur_time = get_time()

    # Ensure the output directory exists
    os.makedirs(root_path+'outputs', exist_ok=True)

    summarized_df = scrape_cities_concurrently(ca_cities, int(opt.n_cpus))

    # Save the summarized DataFrame
    output_path = root_path+os.path.join('outputs', f'{cur_time}.csv')
    summarized_df = summarized_df.sort_values('count', ascending=False)
    summarized_df.to_csv(output_path, index=False)
    print(f"Data saved to {output_path}")
