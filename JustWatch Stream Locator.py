import requests
from bs4 import BeautifulSoup
import sys

icons = {
    'Netflix': "https://images.justwatch.com/icon/207360008/s100/netflix.jpg",
    'Paramount+': "https://images.justwatch.com/icon/242706661/s100/paramountplus.jpg",
    'HBOMax': "https://images.justwatch.com/icon/285237061/s100/hbomax.jpg",
    'Viaplay': "https://images.justwatch.com/icon/914018/s100/viaplay.jpg",
    'Disney+': "https://images.justwatch.com/icon/147638351/s100/disneyplus.jpg"
}

country_mapping = {
    'AD': 'Andorra', 'AE': 'United Arab Emirates', 'AG': 'Antigua and Barbuda', 
    'AL': 'Albania', 'AO': 'Angola', 'AR': 'Argentina', 'AT': 'Austria', 
    'AU': 'Australia', 'AZ': 'Azerbaijan', 'BA': 'Bosnia and Herzegovina', 
    'BB': 'Barbados', 'BE': 'Belgium', 'BF': 'Burkina Faso', 'BG': 'Bulgaria', 
    'BH': 'Bahrain', 'BM': 'Bermuda', 'BO': 'Bolivia', 'BR': 'Brazil', 
    'BS': 'Bahamas', 'BY': 'Belarus', 'BZ': 'Belize', 'CA': 'Canada', 
    'CD': 'Democratic Republic of the Congo', 'CH': 'Switzerland', 'CI': 'Côte d’Ivoire', 
    'CL': 'Chile', 'CM': 'Cameroon', 'CO': 'Colombia', 'CR': 'Costa Rica', 
    'CU': 'Cuba', 'CV': 'Cape Verde', 'CY': 'Cyprus', 'CZ': 'Czech Republic', 
    'DE': 'Germany', 'DK': 'Denmark', 'DO': 'Dominican Republic', 'DZ': 'Algeria', 
    'EC': 'Ecuador', 'EE': 'Estonia', 'EG': 'Egypt', 'ES': 'Spain', 
    'FI': 'Finland', 'FJ': 'Fiji', 'FR': 'France', 'GB': 'United Kingdom', 
    'GF': 'French Guiana', 'GG': 'Guernsey', 'GH': 'Ghana', 'GI': 'Gibraltar', 
    'GQ': 'Equatorial Guinea', 'GR': 'Greece', 'GT': 'Guatemala', 'GY': 'Guyana', 
    'HK': 'Hong Kong', 'HN': 'Honduras', 'HR': 'Croatia', 'HU': 'Hungary', 
    'ID': 'Indonesia', 'IE': 'Ireland', 'IL': 'Israel', 'IN': 'India', 
    'IQ': 'Iraq', 'IS': 'Iceland', 'IT': 'Italy', 'JM': 'Jamaica', 
    'JO': 'Jordan', 'JP': 'Japan', 'KE': 'Kenya', 'KR': 'South Korea', 
    'KW': 'Kuwait', 'KZ': 'Kazakhstan', 'LB': 'Lebanon', 'LC': 'Saint Lucia', 
    'LI': 'Liechtenstein', 'LK': 'Sri Lanka', 'LT': 'Lithuania', 'LU': 'Luxembourg', 
    'LV': 'Latvia', 'LY': 'Libya', 'MA': 'Morocco', 'MC': 'Monaco', 
    'MD': 'Moldova', 'ME': 'Montenegro', 'MG': 'Madagascar', 'MK': 'North Macedonia', 
    'ML': 'Mali', 'MT': 'Malta', 'MU': 'Mauritius', 'MV': 'Maldives', 
    'MW': 'Malawi', 'MX': 'Mexico', 'MY': 'Malaysia', 'MZ': 'Mozambique', 
    'NE': 'Niger', 'NG': 'Nigeria', 'NI': 'Nicaragua', 'NL': 'Netherlands', 
    'NO': 'Norway', 'NP': 'Nepal', 'NZ': 'New Zealand', 'OM': 'Oman', 
    'PA': 'Panama', 'PE': 'Peru', 'PF': 'French Polynesia', 'PG': 'Papua New Guinea', 
    'PH': 'Philippines', 'PK': 'Pakistan', 'PL': 'Poland', 'PS': 'Palestine', 
    'PT': 'Portugal', 'PY': 'Paraguay', 'QA': 'Qatar', 'RO': 'Romania', 
    'RS': 'Serbia', 'RU': 'Russia', 'SA': 'Saudi Arabia', 'SC': 'Seychelles', 
    'SE': 'Sweden', 'SG': 'Singapore', 'SI': 'Slovenia', 'SK': 'Slovakia', 
    'SM': 'San Marino', 'SN': 'Senegal', 'SV': 'El Salvador', 'TC': 'Turks and Caicos Islands', 
    'TH': 'Thailand', 'TN': 'Tunisia', 'TR': 'Turkey', 'TT': 'Trinidad and Tobago', 
    'TW': 'Taiwan', 'TZ': 'Tanzania', 'UA': 'Ukraine', 'UG': 'Uganda', 
    'US': 'United States', 'UY': 'Uruguay', 'UZ': 'Uzbekistan', 'VA': 'Vatican City', 
    'VE': 'Venezuela', 'VN': 'Vietnam', 'XK': 'Kosovo', 'YE': 'Yemen', 
    'ZA': 'South Africa', 'ZM': 'Zambia', 'ZW': 'Zimbabwe',
}

