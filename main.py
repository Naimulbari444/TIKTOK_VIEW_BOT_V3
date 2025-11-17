import requests, sys, json, uuid, time, os
from colorama import init, Fore, Back, Style

# Initialize colorama and clear screen
os.system('cls' if os.name=='nt' else 'clear')
init(autoreset=True)

# API endpoint
API = "https://zefame-free.com/api_free.php?action=config"

# Service names mapping
names = {
    229: "TikTok Views",
    228: "TikTok Followers",
    232: "TikTok Free Likes",
    235: "TikTok Free Shares",
    236: "TikTok Free Favorites"
}

def print_header():
    """Print the script header with styling"""
    print(f"\n{Fore.CYAN}{'='*60}")
    print(f"{Fore.YELLOW}╔══════════════════════════════════════════════════════════╗")
    print(f"{Fore.YELLOW}║{Fore.CYAN}                 TIKTOK SERVICES AUTOMATION               {Fore.YELLOW}║")
    print(f"{Fore.YELLOW}║{Fore.CYAN}               CREATED BY: NATMUL HACKER KING             {Fore.YELLOW}║")
    print(f"{Fore.YELLOW}╚══════════════════════════════════════════════════════════╝")
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")

def print_service_list(services):
    """Print the list of available services with styling"""
    print(f"{Fore.YELLOW}┌───────────────────── AVAILABLE SERVICES ────────────────────┐{Style.RESET_ALL}")
    
    for i, service in enumerate(services, 1):
        sid = service.get('id')
        name = names.get(sid, service.get('name', '').strip())
        rate = service.get('description', '').strip()
        
        if rate:
            rate = f"[{rate.replace('vues', 'views').replace('partages', 'shares').replace('favoris', 'favorites')}]"
        
        status = f"{Fore.GREEN}● WORKING {Style.RESET_ALL}" if service.get('available') else f"{Fore.RED}● DOWN {Style.RESET_ALL}"
        
        # Format the service entry with proper alignment
        service_line = f"{Fore.WHITE}{i:2d}. {name}"
        status_line = f"  {status}"
        rate_line = f"  {Fore.CYAN}{rate}{Style.RESET_ALL}" if rate else ""
        
        print(f"{Fore.YELLOW}│ {service_line}{status_line}{rate_line}{' '*(50-len(service_line)-len(status_line)-len(rate_line))} {Fore.YELLOW}│")
    
    print(f"{Fore.YELLOW}└─────────────────────────────────────────────────────────────┘{Style.RESET_ALL}")

def print_footer():
    """Print the script footer"""
    print(f"\n{Fore.CYAN}{'='*60}")
    print(f"{Fore.YELLOW}           THANK YOU FOR USING OUR SERVICES!")
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")

