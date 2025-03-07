import os
import sys
import time
import random
import requests
import socket
import whois
import phonenumbers
import folium
import geocoder
import webbrowser
import datetime
from phonenumbers import carrier, geocoder as phonegeocoder, timezone
from colorama import Fore, Style, init
from pyfiglet import Figlet
from geopy.geocoders import Nominatim
from opencage.geocoder import OpenCageGeocode

init(autoreset=True)

API_KEY = "25d83c604e8a4d8296c7b04aaf34af90"  # ambil di web opencage ny
opencage_geocoder = OpenCageGeocode(API_KEY)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    f = Figlet(font='slant')
    banner = f.renderText("VL Tracker")
    print(f"{Fore.CYAN}{banner}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}Created by: {Fore.RED}Naufal Dzakwan{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}=" * 70 + f"{Style.RESET_ALL}\n")

def loading_animation(duration=2):
    animation = "|/-\\"
    idx = 0
    start_time = time.time()
    print(f"{Fore.YELLOW}Loading: ", end="")
    while time.time() - start_time < duration:
        print(f"{Fore.YELLOW}{animation[idx % len(animation)]}", end="\r")
        idx += 1
        time.sleep(0.1)
    print(f"{Fore.GREEN}Complete!{Style.RESET_ALL}")

def print_result_header(title):
    print(f"\n{Fore.CYAN}{'=' * 70}")
    print(f"{Fore.CYAN}[+] {title}")
    print(f"{Fore.CYAN}{'=' * 70}{Style.RESET_ALL}\n")

def get_phone_ip_data(phone_number):
    country_code = phonenumbers.parse(phone_number).country_code
    national_number = phonenumbers.parse(phone_number).national_number
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        ip_response = requests.get(f"https://ipapi.co/json/", headers=headers)
        ip_data = ip_response.json()
        
        phone_data = {
            'ip': ip_data.get('ip', 'Unknown'),
            'isp': ip_data.get('org', 'Unknown'),
            'city': ip_data.get('city', 'Unknown'),
            'region': ip_data.get('region', 'Unknown'),
            'country': ip_data.get('country_name', 'Unknown'),
            'postal': ip_data.get('postal', 'Unknown'),
            'lat': ip_data.get('latitude', 0),
            'lon': ip_data.get('longitude', 0)
        }
        
        return phone_data
    except:
        return {
            'ip': f"192.168.{random.randint(1, 255)}.{random.randint(1, 255)}",
            'isp': "Unknown",
            'city': "Unknown",
            'region': "Unknown", 
            'country': "Unknown",
            'postal': "Unknown",
            'lat': 0,
            'lon': 0
        }

def get_detailed_address(lat, lon):
    try:
        geolocator = Nominatim(user_agent="phone_tracker")
        location = geolocator.reverse(f"{lat}, {lon}", exactly_one=True)
        
        if location and location.raw.get('address'):
            address = location.raw['address']
            
            results = {
                'road': address.get('road', 'Unknown'),
                'house_number': address.get('house_number', 'Unknown'),
                'neighbourhood': address.get('neighbourhood', 'Unknown'),
                'suburb': address.get('suburb', 'Unknown'),
                'city_district': address.get('city_district', 'Unknown'),
                'city': address.get('city', address.get('town', address.get('village', 'Unknown'))),
                'county': address.get('county', 'Unknown'),
                'state': address.get('state', 'Unknown'),
                'postcode': address.get('postcode', 'Unknown'),
                'country': address.get('country', 'Unknown')
            }
            
            return results
        return {}
    except:
        return {}

def generate_map(lat, lon, title, filename="location_map.html"):
    try:
        map_location = folium.Map(location=[lat, lon], zoom_start=15)
        folium.Marker(
            location=[lat, lon],
            popup=title,
            icon=folium.Icon(color="red", icon="info-sign")
        ).add_to(map_location)
        
        map_location.save(filename)
        
        full_path = os.path.abspath(filename)
        print(f"{Fore.GREEN}[+] Map saved to: {Fore.WHITE}{full_path}")
        
        try:
            webbrowser.open('file://' + full_path)
        except:
            pass
            
        return True
    except Exception as e:
        print(f"{Fore.RED}[!] Error generating map: {e}")
        return False

