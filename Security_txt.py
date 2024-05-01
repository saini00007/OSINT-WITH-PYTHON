import requests
from urllib.parse import urlparse, urljoin
import re

SECURITY_TXT_PATHS = [
    '/security.txt',
    '/.well-known/security.txt',
]

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
       

def parse_result(result):
    output = {}
    counts = {}
    lines = result.split('\n')
    for line in lines:
        if not line.startswith("#") and not line.startswith("-----") and line.strip() != '':
            key_value = line.split(':', 1)
            if len(key_value) == 2:
                key = key_value[0].strip()
                value = key_value[1].strip()
                if key in output:
                    counts[key] = counts.get(key, 0) + 1
                    key += str(counts[key])
                output[key] = value
    return output

def is_pgp_signed(result):
    return '-----BEGIN PGP SIGNED MESSAGE-----' in result

def handler(url_param):
    try:
        url = urlparse(url_param) if '://' in url_param else urlparse('https://' + url_param)
    except Exception as e:
        raise ValueError('Invalid URL or URL is not responding to this query.')

    base_url = url._replace(path='').geturl()

    for path in SECURITY_TXT_PATHS:
        try:
            result = fetch_security_txt(base_url, path)
            if result and '<html' in result:
                return {'isPresent': False}
            if result:
                return {
                    'isPresent': True,
                    'foundIn': path,
                    'content': result,
                    'isPgpSigned': is_pgp_signed(result),
                    'fields': parse_result(result),
                }
        except Exception as e:
            raise Exception(str(e))

    return {'isPresent': False}

def fetch_security_txt(base_url, path):
    url = urljoin(base_url, path)
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    return None

if __name__ == "__main__":
    text = "\nSecurity.txt\n"
    print(text)
    try:
        url = input("Enter URL: ")
        valid_url = check_url(url)
        result = handler(valid_url)
        if result['isPresent']:
            print("\n{:<20} {:^} {:<10}".format("Security.txt", "-->" + " " * 5, "present"))
            
            print("{:<20} {:^} {:<10}".format("File Location", ":" + " " * 5, result['foundIn']))
            
            print("{:<20} {:^} {:<10}".format("PGP Signed", ":" + " " * 5, "Yes" if result['isPgpSigned'] else "No"))
            
            #print("Content:")
            for key, value in result['fields'].items():
                print("{:<20} {:^} {:<10}".format(key, ":" + " " * 5, value))
        else:
            print("\n{:<20} {:^} ".format("Security.txt", "-->" + " " * 5 + "not present")) 
    except Exception as e:
        print("{} {}".format("\nError: ", e))
