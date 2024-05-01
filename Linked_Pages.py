import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json
import re

def check_url(url):
    try:
            if not url.startswith('http://') and not url.startswith('https://'):
            url = 'https://' + url
            
            
        
        if re.match(r'^https?://(?:www\.)?[-a-zA-Z0-9@:%._+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_+.~#?&/=]*)$', url):
            
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

def handler(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')

        internal_links_map = {}
        external_links_map = {}

        
        for link in soup.find_all('a', href=True):
            href = link['href']
            absolute_url = urljoin(url, href)
            
                 if absolute_url.startswith(url):
                internal_links_map[absolute_url] = internal_links_map.get(absolute_url, 0) + 1
            elif href.startswith(('http://', 'https://')):
                external_links_map[absolute_url] = external_links_map.get(absolute_url, 0) + 1

            internal_links = sorted(internal_links_map.keys(), key=lambda k: internal_links_map[k], reverse=True)
        external_links = sorted(external_links_map.keys(), key=lambda k: external_links_map[k], reverse=True)

            if not internal_links and not external_links:
            return {
                'statusCode': 400,
                'body': json.dumps({
                    'skipped': 'No internal or external links found. This may be due to the website being dynamically rendered, '
                               'using a client-side framework (like React), and without SSR enabled. '
                               'That would mean that the static HTML returned from the HTTP request doesn\'t contain any meaningful content for analysis. '
                               'You can rectify this by using a headless browser to render the page instead.'
                })
            }

           base_url_len = len(url)
        internal_links = [link[base_url_len:] if link.startswith(url) else link for link in internal_links]

        return {'internal': internal_links, 'external': external_links}

    except Exception as e:
        raise Exception(str(e))

def main():
    text = "\nLinked Pages\n"
    print(text)
    try:
        url = str(input("Enter URL: "))
        valid_url = check_url(url)
        result = handler(valid_url)
        #print(result)
        print("\n{} {}".format("Total internal links found: ", len(result['internal'])))
        print("\nInternal Links: ")
        for link in result['internal']:
            print(link )
    except Exception as e:
        print("{} {}".format("\nError: ", e))

if __name__ == "__main__":
    main()
