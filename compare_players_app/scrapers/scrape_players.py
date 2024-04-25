import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import time
import random
import pickle
    
def retrieve_players(url):
    # Send a GET request to the URL
    response = requests.get(url)
    
    # Parse the HTML content of the page
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find the div that contains the player names
    content_div = soup.find('div', class_='section_content')
    
    # Find all <a> tags within <p> tags in the div
    a_tags = content_div.find_all('a')
    
    # Extract the text and href from each <a> tag
    player_data = {a.text.strip(): a['href'] for a in a_tags}
    
    return player_data

def get_all_players(url):
    # Send a GET request to the URL
    response = requests.get(url)
    
    # Parse the HTML content of the page
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find the ul with class 'page_index'
    ul = soup.find('ul', class_='page_index')
    
    # Find all <a> tags within <li> tags inside the ul
    links = ul.find_all('a')  # Assuming each li directly contains an a
    
    # Extract the href and text from each <a> tag and store them in a dictionary
    # link_ls = [retrieve_players(url+link['href']) for link in tqdm(links) if link.text.strip()]
    player_urls=[]
    for link in tqdm(links):
        if link.text.strip():
            player_urls.extend(retrieve_players(url+link['href']))
            time.sleep(random.randint(5, 10))
    
    return player_urls

def store_records(records):
    # File path to save the pickled data
    file_path = 'data/raw/players_url.pickle'

    # Open a file in binary write mode
    with open(file_path, 'wb') as file:
        # Pickle the dictionary to the file
        pickle.dump(records, file)
        
def main():
    try:
        # URL of the page to scrape
        url = 'https://fbref.com/en/players/'

        # Call the function and print the results
        player_urls = get_all_players(url)
        store_records(player_urls)
        
    except Exception as e:
        print(e)
        


if __name__=="__main__":
    main()

