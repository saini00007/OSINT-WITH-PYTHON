import requests
from datetime import datetime, timedelta
from statistics import mean
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

def convert_timestamp_to_date(timestamp):
    year = int(timestamp[0:4])
    month = int(timestamp[4:6])
    day = int(timestamp[6:8])
    hour = int(timestamp[8:10])
    minute = int(timestamp[10:12])
    second = int(timestamp[12:14])
    return datetime(year, month, day, hour, minute, second)

def count_page_changes(results):
    prev_digest = None
    change_count = 0
    for result in results:
        if result[2] != prev_digest:
            change_count += 1
            prev_digest = result[2]
    return change_count

def get_average_page_size(scans):
    sizes = [int(scan[3]) for scan in scans]
    return round(mean(sizes))

def get_scan_frequency(first_scan, last_scan, total_scans, change_count):
    days_between_scans = (last_scan - first_scan).days / total_scans
    days_between_changes = (last_scan - first_scan).days / change_count
    scans_per_day = (total_scans - 1) / (last_scan - first_scan).days
    changes_per_day = change_count / (last_scan - first_scan).days
    return {
        'Days Between Scans': round(days_between_scans, 2),
        'Days Between Changes': round(days_between_changes, 2),
        'Scans Per Day': round(scans_per_day, 2),
        'Changes Per Day': round(changes_per_day, 2)
    }

def get_wayback_data(url):
    cdx_url = f"https://web.archive.org/cdx/search/cdx?url={url}&output=json&fl=timestamp,statuscode,digest,length,offset"

    try:
        response = requests.get(cdx_url)
        data = response.json()
        
        if not data or not isinstance(data, list) or len(data) <= 1:
            return { 'skipped': 'Site has never before been archived via the Wayback Machine' }

        data.pop(0)

        first_scan = convert_timestamp_to_date(data[0][0])
        last_scan = convert_timestamp_to_date(data[-1][0])
        total_scans = len(data)
        change_count = count_page_changes(data)
        average_page_size = get_average_page_size(data)
        scan_frequency = get_scan_frequency(first_scan, last_scan, total_scans, change_count)

        return {
            'First Scan': first_scan.strftime("%Y-%m-%d %H:%M:%S"),
            'Last Scan': last_scan.strftime("%Y-%m-%d %H:%M:%S"),
            'Total Scans': total_scans,
            'Change Count': change_count,
            'Avg Size': average_page_size,
            'Avg Scans per Day': scan_frequency['Scans Per Day']
        }
    except Exception as e:
        return { 'error': f'Error fetching Wayback data: {str(e)}' }

def print_colored_result(url, result):
    if 'error' in result:
        print("{} {}".format("Error: ", result['error']))
        return

    if 'skipped' in result:
        print("{} {}".format("Skipped: ",result['skipped']))
        return

    print(f"\nWayback Data : ")
    for key, value in result.items():
        if value == False:
            print("  - {:<20} {:^} {:<10}".format(key, ":" + " " * 5, str(value)))
        else:
             print("  - {:<20} {:^} {:<10}".format(key, ":" + " " * 5, str(value)))
                
                
if __name__ == "__main__":
    text = "\nArchive History\n"
    print(text)
    try:
        url = input("Enter URL: ").strip()
        valid_url = check_url(url)
        result = get_wayback_data(valid_url)
        print_colored_result(valid_url, result)
    except Exception as e:
        print("{} {}".format("\nError: ", e))
