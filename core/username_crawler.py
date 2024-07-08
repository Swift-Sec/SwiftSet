import requests
from bs4 import BeautifulSoup
from colorama import Fore, Style

def check_username_availability(username, urls):
    results = []
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

    for url in urls:
        try:
            response = requests.get(url.format(username), headers=headers)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                if any(keyword in soup.text.lower() for keyword in error_list):
                    results.append((url.format(username), False))
                else:
                    if "https://www.pinterest.com/" in url:
                        results.append((url.format(username), 433))
                    elif "https://www.facebook.com/" in url:
                        if "this content isn't available at the moment" in soup.text.lower():
                            results.append((url.format(username), 433))
                        
                    else:
                        results.append((url.format(username), True))
            else:
                results.append((url.format(username), False))
        except Exception as e:
            results.append((url.format(username), False))
    return results

urls = [
    "https://twitter.com/{}",
    "https://www.instagram.com/{}",
    "https://www.facebook.com/{}",
    "https://www.reddit.com/user/{}",
    "https://www.pinterest.com/{}",
    "https://www.tiktok.com/@{}",
    "https://www.tumblr.com/search?scope=all_of_tumblr&q={}",
    "https://github.com/{}",
    "https://www.linkedin.com/in/{}",
    "https://www.flickr.com/people/{}",
    "https://soundcloud.com/{}",
    "https://medium.com/@{}",
    "https://www.twitch.tv/{}",
    "https://vimeo.com/{}",
    "https://www.behance.net/{}",
    "https://dribbble.com/{}",
    "https://{}.deviantart.com",
    "https://www.goodreads.com/search?q={}&search%5Bsource%5D=goodreads&search_type=people&tab=people",
    "https://about.me/{}",
    "https://500px.com/{}",
    "https://www.blogger.com/profile/{}",
    "https://{}.wordpress.com",
    "https://www.last.fm/user/{}",
    "https://myspace.com/{}",
    "https://www.slideshare.net/{}",
    "https://angel.co/{}",
    "https://www.mixcloud.com/{}",
    "https://www.kaggle.com/{}",
    "https://www.producthunt.com/@{}",
    "https://www.yelp.com/user_details?userid={}"
]

error_list = [
    "user not found",
    "page not found",
    "page is gone",
    "page is no longer",
    "does not exist",
    "doesn't exist",
    "couldn't find",
    "could not find",
    "can't find",
    "we seem to have lost this page",
    "there's nothing here.",
    "isn't available",
    "is not available",
    "is still available. why not register it?",
    "it appears the profile you seek doesn’t exist.",
    "llama not found",
    "there is no one by the name",
    "nobody with the name",
    "check the name",
    "profile not available",
    "something went wrong",
    "if searching other variants of their name (eg bill for william, etc) doesn't work, try using the friend finder",
]
username = "HazeSec"

def crawl(username):
    results = check_username_availability(username, urls)

    for url, found in results:
        if found == True:
            print(f"{Fore.GREEN}[{url}] User found!{Style.RESET_ALL}")
        elif found == False:
            print(f"{Fore.RED}[{url}] User not found!{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}[{url}] User might be found!{Style.RESET_ALL}")