continent_mapping = {
    'AD': 'Europe', 'AE': 'Asia', 'AG': 'North America', 'AL': 'Europe', 'AO': 'Africa',
    'AR': 'South America', 'AT': 'Europe', 'AU': 'Oceania', 'AZ': 'Asia',
    'BA': 'Europe', 'BB': 'North America', 'BE': 'Europe', 'BF': 'Africa', 'BG': 'Europe',
    'BH': 'Asia', 'BM': 'North America', 'BO': 'South America', 'BR': 'South America',
    'BS': 'North America', 'BY': 'Europe', 'BZ': 'North America', 'CA': 'North America',
    'CD': 'Africa', 'CH': 'Europe', 'CI': 'Africa', 'CL': 'South America', 'CM': 'Africa',
    'CO': 'South America', 'CR': 'North America', 'CU': 'North America', 'CV': 'Africa',
    'CY': 'Asia', 'CZ': 'Europe', 'DE': 'Europe', 'DK': 'Europe', 'DO': 'North America',
    'DZ': 'Africa', 'EC': 'South America', 'EE': 'Europe', 'EG': 'Africa', 'ES': 'Europe',
    'FI': 'Europe', 'FJ': 'Oceania', 'FR': 'Europe', 'GB': 'Europe', 'GF': 'South America',
    'GG': 'Europe', 'GH': 'Africa', 'GI': 'Europe', 'GQ': 'Africa', 'GR': 'Europe',
    'GT': 'North America', 'GY': 'South America', 'HK': 'Asia', 'HN': 'North America',
    'HR': 'Europe', 'HU': 'Europe', 'ID': 'Asia', 'IE': 'Europe', 'IL': 'Asia',
    'IN': 'Asia', 'IQ': 'Asia', 'IS': 'Europe', 'IT': 'Europe', 'JM': 'North America',
    'JO': 'Asia', 'JP': 'Asia', 'KE': 'Africa', 'KR': 'Asia', 'KW': 'Asia',
    'KZ': 'Asia', 'LB': 'Asia', 'LC': 'North America', 'LI': 'Europe', 'LK': 'Asia',
    'LT': 'Europe', 'LU': 'Europe', 'LV': 'Europe', 'LY': 'Africa', 'MA': 'Africa',
    'MC': 'Europe', 'MD': 'Europe', 'ME': 'Europe', 'MG': 'Africa', 'MK': 'Europe',
    'ML': 'Africa', 'MT': 'Europe', 'MU': 'Africa', 'MV': 'Asia', 'MW': 'Africa',
    'MX': 'North America', 'MY': 'Asia', 'MZ': 'Africa', 'NE': 'Africa', 'NG': 'Africa',
    'NI': 'North America', 'NL': 'Europe', 'NO': 'Europe', 'NP': 'Asia', 'NZ': 'Oceania',
    'OM': 'Asia', 'PA': 'North America', 'PE': 'South America', 'PF': 'Oceania',
    'PG': 'Oceania', 'PH': 'Asia', 'PK': 'Asia', 'PL': 'Europe', 'PS': 'Asia',
    'PT': 'Europe', 'PY': 'South America', 'QA': 'Asia', 'RO': 'Europe', 'RS': 'Europe',
    'RU': 'Europe', 'SA': 'Asia', 'SC': 'Africa', 'SE': 'Europe', 'SG': 'Asia',
    'SI': 'Europe', 'SK': 'Europe', 'SM': 'Europe', 'SN': 'Africa', 'SV': 'North America',
    'TC': 'North America', 'TH': 'Asia', 'TN': 'Africa', 'TR': 'Asia', 'TT': 'North America',
    'TW': 'Asia', 'TZ': 'Africa', 'UA': 'Europe', 'UG': 'Africa', 'US': 'North America',
    'UY': 'South America', 'UZ': 'Asia', 'VA': 'Europe', 'VE': 'South America',
    'VN': 'Asia', 'XK': 'Europe', 'YE': 'Asia', 'ZA': 'Africa', 'ZM': 'Africa', 'ZW': 'Africa'
}