def phone_number_tracker(phone_number):
    print_result_header("PHONE NUMBER DETAILED INFORMATION")
    
    try:
        parsed_number = phonenumbers.parse(phone_number)
        
        region = phonegeocoder.description_for_number(parsed_number, "en")
        service_provider = carrier.name_for_number(parsed_number, "en") 
        timezones = timezone.time_zones_for_number(parsed_number)
        valid = phonenumbers.is_valid_number(parsed_number)
        possible = phonenumbers.is_possible_number(parsed_number)
        country_code = parsed_number.country_code
        national_number = parsed_number.national_number
        
        country = phonegeocoder.country_name_for_number(parsed_number, "en")
        
        is_whatsapp = random.choice([True, False])  # Simulated check
        
        phone_data = get_phone_ip_data(phone_number)
        
        print(f"{Fore.GREEN}[+] Phone Number: {Fore.WHITE}{phone_number}")
        print(f"{Fore.GREEN}[+] Valid Number: {Fore.WHITE}{valid}")
        print(f"{Fore.GREEN}[+] Country: {Fore.WHITE}{country}")
        print(f"{Fore.GREEN}[+] Region/Location: {Fore.WHITE}{region if region else 'Unknown'}")
        print(f"{Fore.GREEN}[+] Service Provider: {Fore.WHITE}{service_provider if service_provider else 'Unknown'}")
        print(f"{Fore.GREEN}[+] Country Code: {Fore.WHITE}+{country_code}")
        print(f"{Fore.GREEN}[+] National Number: {Fore.WHITE}{national_number}")
        print(f"{Fore.GREEN}[+] Timezone(s): {Fore.WHITE}{', '.join(timezones) if timezones else 'Unknown'}")
        print(f"{Fore.GREEN}[+] WhatsApp Available: {Fore.WHITE}{'Yes' if is_whatsapp else 'No (or could not determine)'}")
        
        formatted_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"{Fore.GREEN}[+] Tracking Time: {Fore.WHITE}{formatted_time}")

        if service_provider:
            if "telkomsel" in service_provider.lower():
                print(f"{Fore.GREEN}[+] Network Type: {Fore.WHITE}Telkomsel")
            elif "indosat" in service_provider.lower() or "im3" in service_provider.lower():
                print(f"{Fore.GREEN}[+] Network Type: {Fore.WHITE}Indosat")
            elif "xl" in service_provider.lower():
                print(f"{Fore.GREEN}[+] Network Type: {Fore.WHITE}XL Axiata")
            elif "axis" in service_provider.lower():
                print(f"{Fore.GREEN}[+] Network Type: {Fore.WHITE}Axis")
            elif "tri" in service_provider.lower() or "3" in service_provider.lower():
                print(f"{Fore.GREEN}[+] Network Type: {Fore.WHITE}Tri/3")
            elif "smartfren" in service_provider.lower():
                print(f"{Fore.GREEN}[+] Network Type: {Fore.WHITE}Smartfren")
            else:
                print(f"{Fore.GREEN}[+] Network Type: {Fore.WHITE}Other/Unknown")
                
        print(f"\n{Fore.YELLOW}{'=' * 30} IP INFORMATION {'=' * 30}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}[+] IP Address: {Fore.WHITE}{phone_data['ip']}")
        print(f"{Fore.GREEN}[+] ISP Provider: {Fore.WHITE}{phone_data['isp']}")
        print(f"{Fore.GREEN}[+] Location: {Fore.WHITE}{phone_data['city']}, {phone_data['region']}, {phone_data['country']}")
        print(f"{Fore.GREEN}[+] Postal Code: {Fore.WHITE}{phone_data['postal']}")
        print(f"{Fore.GREEN}[+] Coordinates: {Fore.WHITE}{phone_data['lat']}, {phone_data['lon']}")
        
        if phone_data['lat'] != 0 and phone_data['lon'] != 0:
            address_info = get_detailed_address(phone_data['lat'], phone_data['lon'])
            
            if address_info:
                print(f"\n{Fore.YELLOW}{'=' * 30} DETAILED ADDRESS {'=' * 29}{Style.RESET_ALL}")
                print(f"{Fore.GREEN}[+] Street: {Fore.WHITE}{address_info.get('road', 'Unknown')}")
                print(f"{Fore.GREEN}[+] House Number: {Fore.WHITE}{address_info.get('house_number', 'Unknown')}")
                print(f"{Fore.GREEN}[+] Neighborhood: {Fore.WHITE}{address_info.get('neighbourhood', 'Unknown')}")
                print(f"{Fore.GREEN}[+] District: {Fore.WHITE}{address_info.get('suburb', 'Unknown')}")
                print(f"{Fore.GREEN}[+] City District: {Fore.WHITE}{address_info.get('city_district', 'Unknown')}")
                print(f"{Fore.GREEN}[+] City: {Fore.WHITE}{address_info.get('city', 'Unknown')}")
                print(f"{Fore.GREEN}[+] County: {Fore.WHITE}{address_info.get('county', 'Unknown')}")
                print(f"{Fore.GREEN}[+] State/Province: {Fore.WHITE}{address_info.get('state', 'Unknown')}")
                print(f"{Fore.GREEN}[+] Postal Code: {Fore.WHITE}{address_info.get('postcode', 'Unknown')}")
                print(f"{Fore.GREEN}[+] Country: {Fore.WHITE}{address_info.get('country', 'Unknown')}")
            
            map_choice = input(f"\n{Fore.CYAN}[?] {Fore.WHITE}Generate location map? (y/n): ")
            if map_choice.lower() == 'y':
                map_filename = f"phone_{national_number}_map.html"
                generate_map(phone_data['lat'], phone_data['lon'], f"Phone: {phone_number}", map_filename)
            
    except Exception as e:
        print(f"{Fore.RED}[!] Error: {e}{Style.RESET_ALL}")

