import requests
from bs4 import BeautifulSoup
import sys
import os
import ctypes
import threading
import stat
import re

all_icons = {
    'Netflix': "https://images.justwatch.com/icon/207360008/s100/netflix.jpg",
    'Paramount+': "https://images.justwatch.com/icon/242706661/s100/paramountplus.jpg",
    'HBOMax': "https://images.justwatch.com/icon/285237061/s100/hbomax.jpg",
    'Max': "https://images.justwatch.com/icon/305458112/s100/max.jpg",
    'Disney+': "https://images.justwatch.com/icon/147638351/s100/disneyplus.jpg",
    'Peacock': "https://images.justwatch.com/icon/194173871/s100/peacocktvpremium.jpg",
    'Hulu': "https://images.justwatch.com/icon/116305230/s100/hulu.jpg",
    'Shudder': "https://images.justwatch.com/icon/2562359/s100/shudder.jpg",
    'Viaplay': "https://images.justwatch.com/icon/914018/s100/viaplay.jpg",
    'Prime Video': "https://images.justwatch.com/icon/52449539/s100/amazonprime.jpg",
    'AppleTV+': "https://images.justwatch.com/icon/152862153/s100/appletvplus.jpg",
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
    'KW': 'Kuwait', 'LB': 'Lebanon', 'LC': 'Saint Lucia', 
    'LI': 'Liechtenstein', 'LT': 'Lithuania', 'LU': 'Luxembourg', 
    'LV': 'Latvia', 'LY': 'Libya', 'MA': 'Morocco', 'MC': 'Monaco', 
    'MD': 'Moldova', 'ME': 'Montenegro', 'MG': 'Madagascar', 'MK': 'North Macedonia', 
    'ML': 'Mali', 'MT': 'Malta', 'MU': 'Mauritius', 
    'MW': 'Malawi', 'MX': 'Mexico', 'MY': 'Malaysia', 'MZ': 'Mozambique', 
    'NE': 'Niger', 'NG': 'Nigeria', 'NI': 'Nicaragua', 'NL': 'Netherlands', 
    'NO': 'Norway', 'NZ': 'New Zealand', 'OM': 'Oman', 
    'PA': 'Panama', 'PE': 'Peru', 'PF': 'French Polynesia', 'PG': 'Papua New Guinea', 
    'PH': 'Philippines', 'PK': 'Pakistan', 'PL': 'Poland', 'PS': 'Palestine', 
    'PT': 'Portugal', 'PY': 'Paraguay', 'QA': 'Qatar', 'RO': 'Romania', 
    'RS': 'Serbia', 'RU': 'Russia', 'SA': 'Saudi Arabia', 'SC': 'Seychelles', 
    'SE': 'Sweden', 'SG': 'Singapore', 'SI': 'Slovenia', 'SK': 'Slovakia', 
    'SM': 'San Marino', 'SN': 'Senegal', 'SV': 'El Salvador', 'TC': 'Turks and Caicos Islands', 
    'TH': 'Thailand', 'TN': 'Tunisia', 'TR': 'Turkey', 'TT': 'Trinidad and Tobago', 
    'TW': 'Taiwan', 'TZ': 'Tanzania', 'UA': 'Ukraine', 'UG': 'Uganda', 
    'US': 'United States', 'UY': 'Uruguay', 'VA': 'Vatican City', 
    'VE': 'Venezuela', 'XK': 'Kosovo', 'YE': 'Yemen', 
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
    'LB': 'Asia', 'LC': 'North America', 'LI': 'Europe',
    'LT': 'Europe', 'LU': 'Europe', 'LV': 'Europe', 'LY': 'Africa', 'MA': 'Africa',
    'MC': 'Europe', 'MD': 'Europe', 'ME': 'Europe', 'MG': 'Africa', 'MK': 'Europe',
    'ML': 'Africa', 'MT': 'Europe', 'MU': 'Africa', 'MW': 'Africa',
    'MX': 'North America', 'MY': 'Asia', 'MZ': 'Africa', 'NE': 'Africa', 'NG': 'Africa',
    'NI': 'North America', 'NL': 'Europe', 'NO': 'Europe', 'NZ': 'Oceania',
    'OM': 'Asia', 'PA': 'North America', 'PE': 'South America', 'PF': 'Oceania',
    'PG': 'Oceania', 'PH': 'Asia', 'PK': 'Asia', 'PL': 'Europe', 'PS': 'Asia',
    'PT': 'Europe', 'PY': 'South America', 'QA': 'Asia', 'RO': 'Europe', 'RS': 'Europe',
    'RU': 'Europe', 'SA': 'Asia', 'SC': 'Africa', 'SE': 'Europe', 'SG': 'Asia',
    'SI': 'Europe', 'SK': 'Europe', 'SM': 'Europe', 'SN': 'Africa', 'SV': 'North America',
    'TC': 'North America', 'TH': 'Asia', 'TN': 'Africa', 'TR': 'Asia', 'TT': 'North America',
    'TW': 'Asia', 'TZ': 'Africa', 'UA': 'Europe', 'UG': 'Africa', 'US': 'North America',
    'UY': 'South America', 'VA': 'Europe', 'VE': 'South America',
    'XK': 'Europe', 'YE': 'Asia', 'ZA': 'Africa', 'ZM': 'Africa', 'ZW': 'Africa'
}

