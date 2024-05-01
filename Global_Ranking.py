import os
import requests
from urllib.parse import urlparse
from tabulate import tabulate
import re

def check_url(url):
    try:
            if not url.startswith('http://') and not url.startswith('https://'):
            url = 'https://' + url
            
            
            if re.match(r'^https?://(?:www\.)?[-a-zA-Z0-9@:%._+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_+.~#?&/=]*)$', url):
            #return url
            pass
        else:
            raise ValueError("Invalid URL format. Please enter a valid URL.")

        response = requests.get(url)
        if response.status_code == 200:
            return url
        else:
            raise ConnectionError(f"The URL '{url}' is not responding or invalid url. Status code: {response.status_code}")

    except requests.exceptions.RequestException as e:
        raise Exception(f"The URL '{url}' is invalid or not responding.")

def fetch_rank(url):
    domain = urlparse(url).hostname
    if not domain:
        raise ValueError('Invalid URL')

    try:
        auth = (
            os.environ.get('TRANCO_USERNAME'),
            os.environ.get('TRANCO_API_KEY')
        ) if os.environ.get('TRANCO_API_KEY') else {}

        response = requests.get(
            f'https://tranco-list.eu/api/ranks/domain/{domain}',
            timeout=5,
            auth=auth
        )

        if not response.ok or 'ranks' not in response.json():
            return {'skipped': f"Skipping, as {domain} isn't ranked in the top 100 million sites yet."}

        ranks = response.json().get('ranks', [])
        global_ranking = ranks[0].get('rank', 'N/A')
        change_since_yesterday = ranks[0].get('delta', 'N/A')
        historical_avg_rank = sum(rank.get('rank', 0) for rank in ranks) / len(ranks) if ranks else 'N/A'

        return {
            'global_ranking': global_ranking,
            'change_since_yesterday': change_since_yesterday,
            'historical_avg_rank': historical_avg_rank,
            'ranks': ranks
        }

    except Exception as e:
        return {'error': f'Unable to fetch rank, {str(e)}'}

def print_result(result):
    if 'error' in result:
        print(Fore.RED + "Error:", result['error'])
        return

    if 'skipped' in result:
        print(Fore.YELLOW + "Skipped:", result['skipped'])
        return

       headers = ['Rank', 'Change Since Yesterday']
    rows = [[rank.get('rank', 'N/A'), rank.get('delta', 'N/A')] for rank in result['ranks']]
    
    print("  - {:<30} {:^} {:<10}".format("Global Ranking", ":" + " " * 5, result['global_ranking']))
   
    
    print("  - {:<30} {:^} {:<10}".format("Historical Average Rank", ":" + " " * 5, result['historical_avg_rank']))


if __name__ == "__main__":
    text = "\nGlobal Ranking\n"
    print(text)
    try:
        url = input("Enter URL: ").strip()
        valid_url = check_url(url)
        result = fetch_rank(valid_url)
        print_result(result)
    except Exception as e:
        print("{} {}".format("\nError: ", e))