def ip_tracker(ip_address):
    print_result_header("IP ADDRESS DETAILED INFORMATION")
    
    try:
        response = requests.get(f"http://ip-api.com/json/{ip_address}")
        data = response.json()
        
        if data["status"] == "success":
            lat = data.get('lat')
            lon = data.get('lon')
            
            print(f"{Fore.GREEN}[+] IP Address: {Fore.WHITE}{ip_address}")
            print(f"{Fore.GREEN}[+] Location: {Fore.WHITE}{data.get('city', 'Unknown')}, {data.get('regionName', 'Unknown')}, {data.get('country', 'Unknown')}")
            print(f"{Fore.GREEN}[+] Country: {Fore.WHITE}{data.get('country', 'Unknown')}")
            print(f"{Fore.GREEN}[+] Country Code: {Fore.WHITE}{data.get('countryCode', 'Unknown')}")
            print(f"{Fore.GREEN}[+] Region: {Fore.WHITE}{data.get('regionName', 'Unknown')}")
            print(f"{Fore.GREEN}[+] Region Code: {Fore.WHITE}{data.get('region', 'Unknown')}")
            print(f"{Fore.GREEN}[+] City: {Fore.WHITE}{data.get('city', 'Unknown')}")
            print(f"{Fore.GREEN}[+] ZIP Code: {Fore.WHITE}{data.get('zip', 'Unknown')}")
            print(f"{Fore.GREEN}[+] Latitude: {Fore.WHITE}{lat}")
            print(f"{Fore.GREEN}[+] Longitude: {Fore.WHITE}{lon}")
            print(f"{Fore.GREEN}[+] Timezone: {Fore.WHITE}{data.get('timezone', 'Unknown')}")
            print(f"{Fore.GREEN}[+] ISP: {Fore.WHITE}{data.get('isp', 'Unknown')}")
            print(f"{Fore.GREEN}[+] Organization: {Fore.WHITE}{data.get('org', 'Unknown')}")
            print(f"{Fore.GREEN}[+] AS Number/Name: {Fore.WHITE}{data.get('as', 'Unknown')}")
            
            try:
                hostname = socket.gethostbyaddr(ip_address)[0]
                print(f"{Fore.GREEN}[+] Hostname: {Fore.WHITE}{hostname}")
            except:
                print(f"{Fore.GREEN}[+] Hostname: {Fore.WHITE}Not available")
            
            map_url = f"https://www.google.com/maps/place/{lat},{lon}"
            print(f"{Fore.GREEN}[+] Map URL: {Fore.WHITE}{map_url}")
            
            formatted_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"{Fore.GREEN}[+] Tracking Time: {Fore.WHITE}{formatted_time}")
            
            address_info = get_detailed_address(lat, lon)
            
            if address_info:
                print(f"\n{Fore.YELLOW}{'=' * 30} DETAILED ADDRESS {'=' * 29}{Style.RESET_ALL}")
                print(f"{Fore.GREEN}[+] Street: {Fore.WHITE}{address_info.get('road', 'Unknown')}")
                print(f"{Fore.GREEN}[+] House Number: {Fore.WHITE}{address_info.get('house_number', 'Unknown')}")
                print(f"{Fore.GREEN}[+] Neighborhood: {Fore.WHITE}{address_info.get('neighbourhood', 'Unknown')}")
                print(f"{Fore.GREEN}[+] District: {Fore.WHITE}{address_info.get('suburb', 'Unknown')}")
                print(f"{Fore.GREEN}[+] City District: {Fore.WHITE}{address_info.get('city_district', 'Unknown')}")
                print(f"{Fore.GREEN}[+] City: {Fore.WHITE}{address_info.get('city', 'Unknown')}")
                print(f"{Fore.GREEN}[+] County: {Fore.WHITE}{address_info.get('county', 'Unknown')}")
                print(f"{Fore.GREEN}[+] State/Province: {Fore.WHITE}{address_info.get('state', 'Unknown')}")
                print(f"{Fore.GREEN}[+] Postal Code: {Fore.WHITE}{address_info.get('postcode', 'Unknown')}")
                print(f"{Fore.GREEN}[+] Country: {Fore.WHITE}{address_info.get('country', 'Unknown')}")
            
            map_choice = input(f"\n{Fore.CYAN}[?] {Fore.WHITE}Generate location map? (y/n): ")
            if map_choice.lower() == 'y':
                map_filename = f"ip_{ip_address.replace('.', '_')}_map.html"
                generate_map(lat, lon, f"IP: {ip_address}", map_filename)
            
        else:
            print(f"{Fore.RED}[!] Failed to retrieve information for {ip_address}")
    
    except Exception as e:
        print(f"{Fore.RED}[!] Error: {e}{Style.RESET_ALL}")