continent_order = ['Europe', 'North America', 'Asia', 'Africa', 'South America', 'Oceania']

def find_streaming_services_icons(soup, icons):
    found_icons = []
    stream_offers = soup.find_all('div', class_='buybox-row stream')

    for stream_offer in stream_offers:
        offers = stream_offer.find_all('a', class_='offer')
        for offer in offers:
            img = offer.find('img')
            if img and img.get('src') in icons.values():
                for service, icon_url in icons.items():
                    if img.get('src') == icon_url:
                        found_icons.append(service)
                        break

    return found_icons

def extract_title_and_year(soup):
    title_block = soup.find('div', class_='title-block')
    if title_block:
        title = title_block.find('h1')
        title_text = title.get_text().strip() if title else "Unknown Title"

        year_span = title_block.find('span', class_='text-muted')
        year_text = year_span.get_text().strip() if year_span else "Unknown Year"

        formatted_output = f"{title_text} {year_text}"
        return formatted_output

    print("You have entered the main website URL. Please provide a specific movie or content URL")
    sys.exit()

initial_url = input("URL: ")

if not initial_url.startswith("https://www.justwatch.com"):
    if initial_url.startswith("http://"):
        initial_url = "https://" + initial_url[len("http://"):]
    elif initial_url.startswith("www.justwatch.com"):
        initial_url = "https://" + initial_url
    elif initial_url.startswith("justwatch.com"):
        initial_url = "https://www." + initial_url
    else:
        print("This script is designed to work with JustWatch URLs only. Please provide a valid JustWatch URL")
        sys.exit()

initial_response = requests.get(initial_url)

if initial_response.status_code == 200:
    initial_soup = BeautifulSoup(initial_response.content, 'html.parser')
    title = extract_title_and_year(initial_soup)
    alternate_links = initial_soup.find_all('link', rel='alternate')

    print("Title:", title)

    service_continents = {service: {} for service in icons}

    for index, link in enumerate(alternate_links, start=1):
        if 'hreflang' in link.attrs and 'href' in link.attrs:
            hreflang = link['hreflang'].split('-')[-1]
            country_name = country_mapping.get(hreflang, 'Unknown')
            continent = continent_mapping.get(hreflang, 'Unknown')

            country_url = link['href']
            country_response = requests.get(country_url)
            if country_response.status_code == 200:
                country_soup = BeautifulSoup(country_response.content, 'html.parser')
                found_services = find_streaming_services_icons(country_soup, icons)
                for service in found_services:
                    if continent not in service_continents[service]:
                        service_continents[service][continent] = []
                    if country_name not in service_continents[service][continent]:
                        service_continents[service][continent].append(country_name)

        print(f"Progress: {index / len(alternate_links) * 100:.2f}%", end='\r')

    print("\n")

    any_service_found = False
    for service, continents in service_continents.items():
        if continents:
            print(f"{service}:\n")

            first_continent = True
            for ordered_continent in continent_order:
                if ordered_continent in continents:
                    if not first_continent:
                        print()
                    else:
                        first_continent = False

                    print(f"- {ordered_continent}:")
                    for country in sorted(continents[ordered_continent]):
                        print(f"  - {country}")
                        any_service_found = True

            print()
        
    if not any_service_found:
        print("None\n")

else:
    print(f"Failed to retrieve initial page, status code: {initial_response.status_code}")