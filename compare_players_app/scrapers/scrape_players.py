import sys
sys.path.append("../")

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import time
import random
import pickle
import utils.config as c
    
def retrieve_players(url):
    # Send a GET request to the URL
    response = requests.get(url)
    
    # Parse the HTML content of the page
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find the div that contains the player names
    content_div = soup.find('div', class_=c.PLAYERS_DIR_DIV_CLASS)
    
    # Find all <a> tags within <p> tags in the div
    a_tags = content_div.find_all('a')
    
    # Extract the text and href from each <a> tag
    player_data = {a.text.strip(): a['href'] for a in a_tags}
    
    return player_data

def get_all_players(url):
    # Send a GET request to the URL
    print(url)
    response = requests.get(url)
    
    # Parse the HTML content of the page
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find the ul with class 'page_index'
    ul = soup.find('ul', class_=c.PLAYERS_DIR_UL_CLASS)
    
    # Find all <a> tags within <li> tags inside the ul
    links = ul.find_all('a')  # Assuming each li directly contains an a
    
    # Extract the href and text from each <a> tag and store them in a dictionary
    player_urls={}
    for link in tqdm(links):
        link_strip = link.text.strip()
        if link_strip:
            players_url = url[:-1] + "/" + link['href'].split("/")[-2] + "/"
            players = retrieve_players(players_url)
            tqdm.write(f"{players_url} | {str(len(players))}")
            player_urls.update(players)
            
            time.sleep(random.randint(5, 10))
    
    return player_urls

def store_records(records):
    # File path to save the pickled data
    file_path = c.PLAYERS_DIR_STORE_PATH

    # Open a file in binary write mode
    with open(file_path, 'wb') as file:
        # Pickle the dictionary to the file
        pickle.dump(records, file)
        
def main():
    try:

        # Call the function and print the results
        
        
        player_urls = get_all_players(c.PLAYERS_DIR_URL)
        store_records(player_urls)
        
    except Exception as e:
        print(e)
        


if __name__=="__main__":
    main()