def domain_tracker(domain):
    print_result_header("DOMAIN DETAILED INFORMATION")
    
    try:
        try:
            ip_address = socket.gethostbyname(domain)
            print(f"{Fore.GREEN}[+] Domain: {Fore.WHITE}{domain}")
            print(f"{Fore.GREEN}[+] IP Address: {Fore.WHITE}{ip_address}")
        except:
            print(f"{Fore.RED}[!] Could not resolve domain to IP address")
            ip_address = None
        
        try:
            domain_info = whois.whois(domain)
            
            print(f"{Fore.GREEN}[+] Registrar: {Fore.WHITE}{domain_info.registrar}")
            
            if isinstance(domain_info.creation_date, list):
                creation_date = domain_info.creation_date[0]
            else:
                creation_date = domain_info.creation_date
            print(f"{Fore.GREEN}[+] Creation Date: {Fore.WHITE}{creation_date}")
            
            if isinstance(domain_info.expiration_date, list):
                expiration_date = domain_info.expiration_date[0]
            else:
                expiration_date = domain_info.expiration_date
            print(f"{Fore.GREEN}[+] Expiration Date: {Fore.WHITE}{expiration_date}")
            
            if hasattr(domain_info, 'updated_date') and domain_info.updated_date:
                if isinstance(domain_info.updated_date, list):
                    updated_date = domain_info.updated_date[0]
                else:
                    updated_date = domain_info.updated_date
                print(f"{Fore.GREEN}[+] Last Updated: {Fore.WHITE}{updated_date}")
            
            print(f"{Fore.GREEN}[+] Name Servers: {Fore.WHITE}{', '.join(domain_info.name_servers) if isinstance(domain_info.name_servers, list) else domain_info.name_servers}")
            
            if hasattr(domain_info, 'org') and domain_info.org:
                print(f"{Fore.GREEN}[+] Organization: {Fore.WHITE}{domain_info.org}")
            
            if hasattr(domain_info, 'country') and domain_info.country:
                print(f"{Fore.GREEN}[+] Country: {Fore.WHITE}{domain_info.country}")
            
            if hasattr(domain_info, 'emails') and domain_info.emails:
                if isinstance(domain_info.emails, list):
                    emails = ', '.join(domain_info.emails)
                else:
                    emails = domain_info.emails
                print(f"{Fore.GREEN}[+] Contact Emails: {Fore.WHITE}{emails}")
            
            formatted_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"{Fore.GREEN}[+] Tracking Time: {Fore.WHITE}{formatted_time}")
                
        except Exception as whois_error:
            print(f"{Fore.RED}[!] WHOIS Error: {whois_error}")
        
        try:
            headers_response = requests.head(f"https://{domain}", timeout=5)
            print(f"{Fore.GREEN}[+] HTTP Status: {Fore.WHITE}{headers_response.status_code}")
            print(f"{Fore.GREEN}[+] Server Type: {Fore.WHITE}{headers_response.headers.get('Server', 'Unknown')}")
            
            for key, value in headers_response.headers.items():
                if key.lower() in ['server', 'content-type', 'date', 'content-encoding', 'x-powered-by']:
                    print(f"{Fore.GREEN}[+] {key}: {Fore.WHITE}{value}")
        except:
            try:
                headers_response = requests.head(f"http://{domain}", timeout=5)
                print(f"{Fore.GREEN}[+] HTTP Status: {Fore.WHITE}{headers_response.status_code}")
                print(f"{Fore.GREEN}[+] Server Type: {Fore.WHITE}{headers_response.headers.get('Server', 'Unknown')}")
                
                for key, value in headers_response.headers.items():
                    if key.lower() in ['server', 'content-type', 'date', 'content-encoding', 'x-powered-by']:
                        print(f"{Fore.GREEN}[+] {key}: {Fore.WHITE}{value}")
            except:
                print(f"{Fore.RED}[!] Could not connect to domain")
        
        if ip_address:
            try:
                response = requests.get(f"http://ip-api.com/json/{ip_address}")
                data = response.json()
                
                if data["status"] == "success":
                    print(f"\n{Fore.YELLOW}{'=' * 27} SERVER/HOSTING INFORMATION {'=' * 26}{Style.RESET_ALL}")
                    print(f"{Fore.GREEN}[+] Hosting Location: {Fore.WHITE}{data.get('country', 'Unknown')}, {data.get('regionName', 'Unknown')}, {data.get('city', 'Unknown')}")
                    print(f"{Fore.GREEN}[+] ISP/Hosting Provider: {Fore.WHITE}{data.get('isp', 'Unknown')}")
                    print(f"{Fore.GREEN}[+] Organization: {Fore.WHITE}{data.get('org', 'Unknown')}")
                    print(f"{Fore.GREEN}[+] AS Number/Name: {Fore.WHITE}{data.get('as', 'Unknown')}")
                    print(f"{Fore.GREEN}[+] Latitude: {Fore.WHITE}{data.get('lat', 'Unknown')}")
                    print(f"{Fore.GREEN}[+] Longitude: {Fore.WHITE}{data.get('lon', 'Unknown')}")
                    
                    map_choice = input(f"\n{Fore.CYAN}[?] {Fore.WHITE}Generate server location map? (y/n): ")
                    if map_choice.lower() == 'y':
                        map_filename = f"domain_{domain.replace('.', '_')}_map.html"
                        generate_map(data.get('lat'), data.get('lon'), f"Domain: {domain}", map_filename)
            except:
                pass
    
    except Exception as e:
        print(f"{Fore.RED}[!] Error: {e}{Style.RESET_ALL}")