search_mapping = {
    'ad': 'cerca', 'al': 'busca', 'ao': 'busca',
    'ar': 'buscar', 'at': 'suche', 'az': 'axtarış',
    'be': 'recherche', 'bf': 'recherche', 'bo': 'buscar',
    'br': 'busca', 'by': 'пошук', 'cd': 'recherche',
    'ch': 'Suche', 'ci': 'recherche', 'cl': 'buscar',
    'co': 'buscar', 'cr': 'buscar', 'cu': 'buscar',
    'cv': 'busca', 'cz': 'vyhledání', 'de': 'Suche',
    'do': 'buscar', 'ec': 'buscar', 'es': 'buscar',
    'fr': 'recherche', 'gf': 'recherche', 'gq': 'buscar',
    'gt': 'buscar', 'hn': 'buscar', 'hr': 'pretraživanje',
    'is': 'leita', 'li': 'Suche', 'lu': 'recherche',
    'mc': 'recherche', 'me': 'pretraga', 'mg': 'recherche',
    'mk': 'пребарување', 'ml': 'recherche', 'mt': 'fittex',
    'mu': 'recherche', 'mx': 'buscar', 'mz': 'busca',
    'ne': 'recherche', 'ni': 'buscar', 'pa': 'buscar',
    'pe': 'buscar', 'pf': 'recherche', 'pt': 'busca',
    'py': 'buscar', 'rs': 'pretraga', 'sc': 'recherche',
    'si': 'iskanje', 'sk': 'vyhľadávať', 'sm': 'cerca',
    'sn': 'recherche', 'sv': 'buscar', 'tr': 'arama',
    'tz': 'tafuta', 'ua': 'пошук', 'uy': 'buscar',
    'va': 'cerca', 've': 'buscar', 'xk': 'kërko',
}

continent_order = ['Europe', 'North America', 'Asia', 'Africa', 'South America', 'Oceania']

try:
    appdata = os.environ.get("APPDATA")
except:
    appdata = "C:\\ProgramData"

data_folder = os.path.join(appdata, "Galaxy", "JustWatch Stream Locator")

settings = os.path.join(data_folder, "settings.txt")

engine = os.path.join(data_folder, "engine.txt")

leaving_soon_status = {}