def main():
    # Print header
    print_header()
    
    # Load services data
    if len(sys.argv) > 1:
        try:
            with open(sys.argv[1]) as f:
                data = json.load(f)
            print(f"{Fore.GREEN}✓ Loaded services from file: {sys.argv[1]}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}✗ Error loading file: {e}{Style.RESET_ALL}")
            sys.exit(1)
    else:
        try:
            print(f"{Fore.YELLOW}⏳ Fetching services from API...{Style.RESET_ALL}")
            data = requests.get(API).json()
            print(f"{Fore.GREEN}✓ Successfully fetched services from API{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}✗ Error fetching from API: {e}{Style.RESET_ALL}")
            sys.exit(1)
    
    # Extract services
    services = data.get('data', {}).get('tiktok', {}).get('services', [])
    
    if not services:
        print(f"{Fore.RED}✗ No services available{Style.RESET_ALL}")
        sys.exit(1)
    
    # Print service list
    print_service_list(services)
    
    # Get user choice
    print(f"\n{Fore.YELLOW}┌─────────────────────── SELECT SERVICE ──────────────────────┐{Style.RESET_ALL}")
    choice = input(f"{Fore.YELLOW}│ {Fore.WHITE}Select number (Enter to exit): {Style.RESET_ALL}")
    print(f"{Fore.YELLOW}└─────────────────────────────────────────────────────────────┘{Style.RESET_ALL}")
    
    if not choice:
        print_footer()
        sys.exit()
    
    # Validate choice
    try:
        idx = int(choice)
        if idx < 1 or idx > len(services):
            print(f"{Fore.RED}✗ Selection out of range{Style.RESET_ALL}")
            sys.exit(1)
    except:
        print(f"{Fore.RED}✗ Invalid selection{Style.RESET_ALL}")
        sys.exit(1)
    
    # Get selected service
    selected = services[idx-1]
    service_name = names.get(selected.get('id'), selected.get('name', '').strip())
    
    print(f"\n{Fore.GREEN}✓ Selected: {service_name}{Style.RESET_ALL}")
    
    # Get video link
    print(f"\n{Fore.YELLOW}┌────────────────────── ENTER VIDEO LINK ────────────────────┐{Style.RESET_ALL}")
    video_link = input(f"{Fore.YELLOW}│ {Fore.WHITE}Enter video link: {Style.RESET_ALL}")
    print(f"{Fore.YELLOW}└─────────────────────────────────────────────────────────────┘{Style.RESET_ALL}")
    
    if not video_link:
        print(f"{Fore.RED}✗ No video link provided{Style.RESET_ALL}")
        sys.exit(1)
    
    # Parse video ID
    print(f"\n{Fore.YELLOW}⏳ Parsing video ID...{Style.RESET_ALL}")
    try:
        id_check = requests.post("https://zefame-free.com/api_free.php?", 
                                data={"action": "checkVideoId", "link": video_link})
        video_id = id_check.json().get("data", {}).get("videoId")
        
        if video_id:
            print(f"{Fore.GREEN}✓ Parsed Video ID: {video_id}{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}✗ Could not parse Video ID{Style.RESET_ALL}")
            sys.exit(1)
    except Exception as e:
        print(f"{Fore.RED}✗ Error parsing video ID: {e}{Style.RESET_ALL}")
        sys.exit(1)
    
    # Process orders
    print(f"\n{Fore.YELLOW}┌───────────────────── PROCESSING ORDERS ────────────────────┐{Style.RESET_ALL}")
    
    order_count = 0
    while True:
        try:
            order_count += 1
            print(f"{Fore.YELLOW}│ {Fore.WHITE}Processing order #{order_count}...{Style.RESET_ALL}")
            
            order = requests.post("https://zefame-free.com/api_free.php?action=order", 
                                data={"service": selected.get('id'), 
                                      "link": video_link, 
                                      "uuid": str(uuid.uuid4()), 
                                      "videoId": video_id})
            
            result = order.json()
            
            # Display result with appropriate color
            if result.get("success"):
                print(f"{Fore.YELLOW}│ {Fore.GREEN}✓ Order successful: {result.get('message', 'N/A')}{Style.RESET_ALL}")
            else:
                print(f"{Fore.YELLOW}│ {Fore.RED}✗ Order failed: {result.get('message', 'N/A')}{Style.RESET_ALL}")
            
            # Check if we need to wait before next order
            wait = result.get("data", {}).get("nextAvailable")
            if wait:
                try:
                    wait = float(wait)
                    if wait > time.time():
                        wait_time = wait - time.time() + 1
                        print(f"{Fore.YELLOW}│ {Fore.CYAN}⏳ Waiting {wait_time:.1f} seconds before next order...{Style.RESET_ALL}")
                        time.sleep(wait_time)
                except:
                    pass
                    
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}│ {Fore.RED}✗ Process interrupted by user{Style.RESET_ALL}")
            break
        except Exception as e:
            print(f"{Fore.YELLOW}│ {Fore.RED}✗ Error processing order: {e}{Style.RESET_ALL}")
            break
    
    print(f"{Fore.YELLOW}└─────────────────────────────────────────────────────────────┘{Style.RESET_ALL}")
    
    # Print footer
    print_footer()

if __name__ == "__main__":
    main()