from bs4 import BeautifulSoup
import logging
from urllib.parse import urljoin, urlparse
import time

import hrequests as requests  

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

visited_urls = set()

def make_request(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 OPR/109.0.0.0'
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            logging.error(f"Request failed with status code {response.status_code}")
            return None
        return response
    except Exception as e:
        logging.error(f"Request failed: {e}")
        return None
                                                                                        
def parse_html(html, base_url):
    soup = BeautifulSoup(html, 'html.parser')
    links = set()
    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        if '#' in href:
            continue  # Skip links with fragment identifiers
        full_url = urljoin(base_url, href)
        parsed_url = urlparse(full_url)
        if parsed_url.netloc == urlparse(base_url).netloc and full_url not in visited_urls:
            links.add(full_url)
    return links
                                        
def crawl(url, max_depth, current_depth=1):
    global visited_urls
                                            
    if current_depth > max_depth or url in visited_urls:
        return
                                                        
    visited_urls.add(url)
    response = make_request(url)
    if not response:
        return
                                                    
    html_content = response.text
    links = parse_html(html_content, url)
    found_urls = list(links)
                                                        
    for link in found_urls:
        print(f"[DEPTH: {current_depth}] {link}")
        time.sleep(1)
                                                
    for link in links:
        crawl(link, max_depth, current_depth=current_depth + 1)
