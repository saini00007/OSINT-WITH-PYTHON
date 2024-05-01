import socket
import requests
from requests.exceptions import ConnectionError
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

def resolve_dns(url):
    try:
        
        domain = url.replace('https://', '').replace('http://', '')
        
        addresses = socket.gethostbyname_ex(domain)[-1]
        
        results = []
        for address in addresses:
            
            try:
                hostname = socket.gethostbyaddr(address)[0]
            except socket.herror:
                hostname = None
            
                try:
                response = requests.get(f'https://{address}/dns-query')
                doh_direct_supports = response.status_code == 200
            except ConnectionError:
                doh_direct_supports = False
            
            results.append({
                'address': address,
                'hostname': hostname,
                'dohDirectSupports': doh_direct_supports
            })

        return {
            'domain': domain,
            'dns': results
        }
    except Exception as e:
        raise Exception(f"An error occurred while resolving DNS. {str(e)}")
        
def print_result(result):

    try:
        n = 1
        for item in result["dns"]:
            print(f"DNS Server #{n}")

            if "address" in item:
                print("{:<20} {:^} {:>10}".format("IP Address", ":" + " " * 5, str(item["address"])))
            if "hostname" in item:
                print("{:<20} {:^} {:>10}".format("Hostname", ":" + " " * 5, str(item["hostname"])))
            if "dohDirectSupports" in item:
                print("{:<20} {:^} {:>10}".format("DoH Support", ":" + " " * 5, str(item["dohDirectSupports"])))

            print("\n")
            n = n + 1

    except Exception as e:
        raise Exception(f"An error occurred while printing result: {str(e)}")

if __name__ == "__main__":
    text = "\nDNS Server\n"
    print(text) 
    try:
        url = input("Enter URL: ").strip()
        print("\n")
        valid_url = check_url(url)
        resolved_dns = resolve_dns(valid_url)        
        print_result(resolved_dns)
    except Exception as e:
        print("{} {}".format("\nError: ", e))