def find_streaming_services_icons(soup, filtered_icons):
    found_icons = {}
    stream_offers = soup.find_all('div', class_='buybox-row stream')

    for stream_offer in stream_offers:
        offers = stream_offer.find_all('a', class_='offer')
        for offer in offers:
            img = offer.find('img')
            leaving_icon = offer.find('span', class_='offer__label--leaving-icon') is not None
            if img and img.get('src') in filtered_icons.values():
                for service, icon_url in filtered_icons.items():
                    if img.get('src') == icon_url:
                        if service not in found_icons:
                            found_icons[service] = []
                        found_icons[service].append(leaving_icon)
                        break

    return found_icons

def clear_input():
    if os.name == 'nt':
        _ = os.system('cls')

def extract_title_and_year(soup):
    title_block = soup.find('div', class_='title-block')
    if title_block:
        title = title_block.find('h1')
        title_text = title.get_text().strip() if title else "Unknown Title"

        formatted_output = title_text.replace("  ", " ")
        return formatted_output

    clear_input()
    print("You have entered the main website URL. Please provide a specific movie or content URL")
    sys.exit()

def main():
    initial_url = input("Input: ")

    def is_url(string):
        return string.startswith("http://") or string.startswith("https://") or string.startswith("www.") or ".com" in string

    def process_url(initial_url):
        if initial_url.startswith("https://www.justwatch.com"):
            return initial_url
        elif initial_url.startswith("http://"):
            return "https://" + initial_url[len("http://"):]
        elif initial_url.startswith("www.justwatch.com"):
            return "https://" + initial_url
        elif initial_url.startswith("justwatch.com"):
            return "https://www." + initial_url
        else:
            clear_input()
            print("Please provide a valid JustWatch URL or a movie name")
            sys.exit()

    if initial_url.lower() in ["engine", "e"]:

        short_country_mapping = {code: name.lower().replace(" ", "") for code, name in country_mapping.items()}

        if 'GB' in short_country_mapping:
            short_country_mapping['UK'] = short_country_mapping.pop('GB')

        edited_country_mapping = {code: name for code, name in country_mapping.items()}

        if 'GB' in edited_country_mapping:
            edited_country_mapping['UK'] = edited_country_mapping.pop('GB')

        def set_engine():
            with open(engine, 'r') as file:
                contents = file.read()

            clear_input()
    
            country_code = None

            if contents.upper() in edited_country_mapping:
                country_name = edited_country_mapping[contents.upper()]
                print(f"{country_name} ({contents.upper()})\n")
            else:
                country_code = None
                for code, name in edited_country_mapping.items():
                    if name.lower() == contents.lower():
                        country_code = code
                        break

            edit_engine = input("Edit: ").lower().replace(" ", "")

            if edit_engine.upper() in short_country_mapping:
                country_code = edit_engine.upper()
            else:
                for code, name in short_country_mapping.items():
                    if name.lower() == edit_engine.lower():
                        country_code = code
                        break

            if country_code:
                with open(engine, 'w') as file:
                    file.write(country_code.lower())
                set_engine()

            elif edit_engine.lower() == "reset":
                with open(engine, "w") as reset:
                    reset.write("us")
                set_engine()

            else:
                clear_input()
                main()

        set_engine()

    elif initial_url.lower() in ["settings", "s"]:

        def set_settings():
            with open(settings, 'r') as file:
                contents = file.read()

            clear_input()

            print(contents, "\n")

            edit_settings = input("Edit: ").lower().replace(" ", "")

            if edit_settings.lower() in ["netflix=true", "netflix=t", "net=true", "net=t", "ne=true", "ne=t", "n=true", "n=t", "1=t"]:
                with open(settings, 'r') as file:
                    lines = file.readlines()

                if len(lines) >= 0:
                    lines[0] = "Netflix = True\n"

                with open(settings, 'w') as file:
                    file.writelines(lines)

                set_settings()

            elif edit_settings.lower() in ["netflix=false", "netflix=f", "net=false", "net=f", "ne=false", "ne=f", "n=false", "n=f", "1=f"]:
                with open(settings, 'r') as file:
                    lines = file.readlines()

                if len(lines) >= 0:
                    lines[0] = "Netflix = False\n"

                with open(settings, 'w') as file:
                    file.writelines(lines)

                set_settings()

            elif edit_settings.lower() in ["paramountplus=true", "paramountplus=t", "paramount+=true", "paramount+=t", "paramount=true", "paramount=t", "par=true", "par=t", "pa=true", "pa=t", "pp=true", "pp=t", "p+=true", "p+=t", "2=t"]:
                with open(settings, 'r') as file:
                    lines = file.readlines()

                if len(lines) > 1:
                    lines[1] = "Paramount+ = True\n"

                with open(settings, 'w') as file:
                    file.writelines(lines)

                set_settings()

            elif edit_settings.lower() in ["paramountplus=false", "paramountplus=f", "paramount+=false", "paramount+=f", "paramount=false", "paramount=f", "par=false", "par=f", "pa=false", "pa=f", "pp=false", "pp=f", "p+=false", "p+=f", "2=f"]:
                with open(settings, 'r') as file:
                    lines = file.readlines()

                if len(lines) > 1:
                    lines[1] = "Paramount+ = False\n"

                with open(settings, 'w') as file:
                    file.writelines(lines)

                set_settings()

            elif edit_settings.lower() in ["hbomax=true", "hbomax=t", "hbo=true", "hbo=t", "hb=true", "hb=t", "3=t"]:
                with open(settings, 'r') as file:
                    lines = file.readlines()

                if len(lines) > 2:
                    lines[2] = "HBOMax = True\n"

                with open(settings, 'w') as file:
                    file.writelines(lines)

                set_settings()

            elif edit_settings.lower() in ["hbomax=false", "hbomax=f", "hbo=false", "hbo=f", "hb=false", "hb=f", "3=f"]:
                with open(settings, 'r') as file:
                    lines = file.readlines()

                if len(lines) > 2:
                    lines[2] = "HBOMax = False\n"

                with open(settings, 'w') as file:
                    file.writelines(lines)

                set_settings()

            elif edit_settings.lower() in ["max=true", "max=t", "ma=true", "ma=t", "m=true", "m=t", "4=t"]:
                with open(settings, 'r') as file:
                    lines = file.readlines()

                if len(lines) > 3:
                    lines[3] = "Max = True\n"

                with open(settings, 'w') as file:
                    file.writelines(lines)

                set_settings()

            elif edit_settings.lower() in ["max=false", "max=f", "ma=false", "ma=f", "m=false", "m=f", "4=f"]:
                with open(settings, 'r') as file:
                    lines = file.readlines()

                if len(lines) > 3:
                    lines[3] = "Max = False\n"

                with open(settings, 'w') as file:
                    file.writelines(lines)

                set_settings()

            elif edit_settings.lower() in ["disneyplus=true", "disneyplus=t", "disney+=true", "disney+=t", "disney=true", "disney=t", "dis=true", "dis=t", "di=true", "di=t", "d=true", "d=t", "5=t"]:
                with open(settings, 'r') as file:
                    lines = file.readlines()

                if len(lines) > 4:
                    lines[4] = "Disney+ = True\n"

                with open(settings, 'w') as file:
                    file.writelines(lines)

                set_settings()

            elif edit_settings.lower() in ["disneyplus=false", "disneyplus=f", "disney+=false", "disney+=f", "disney=false", "disney=f", "dis=false", "dis=f", "di=false", "di=f", "d=false", "d=f", "5=f"]:
                with open(settings, 'r') as file:
                    lines = file.readlines()

                if len(lines) > 4:
                    lines[4] = "Disney+ = False\n"

                with open(settings, 'w') as file:
                    file.writelines(lines)

                set_settings()

            elif edit_settings.lower() in ["peacock=true", "peacock=t", "pea=true", "pea=t", "pe=true", "pe=t", "p=true", "p=t", "6=t"]:
                with open(settings, 'r') as file:
                    lines = file.readlines()

                if len(lines) > 5:
                    lines[5] = "Peacock = True\n"

                with open(settings, 'w') as file:
                    file.writelines(lines)

                set_settings()

            elif edit_settings.lower() in ["peacock=false", "peacock=f", "pea=false", "pea=f", "pe=false", "pe=f", "p=false", "p=f", "6=f"]:
                with open(settings, 'r') as file:
                    lines = file.readlines()

                if len(lines) > 5:
                    lines[5] = "Peacock = False\n"

                with open(settings, 'w') as file:
                    file.writelines(lines)

                set_settings()

            elif edit_settings.lower() in ["hulu=true", "hulu=t","hul=true", "hul=t", "hu=true", "hu=t", "h=true", "h=t", "7=t"]:
                with open(settings, 'r') as file:
                    lines = file.readlines()

                if len(lines) > 6:
                    lines[6] = "Hulu = True\n"

                with open(settings, 'w') as file:
                    file.writelines(lines)

                set_settings()

            elif edit_settings.lower() in ["hulu=false", "hulu=f", "hul=false", "hul=f", "hu=false", "hu=f", "h=false", "h=f", "7=f"]:
                with open(settings, 'r') as file:
                    lines = file.readlines()

                if len(lines) > 6:
                    lines[6] = "Hulu = False\n"

                with open(settings, 'w') as file:
                    file.writelines(lines)

                set_settings()

            elif edit_settings.lower() in ["shudder=true", "shudder=t", "shud=true", "shud=t", "shu=true", "shu=t", "sh=true", "sh=t", "s=true", "s=t", "8=t"]:
                with open(settings, 'r') as file:
                    lines = file.readlines()

                if len(lines) > 7:
                    lines[7] = "Shudder = True\n"

                with open(settings, 'w') as file:
                    file.writelines(lines)

                set_settings()

            elif edit_settings.lower() in ["shudder=false", "shudder=f", "shud=false", "shud=f", "shu=false", "shu=f", "sh=false", "sh=f", "s=false", "s=f", "8=f"]:
                with open(settings, 'r') as file:
                    lines = file.readlines()

                if len(lines) > 7:
                    lines[7] = "Shudder = False\n"

                with open(settings, 'w') as file:
                    file.writelines(lines)

                set_settings()

            elif edit_settings.lower() in ["viaplay=true", "viaplay=t", "via=true", "via=t", "vi=true", "vi=t", "v=true", "v=t", "9=t"]:
                with open(settings, 'r') as file:
                    lines = file.readlines()

                if len(lines) > 8:
                    lines[8] = "Viaplay = True\n"

                with open(settings, 'w') as file:
                    file.writelines(lines)

                set_settings()

            elif edit_settings.lower() in ["viaplay=false", "viaplay=f", "via=false", "via=f", "vi=false", "vi=f", "v=false", "v=f", "9=f"]:
                with open(settings, 'r') as file:
                    lines = file.readlines()

                if len(lines) > 8:
                    lines[8] = "Viaplay = False\n"

                with open(settings, 'w') as file:
                    file.writelines(lines)

                set_settings()

            elif edit_settings.lower() in ["primevideo=true", "primevideo=t", "prime=true", "prime=t", "video=true", "video=t", "pri=true", "pri=t", "pr=true", "pr=t", "pv=true", "pv=t", "10=t"]:
                with open(settings, 'r') as file:
                    lines = file.readlines()

                if len(lines) > 9:
                    lines[9] = "Prime Video = True\n"

                with open(settings, 'w') as file:
                    file.writelines(lines)

                set_settings()

            elif edit_settings.lower() in ["primevideo=false", "primevideo=f", "prime=false", "prime=f", "video=false", "video=f", "pri=false", "pri=f", "pr=false", "pr=f", "pv=false", "pv=f", "10=f"]:
                with open(settings, 'r') as file:
                    lines = file.readlines()

                if len(lines) > 9:
                    lines[9] = "Prime Video = False\n"

                with open(settings, 'w') as file:
                    file.writelines(lines)

                set_settings()

            elif edit_settings.lower() in ["appletvplus=true", "appletvplus=t", "appletv+=true", "appletv+=t", "apple=true", "apple=t", "appletv=true", "appletv=t", "app=true", "app=t", "ap=true", "ap=t", "atv=true", "atv=t", "at=true", "at=t", "tv=true", "tv=t", "tv+=true", "tv+=t", "tvplus=true", "tvplus=t", "11=t"]:
                with open(settings, 'r') as file:
                    lines = file.readlines()

                if len(lines) > 10:
                    lines[10] = "AppleTV+ = True"

                with open(settings, 'w') as file:
                    file.writelines(lines)

                set_settings()

            elif edit_settings.lower() in ["appletvplus=false", "appletvplus=f", "appletv+=false", "appletv+=f", "apple=false", "apple=f", "appletv=false", "appletv=f", "app=false", "app=f", "ap=false", "ap=f", "atv=false", "atv=f", "at=false", "at=f", "tv=false", "tv=f", "tv+=false", "tv+=f", "tvplus=false", "tvplus=f", "11=f"]:
                with open(settings, 'r') as file:
                    lines = file.readlines()

                if len(lines) > 10:
                    lines[10] = "AppleTV+ = False"

                with open(settings, 'w') as file:
                    file.writelines(lines)
    
                set_settings()

            elif edit_settings.lower() == "reset":
                with open(settings, "w") as reset:
                    reset.write("Netflix = True\nParamount+ = True\nHBOMax = True\nMax = True\nDisney+ = True\nPeacock = True\nHulu = True\nShudder = True\nViaplay = True\nPrime Video = True\nApple TV+ = True")

                set_settings()

            else:
                clear_input()
                main()

        set_settings()
    else:
        if is_url(initial_url):
            initial_url = process_url(initial_url)
        else:
            def search_justwatch(query, year=None):
                encoded_query = requests.utils.quote(query)

                with open(engine, 'r') as file:
                    search_engine = file.read()

                if search_engine in search_mapping:
                    search = f"{search_mapping[search_engine]}"
                else:
                    search = "search"

                url = f"https://www.justwatch.com/{search_engine}/{search}?q={encoded_query}"
                response = requests.get(url)

                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    if year:
                        results = soup.find_all(class_='title-list-row__column-header', limit=5)
                        for result in results:
                            header_year = result.find("span", {"class": "header-year"})
                            if header_year and f"({year})" in header_year.text:
                                if 'href' in result.attrs:
                                    full_url = f"https://www.justwatch.com{result['href']}"
                                    return full_url

                    title_column_header = soup.find(class_='title-list-row__column-header')
                    if title_column_header and 'href' in title_column_header.attrs:
                        full_url = f"https://www.justwatch.com{title_column_header['href']}"
                        return full_url
                    else:
                        sys.exit("No results found.")
                else:
                    url = f"https://www.justwatch.com/us/search?q={encoded_query}"
                    response = requests.get(url)

                    if response.status_code == 200:
                        soup = BeautifulSoup(response.content, 'html.parser')
                        
                        if year:
                            results = soup.find_all(class_='title-list-row__column-header', limit=5)
                            for result in results:
                                header_year = result.find("span", {"class": "header-year"})
                                if header_year and f"({year})" in header_year.text:
                                    if 'href' in result.attrs:
                                        full_url = f"https://www.justwatch.com{result['href']}"
                                        return full_url

                        title_column_header = soup.find(class_='title-list-row__column-header')
                        if title_column_header and 'href' in title_column_header.attrs:
                            full_url = f"https://www.justwatch.com{title_column_header['href']}"
                            return full_url
                        else:
                            sys.exit("No results found.")
                    else:
                        sys.exit("Failed to fetch JustWatch search results.")

            try:
                number_matches = re.findall(r'\b\d{4}\b', initial_url)
                
                if number_matches:
                    if initial_url.startswith(number_matches[0]):
                        if len(number_matches) > 1:
                            year = number_matches[1]
                            query_without_year = initial_url.replace(year, '').strip()
                        else:
                            query_without_year = initial_url
                            year = None
                    else:
                        if len(number_matches) >= 2:
                            year = number_matches[-1]
                            query_without_year = re.sub(r'\b' + re.escape(year) + r'\b', '', initial_url).strip()
                        elif len(number_matches) == 1:
                            year = number_matches[0]
                            query_without_year = re.sub(r'\b\d{4}\b', '', initial_url).strip()
                        else:
                            query_without_year = initial_url
                            year = None
                else:
                    query_without_year = initial_url
                    year = None
                
                query_without_year = re.sub(r'\(|\)', '', query_without_year).strip()

                url = search_justwatch(query_without_year, year)
                initial_url = url
            except:
                clear_input()
                print("No results found.")
                sys.exit()

        def read_settings(file_path):
            settings = {}
            with open(file_path, 'r') as file:
                for line in file:
                    if '=' in line:
                        key, value = line.rsplit(' = ', 1)
                        settings[key.strip()] = value.strip() == 'True'
            return settings

        def filter_icons(settings, all_icons):
            return {key: all_icons[key] for key in settings if settings[key] and key in all_icons}

        settings_icons = read_settings(settings)
        filtered_icons = filter_icons(settings_icons, all_icons)

        if not filtered_icons:
            filtered_icons = all_icons

        initial_response = requests.get(initial_url)

        if initial_response.status_code == 200:
            initial_soup = BeautifulSoup(initial_response.content, 'html.parser')
            title = extract_title_and_year(initial_soup)
            alternate_links = initial_soup.find_all('link', rel='alternate')

            clear_input()

            print("Title:", title)

            service_continents = {service: {} for service in filtered_icons}

            for index, link in enumerate(alternate_links, start=1):
                if 'hreflang' in link.attrs and 'href' in link.attrs:
                    hreflang = link['hreflang'].split('-')[-1]
                    country_name = country_mapping.get(hreflang, 'Unknown')
                    continent = continent_mapping.get(hreflang, 'Unknown')

                    country_url = link['href']
                    country_response = requests.get(country_url)
                    if country_response.status_code == 200:
                        country_soup = BeautifulSoup(country_response.content, 'html.parser')
                    found_services = find_streaming_services_icons(country_soup, filtered_icons)
                    for service, leaving_soon_list in found_services.items():
                        if continent not in service_continents[service]:
                            service_continents[service][continent] = {}
                        if country_name not in service_continents[service][continent]:
                            service_continents[service][continent][country_name] = any(leaving_soon_list)

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
                            for country, leaving_soon in continents[ordered_continent].items():
                                leaving_soon_text = "(Leaving Soon)" if leaving_soon else ""
                                print(f"  - {country} {leaving_soon_text}")
                                any_service_found = True

                    print()

            if not any_service_found:
                print("None\n")

        else:
            print(f"Failed to retrieve initial page, status code: {initial_response.status_code}")

def create_settings():
    if not os.path.exists(data_folder):
        os.makedirs(data_folder, exist_ok=True)

    if not os.path.exists(settings):
        with open(settings, "w") as create:
            create.write("Netflix = True\nParamount+ = True\nHBOMax = True\nMax = True\nDisney+ = True\nPeacock = True\nHulu = True\nShudder = True\nViaplay = True\nPrime Video = True\nApple TV+ = True")

    if not os.path.exists(engine):
        with open(engine, "w") as create:
            create.write("us")

    if ctypes.windll.shell32.IsUserAnAdmin():
        os.chmod(data_folder, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)

if __name__ == "__main__":
    create_settings_thread = threading.Thread(target=create_settings, daemon=True)
    create_settings_thread.start()
    main()