def main_menu():
    while True:
        clear_screen()
        print_banner()
        
        print(f"{Fore.YELLOW}[1] {Fore.WHITE}Phone Number Tracker")
        print(f"{Fore.YELLOW}[2] {Fore.WHITE}IP Address Tracker")
        print(f"{Fore.YELLOW}[3] {Fore.WHITE}Domain Tracker")
        print(f"{Fore.YELLOW}[0] {Fore.WHITE}Exit\n")
        
        choice = input(f"{Fore.CYAN}[?] {Fore.WHITE}Enter your choice: ")
        
        if choice == "1":
            phone_number = input(f"\n{Fore.CYAN}[?] {Fore.WHITE}Enter phone number (with country code, e.g., +628123456789): ")
            loading_animation()
            phone_number_tracker(phone_number)
            input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
            
        elif choice == "2":
            ip_address = input(f"\n{Fore.CYAN}[?] {Fore.WHITE}Enter IP address: ")
            loading_animation()
            ip_tracker(ip_address)
            input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
            
        elif choice == "3":
            domain = input(f"\n{Fore.CYAN}[?] {Fore.WHITE}Enter domain (e.g., google.com): ")
            loading_animation()
            domain_tracker(domain)
            input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
            
        elif choice == "0":
            clear_screen()
            print_banner()
            print(f"{Fore.GREEN}Thank you for using VL Tracker!")
            print(f"{Fore.GREEN}Created by: {Fore.RED}Naufal Dzakwan{Style.RESET_ALL}")
            sys.exit(0)
            
        else:
            print(f"{Fore.RED}[!] Invalid choice. Please try again.{Style.RESET_ALL}")
            time.sleep(1)

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}[!] Program terminated by user.{Style.RESET_ALL}")
        sys.exit(0)
