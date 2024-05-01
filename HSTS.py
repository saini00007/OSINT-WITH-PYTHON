import requests
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

def check_hsts_compatibility(url):
    try:
        response = requests.head(url)
        headers = response.headers
        hsts_header = headers.get('strict-transport-security')

        if not hsts_header:
            return {'message': 'HSTS not Enabled. \nSite does not serve any HSTS headers.', 'compatible': False, 'hstsHeader': None}
            
        max_age_match = re.search(r'max-age=(\d+)', hsts_header)
        includes_subdomains = 'includeSubDomains' in hsts_header
        preload = 'preload' in hsts_header

        details = {
            'HSTS Enabled': True,
            'max-age': max_age_match.group(1) if max_age_match else 'N/A',
            'includeSubDomains': includes_subdomains,
            'preload': preload
        }

        if max_age_match and int(max_age_match.group(1)) >= 10886400 and includes_subdomains and preload:
            return {'message': 'Site is compatible with the HSTS preload list!', 'compatible': True, 'hstsHeader': hsts_header, 'details': details}
        else:
            return {'message': 'HSTS header does not include all subdomains.', 'compatible': False, 'hstsHeader': hsts_header, 'details': details}
            
    except Exception as e:
        return {'message': f'Error making request: {str(e)}', 'compatible': False, 'hstsHeader': None}

def print_colored_result(result):
    if result['compatible']:
        print("\nCompatible : ", result['message'])
    else:
        print("\nIncompatible : ", result['message'])

    details = result.get('details')
    if details:
        print("\nDetails : ")
        for key, value in details.items():
            print("  - {:<20} {:^} {:<10}".format(key, ":" + " " * 5, str(value)))
                
if __name__ == "__main__":
    text = "\nHSTS Check\n"
    print(text)
    try:   
        url = input("Enter URL: ").strip()
        valid_url = check_url(url)
        result = check_hsts_compatibility(valid_url)
        print_colored_result(result)
    except Exception as e:
        print("{} {}".format("\nError: ", e))
