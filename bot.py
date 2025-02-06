import cloudscraper
from fake_useragent import FakeUserAgent
from datetime import datetime
from colorama import *
import asyncio, json, string, random, os, pytz

wib = pytz.timezone('Asia/Jakarta')

class Bless:
    def __init__(self) -> None:
        self.scraper = cloudscraper.create_scraper()
        self.headers = {
            "Accept": "*/*",
            "Accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "Origin": "chrome-extension://pljbjcehnhcnofmkdbjolghdcjnmekia",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "cross-site",
            "User-Agent": FakeUserAgent().random
        }
        self.proxies = []
        self.proxy_index = 0
        self.account_proxies = {}

    def clear_terminal(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def log(self, message):
        print(
            f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}{message}",
            flush=True
        )

    def welcome(self):
        print(
            f"""
        {Fore.GREEN + Style.BRIGHT}Auto Ping {Fore.BLUE + Style.BRIGHT}Bless - BOT
            """
            f"""
        {Fore.GREEN + Style.BRIGHT}Rey? {Fore.YELLOW + Style.BRIGHT}<INI WATERMARK>
            """
        )

    def format_seconds(self, seconds):
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"
    
    async def load_proxies(self, use_proxy_choice: int):
        filename = "proxy.txt"
        try:
            if use_proxy_choice == 1:
                response = await asyncio.to_thread(self.scraper.get, "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/all.txt")
                response.raise_for_status()
                content = response.text
                with open(filename, 'w') as f:
                    f.write(content)
                self.proxies = content.splitlines()
            else:
                if not os.path.exists(filename):
                    self.log(f"{Fore.RED + Style.BRIGHT}File {filename} Not Found.{Style.RESET_ALL}")
                    return
                with open(filename, 'r') as f:
                    self.proxies = f.read().splitlines()
            
            if not self.proxies:
                self.log(f"{Fore.RED + Style.BRIGHT}No Proxies Found.{Style.RESET_ALL}")
                return

            self.log(
                f"{Fore.GREEN + Style.BRIGHT}Proxies Total  : {Style.RESET_ALL}"
                f"{Fore.WHITE + Style.BRIGHT}{len(self.proxies)}{Style.RESET_ALL}"
            )
        
        except Exception as e:
            self.log(f"{Fore.RED + Style.BRIGHT}Failed To Load Proxies: {e}{Style.RESET_ALL}")
            self.proxies = []

    def check_proxy_schemes(self, proxies):
        schemes = ["http://", "https://", "socks4://", "socks5://"]
        if any(proxies.startswith(scheme) for scheme in schemes):
            return {"http":proxies, "https":proxies}
        return {"http":f"http://{proxies}", "https":f"http://{proxies}"}

    def get_next_proxy_for_account(self, account):
        if account not in self.account_proxies:
            if not self.proxies:
                return None
            proxy = self.check_proxy_schemes(self.proxies[self.proxy_index])
            self.account_proxies[account] = proxy
            self.proxy_index = (self.proxy_index + 1) % len(self.proxies)
        return self.account_proxies[account]

    def rotate_proxy_for_account(self, account):
        if not self.proxies:
            return None
        proxy = self.check_proxy_schemes(self.proxies[self.proxy_index])
        self.account_proxies[account] = proxy
        self.proxy_index = (self.proxy_index + 1) % len(self.proxies)
        return proxy
    
    def load_accounts(self):
        try:
            with open('accounts.json', 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            return []
        
    def get_random_hardware_identifier(self):
        hardware_id = ''.join(random.choices(string.hexdigits.lower(), k=64))
        return hardware_id

    def generate_hardware_info(self):
        cpu_models = [
            "AMD Ryzen 9 5900HS", "Intel Core i7-10700K", "AMD Ryzen 5 3600",
            "Intel Core i9-10900K", "AMD Ryzen 7 3700X", "Intel Core i5-10600K",
            "AMD Ryzen 3 3300X", "Intel Core i3-10100", "AMD Ryzen 7 5800X",
            "Intel Core i5-11600K", "AMD Ryzen 5 5600X", "Intel Core i3-10320",
            "AMD Ryzen 3 3100", "Intel Core i9-9900K", "AMD Ryzen 9 3900X",
            "Intel Core i7-9700K", "AMD Ryzen 7 2700X", "Intel Core i5-9600K",
            "AMD Ryzen 5 2600", "Intel Core i3-9100", "AMD Ryzen 3 2200G",
            "Intel Core i9-11900K", "AMD Ryzen 9 5950X", "Intel Core i7-11700K",
            "AMD Ryzen 5 4500U", "Intel Core i7-10750H", "AMD Ryzen 7 4800H",
            "Intel Core i5-10210U", "AMD Ryzen 3 4300U", "Intel Core i3-1005G1",
            "AMD Ryzen 9 4900HS", "Intel Core i9-10850K", "AMD Ryzen 9 3950X",
            "Intel Core i7-10700", "AMD Ryzen 7 3700U", "Intel Core i5-10400",
            "AMD Ryzen 5 3550H", "Intel Core i3-10100F", "AMD Ryzen 3 3200G",
            "Intel Core i9-9900KS", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i7-9750H", "AMD Ryzen 5 4600H",
            "Intel Core i9-10940X", "AMD Ryzen 7 2700", "Intel Core i5-9400F",
            "AMD Ryzen 3 1200", "Intel Core i3-8100", "AMD Ryzen 9 5900X",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i7-10710U", "AMD Ryzen 7 2700E",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i9-10980HK", "AMD Ryzen 5 3600X",
            "Intel Core i7-10700F", "AMD Ryzen 7 2700", "Intel Core i5-9400",
            "AMD Ryzen 3 1200", "Intel Core i3-8100", "AMD Ryzen 9 5900X",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i7-10710U", "AMD Ryzen 7 2700E",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i9-10980HK", "AMD Ryzen 5 3600X",
            "Intel Core i7-10700F", "AMD Ryzen 7 2700", "Intel Core i5-9400",
            "AMD Ryzen 3 1200", "Intel Core i3-8100", "AMD Ryzen 9 5900X",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i7-10710U", "AMD Ryzen 7 2700E",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i9-10980HK", "AMD Ryzen 5 3600X",
            "Intel Core i7-10700F", "AMD Ryzen 7 2700", "Intel Core i5-9400",
            "AMD Ryzen 3 1200", "Intel Core i3-8100", "AMD Ryzen 9 5900X",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i7-10710U", "AMD Ryzen 7 2700E",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i9-10980HK", "AMD Ryzen 5 3600X",
            "Intel Core i7-10700F", "AMD Ryzen 7 2700", "Intel Core i5-9400",
            "AMD Ryzen 3 1200", "Intel Core i3-8100", "AMD Ryzen 9 5900X",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i7-10710U", "AMD Ryzen 7 2700E",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i9-10980HK", "AMD Ryzen 5 3600X",
            "Intel Core i7-10700F", "AMD Ryzen 7 2700", "Intel Core i5-9400",
            "AMD Ryzen 3 1200", "Intel Core i3-8100", "AMD Ryzen 9 5900X",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i7-10710U", "AMD Ryzen 7 2700E",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i9-10980HK", "AMD Ryzen 5 3600X",
            "Intel Core i7-10700F", "AMD Ryzen 7 2700", "Intel Core i5-9400",
            "AMD Ryzen 3 1200", "Intel Core i3-8100", "AMD Ryzen 9 5900X",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i7-10710U", "AMD Ryzen 7 2700E",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i9-10980HK", "AMD Ryzen 5 3600X",
            "Intel Core i7-10700F", "AMD Ryzen 7 2700", "Intel Core i5-9400",
            "AMD Ryzen 3 1200", "Intel Core i3-8100", "AMD Ryzen 9 5900X",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i7-10710U", "AMD Ryzen 7 2700E",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i9-10980HK", "AMD Ryzen 5 3600X",
            "Intel Core i7-10700F", "AMD Ryzen 7 2700", "Intel Core i5-9400",
            "AMD Ryzen 3 1200", "Intel Core i3-8100", "AMD Ryzen 9 5900X",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i7-10710U", "AMD Ryzen 7 2700E",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i9-10980HK", "AMD Ryzen 5 3600X",
            "Intel Core i7-10700F", "AMD Ryzen 7 2700", "Intel Core i5-9400",
            "AMD Ryzen 3 1200", "Intel Core i3-8100", "AMD Ryzen 9 5900X",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i7-10710U", "AMD Ryzen 7 2700E",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i9-10980HK", "AMD Ryzen 5 3600X",
            "Intel Core i7-10700F", "AMD Ryzen 7 2700", "Intel Core i5-9400",
            "AMD Ryzen 3 1200", "Intel Core i3-8100", "AMD Ryzen 9 5900X",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i7-10710U", "AMD Ryzen 7 2700E",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i9-10980HK", "AMD Ryzen 5 3600X",
            "Intel Core i7-10700F", "AMD Ryzen 7 2700", "Intel Core i5-9400",
            "AMD Ryzen 3 1200", "Intel Core i3-8100", "AMD Ryzen 9 5900X",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i7-10710U", "AMD Ryzen 7 2700E",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i9-10980HK", "AMD Ryzen 5 3600X",
            "Intel Core i7-10700F", "AMD Ryzen 7 2700", "Intel Core i5-9400",
            "AMD Ryzen 3 1200", "Intel Core i3-8100", "AMD Ryzen 9 5900X",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i7-10710U", "AMD Ryzen 7 2700E",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i9-10980HK", "AMD Ryzen 5 3600X",
            "Intel Core i7-10700F", "AMD Ryzen 7 2700", "Intel Core i5-9400",
            "AMD Ryzen 3 1200", "Intel Core i3-8100", "AMD Ryzen 9 5900X",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i7-10710U", "AMD Ryzen 7 2700E",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i9-10980HK", "AMD Ryzen 5 3600X",
            "Intel Core i7-10700F", "AMD Ryzen 7 2700", "Intel Core i5-9400",
            "AMD Ryzen 3 1200", "Intel Core i3-8100", "AMD Ryzen 9 5900X",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i7-10710U", "AMD Ryzen 7 2700E",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i9-10980HK", "AMD Ryzen 5 3600X",
            "Intel Core i7-10700F", "AMD Ryzen 7 2700", "Intel Core i5-9400",
            "AMD Ryzen 3 1200", "Intel Core i3-8100", "AMD Ryzen 9 5900X",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i7-10710U", "AMD Ryzen 7 2700E",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i9-10980HK", "AMD Ryzen 5 3600X",
            "Intel Core i7-10700F", "AMD Ryzen 7 2700", "Intel Core i5-9400",
            "AMD Ryzen 3 1200", "Intel Core i3-8100", "AMD Ryzen 9 5900X",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i7-10710U", "AMD Ryzen 7 2700E",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i9-10980HK", "AMD Ryzen 5 3600X",
            "Intel Core i7-10700F", "AMD Ryzen 7 2700", "Intel Core i5-9400",
            "AMD Ryzen 3 1200", "Intel Core i3-8100", "AMD Ryzen 9 5900X",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i7-10710U", "AMD Ryzen 7 2700E",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i9-10980HK", "AMD Ryzen 5 3600X",
            "Intel Core i7-10700F", "AMD Ryzen 7 2700", "Intel Core i5-9400",
            "AMD Ryzen 3 1200", "Intel Core i3-8100", "AMD Ryzen 9 5900X",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i7-10710U", "AMD Ryzen 7 2700E",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i9-10980HK", "AMD Ryzen 5 3600X",
            "Intel Core i7-10700F", "AMD Ryzen 7 2700", "Intel Core i5-9400",
            "AMD Ryzen 3 1200", "Intel Core i3-8100", "AMD Ryzen 9 5900X",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i7-10710U", "AMD Ryzen 7 2700E",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i9-10980HK", "AMD Ryzen 5 3600X",
            "Intel Core i7-10700F", "AMD Ryzen 7 2700", "Intel Core i5-9400",
            "AMD Ryzen 3 1200", "Intel Core i3-8100", "AMD Ryzen 9 5900X",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i7-10710U", "AMD Ryzen 7 2700E",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i9-10980HK", "AMD Ryzen 5 3600X",
            "Intel Core i7-10700F", "AMD Ryzen 7 2700", "Intel Core i5-9400",
            "AMD Ryzen 3 1200", "Intel Core i3-8100", "AMD Ryzen 9 5900X",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i7-10710U", "AMD Ryzen 7 2700E",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i9-10980HK", "AMD Ryzen 5 3600X",
            "Intel Core i7-10700F", "AMD Ryzen 7 2700", "Intel Core i5-9400",
            "AMD Ryzen 3 1200", "Intel Core i3-8100", "AMD Ryzen 9 5900X",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i7-10710U", "AMD Ryzen 7 2700E",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i9-10980HK", "AMD Ryzen 5 3600X",
            "Intel Core i7-10700F", "AMD Ryzen 7 2700", "Intel Core i5-9400",
            "AMD Ryzen 3 1200", "Intel Core i3-8100", "AMD Ryzen 9 5900X",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i7-10710U", "AMD Ryzen 7 2700E",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i9-10980HK", "AMD Ryzen 5 3600X",
            "Intel Core i7-10700F", "AMD Ryzen 7 2700", "Intel Core i5-9400",
            "AMD Ryzen 3 1200", "Intel Core i3-8100", "AMD Ryzen 9 5900X",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i7-10710U", "AMD Ryzen 7 2700E",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i9-10980HK", "AMD Ryzen 5 3600X",
            "Intel Core i7-10700F", "AMD Ryzen 7 2700", "Intel Core i5-9400",
            "AMD Ryzen 3 1200", "Intel Core i3-8100", "AMD Ryzen 9 5900X",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i7-10710U", "AMD Ryzen 7 2700E",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i9-10980HK", "AMD Ryzen 5 3600X",
            "Intel Core i7-10700F", "AMD Ryzen 7 2700", "Intel Core i5-9400",
            "AMD Ryzen 3 1200", "Intel Core i3-8100", "AMD Ryzen 9 5900X",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i7-10710U", "AMD Ryzen 7 2700E",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i9-10980HK", "AMD Ryzen 5 3600X",
            "Intel Core i7-10700F", "AMD Ryzen 7 2700", "Intel Core i5-9400",
            "AMD Ryzen 3 1200", "Intel Core i3-8100", "AMD Ryzen 9 5900X",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i7-10710U", "AMD Ryzen 7 2700E",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i9-10980HK", "AMD Ryzen 5 3600X",
            "Intel Core i7-10700F", "AMD Ryzen 7 2700", "Intel Core i5-9400",
            "AMD Ryzen 3 1200", "Intel Core i3-8100", "AMD Ryzen 9 5900X",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i7-10710U", "AMD Ryzen 7 2700E",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i9-10980HK", "AMD Ryzen 5 3600X",
            "Intel Core i7-10700F", "AMD Ryzen 7 2700", "Intel Core i5-9400",
            "AMD Ryzen 3 1200", "Intel Core i3-8100", "AMD Ryzen 9 5900X",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i7-10710U", "AMD Ryzen 7 2700E",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i9-10980HK", "AMD Ryzen 5 3600X",
            "Intel Core i7-10700F", "AMD Ryzen 7 2700", "Intel Core i5-9400",
            "AMD Ryzen 3 1200", "Intel Core i3-8100", "AMD Ryzen 9 5900X",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i7-10710U", "AMD Ryzen 7 2700E",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i9-10980HK", "AMD Ryzen 5 3600X",
            "Intel Core i7-10700F", "AMD Ryzen 7 2700", "Intel Core i5-9400",
            "AMD Ryzen 3 1200", "Intel Core i3-8100", "AMD Ryzen 9 5900X",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i7-10710U", "AMD Ryzen 7 2700E",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i9-10980HK", "AMD Ryzen 5 3600X",
            "Intel Core i7-10700F", "AMD Ryzen 7 2700", "Intel Core i5-9400",
            "AMD Ryzen 3 1200", "Intel Core i3-8100", "AMD Ryzen 9 5900X",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i7-10710U", "AMD Ryzen 7 2700E",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i9-10980HK", "AMD Ryzen 5 3600X",
            "Intel Core i7-10700F", "AMD Ryzen 7 2700", "Intel Core i5-9400",
            "AMD Ryzen 3 1200", "Intel Core i3-8100", "AMD Ryzen 9 5900X",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i7-10710U", "AMD Ryzen 7 2700E",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i9-10980HK", "AMD Ryzen 5 3600X",
            "Intel Core i7-10700F", "AMD Ryzen 7 2700", "Intel Core i5-9400",
            "AMD Ryzen 3 1200", "Intel Core i3-8100", "AMD Ryzen 9 5900X",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i7-10710U", "AMD Ryzen 7 2700E",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i9-10980HK", "AMD Ryzen 5 3600X",
            "Intel Core i7-10700F", "AMD Ryzen 7 2700", "Intel Core i5-9400",
            "AMD Ryzen 3 1200", "Intel Core i3-8100", "AMD Ryzen 9 5900X",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i7-10710U", "AMD Ryzen 7 2700E",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i9-10980HK", "AMD Ryzen 5 3600X",
            "Intel Core i7-10700F", "AMD Ryzen 7 2700", "Intel Core i5-9400",
            "AMD Ryzen 3 1200", "Intel Core i3-8100", "AMD Ryzen 9 5900X",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i7-10710U", "AMD Ryzen 7 2700E",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i9-10980HK", "AMD Ryzen 5 3600X",
            "Intel Core i7-10700F", "AMD Ryzen 7 2700", "Intel Core i5-9400",
            "AMD Ryzen 3 1200", "Intel Core i3-8100", "AMD Ryzen 9 5900X",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i7-10710U", "AMD Ryzen 7 2700E",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i9-10980HK", "AMD Ryzen 5 3600X",
            "Intel Core i7-10700F", "AMD Ryzen 7 2700", "Intel Core i5-9400",
            "AMD Ryzen 3 1200", "Intel Core i3-8100", "AMD Ryzen 9 5900X",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i7-10710U", "AMD Ryzen 7 2700E",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i9-10980HK", "AMD Ryzen 5 3600X",
            "Intel Core i7-10700F", "AMD Ryzen 7 2700", "Intel Core i5-9400",
            "AMD Ryzen 3 1200", "Intel Core i3-8100", "AMD Ryzen 9 5900X",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i7-10710U", "AMD Ryzen 7 2700E",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i9-10980HK", "AMD Ryzen 5 3600X",
            "Intel Core i7-10700F", "AMD Ryzen 7 2700", "Intel Core i5-9400",
            "AMD Ryzen 3 1200", "Intel Core i3-8100", "AMD Ryzen 9 5900X",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i7-10710U", "AMD Ryzen 7 2700E",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i9-10980HK", "AMD Ryzen 5 3600X",
            "Intel Core i7-10700F", "AMD Ryzen 7 2700", "Intel Core i5-9400",
            "AMD Ryzen 3 1200", "Intel Core i3-8100", "AMD Ryzen 9 5900X",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i7-10710U", "AMD Ryzen 7 2700E",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i9-10980HK", "AMD Ryzen 5 3600X",
            "Intel Core i7-10700F", "AMD Ryzen 7 2700", "Intel Core i5-9400",
            "AMD Ryzen 3 1200", "Intel Core i3-8100", "AMD Ryzen 9 5900X",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i7-10710U", "AMD Ryzen 7 2700E",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i9-10980HK", "AMD Ryzen 5 3600X",
            "Intel Core i7-10700F", "AMD Ryzen 7 2700", "Intel Core i5-9400",
            "AMD Ryzen 3 1200", "Intel Core i3-8100", "AMD Ryzen 9 5900X",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i7-10710U", "AMD Ryzen 7 2700E",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i9-10980HK", "AMD Ryzen 5 3600X",
            "Intel Core i7-10700F", "AMD Ryzen 7 2700", "Intel Core i5-9400",
            "AMD Ryzen 3 1200", "Intel Core i3-8100", "AMD Ryzen 9 5900X",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i7-10710U", "AMD Ryzen 7 2700E",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i9-10980HK", "AMD Ryzen 5 3600X",
            "Intel Core i7-10700F", "AMD Ryzen 7 2700", "Intel Core i5-9400",
            "AMD Ryzen 3 1200", "Intel Core i3-8100", "AMD Ryzen 9 5900X",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i7-10710U", "AMD Ryzen 7 2700E",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i9-10980HK", "AMD Ryzen 5 3600X",
            "Intel Core i7-10700F", "AMD Ryzen 7 2700", "Intel Core i5-9400",
            "AMD Ryzen 3 1200", "Intel Core i3-8100", "AMD Ryzen 9 5900X",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i7-10710U", "AMD Ryzen 7 2700E",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i9-10980HK", "AMD Ryzen 5 3600X",
            "Intel Core i7-10700F", "AMD Ryzen 7 2700", "Intel Core i5-9400",
            "AMD Ryzen 3 1200", "Intel Core i3-8100", "AMD Ryzen 9 5900X",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i7-10710U", "AMD Ryzen 7 2700E",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i9-10980HK", "AMD Ryzen 5 3600X",
            "Intel Core i7-10700F", "AMD Ryzen 7 2700", "Intel Core i5-9400",
            "AMD Ryzen 3 1200", "Intel Core i3-8100", "AMD Ryzen 9 5900X",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i7-10710U", "AMD Ryzen 7 2700E",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i9-10980HK", "AMD Ryzen 5 3600X",
            "Intel Core i7-10700F", "AMD Ryzen 7 2700", "Intel Core i5-9400",
            "AMD Ryzen 3 1200", "Intel Core i3-8100", "AMD Ryzen 9 5900X",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i7-10710U", "AMD Ryzen 7 2700E",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i9-10980HK", "AMD Ryzen 5 3600X",
            "Intel Core i7-10700F", "AMD Ryzen 7 2700", "Intel Core i5-9400",
            "AMD Ryzen 3 1200", "Intel Core i3-8100", "AMD Ryzen 9 5900X",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i7-10710U", "AMD Ryzen 7 2700E",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i9-10980HK", "AMD Ryzen 5 3600X",
            "Intel Core i7-10700F", "AMD Ryzen 7 2700", "Intel Core i5-9400",
            "AMD Ryzen 3 1200", "Intel Core i3-8100", "AMD Ryzen 9 5900X",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i7-10710U", "AMD Ryzen 7 2700E",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i9-10980HK", "AMD Ryzen 5 3600X",
            "Intel Core i7-10700F", "AMD Ryzen 7 2700", "Intel Core i5-9400",
            "AMD Ryzen 3 1200", "Intel Core i3-8100", "AMD Ryzen 9 5900X",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i7-10710U", "AMD Ryzen 7 2700E",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i9-10980HK", "AMD Ryzen 5 3600X",
            "Intel Core i7-10700F", "AMD Ryzen 7 2700", "Intel Core i5-9400",
            "AMD Ryzen 3 1200", "Intel Core i3-8100", "AMD Ryzen 9 5900X",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i7-10710U", "AMD Ryzen 7 2700E",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i9-10980HK", "AMD Ryzen 5 3600X",
            "Intel Core i7-10700F", "AMD Ryzen 7 2700", "Intel Core i5-9400",
            "AMD Ryzen 3 1200", "Intel Core i3-8100", "AMD Ryzen 9 5900X",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i7-10710U", "AMD Ryzen 7 2700E",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i9-10980HK", "AMD Ryzen 5 3600X",
            "Intel Core i7-10700F", "AMD Ryzen 7 2700", "Intel Core i5-9400",
            "AMD Ryzen 3 1200", "Intel Core i3-8100", "AMD Ryzen 9 5900X",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i7-10710U", "AMD Ryzen 7 2700E",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i9-10980HK", "AMD Ryzen 5 3600X",
            "Intel Core i7-10700F", "AMD Ryzen 7 2700", "Intel Core i5-9400",
            "AMD Ryzen 3 1200", "Intel Core i3-8100", "AMD Ryzen 9 5900X",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i7-10710U", "AMD Ryzen 7 2700E",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i9-10980HK", "AMD Ryzen 5 3600X",
            "Intel Core i7-10700F", "AMD Ryzen 7 2700", "Intel Core i5-9400",
            "AMD Ryzen 3 1200", "Intel Core i3-8100", "AMD Ryzen 9 5900X",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i7-10710U", "AMD Ryzen 7 2700E",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i9-10980HK", "AMD Ryzen 5 3600X",
            "Intel Core i7-10700F", "AMD Ryzen 7 2700", "Intel Core i5-9400",
            "AMD Ryzen 3 1200", "Intel Core i3-8100", "AMD Ryzen 9 5900X",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i7-10710U", "AMD Ryzen 7 2700E",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i9-10980HK", "AMD Ryzen 5 3600X",
            "Intel Core i7-10700F", "AMD Ryzen 7 2700", "Intel Core i5-9400",
            "AMD Ryzen 3 1200", "Intel Core i3-8100", "AMD Ryzen 9 5900X",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i7-10710U", "AMD Ryzen 7 2700E",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i9-10980HK", "AMD Ryzen 5 3600X",
            "Intel Core i7-10700F", "AMD Ryzen 7 2700", "Intel Core i5-9400",
            "AMD Ryzen 3 1200", "Intel Core i3-8100", "AMD Ryzen 9 5900X",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i7-10710U", "AMD Ryzen 7 2700E",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i9-10980HK", "AMD Ryzen 5 3600X",
            "Intel Core i7-10700F", "AMD Ryzen 7 2700", "Intel Core i5-9400",
            "AMD Ryzen 3 1200", "Intel Core i3-8100", "AMD Ryzen 9 5900X",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i7-10710U", "AMD Ryzen 7 2700E",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i9-10980HK", "AMD Ryzen 5 3600X",
            "Intel Core i7-10700F", "AMD Ryzen 7 2700", "Intel Core i5-9400",
            "AMD Ryzen 3 1200", "Intel Core i3-8100", "AMD Ryzen 9 5900X",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i7-10710U", "AMD Ryzen 7 2700E",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i9-10980HK", "AMD Ryzen 5 3600X",
            "Intel Core i7-10700F", "AMD Ryzen 7 2700", "Intel Core i5-9400",
            "AMD Ryzen 3 1200", "Intel Core i3-8100", "AMD Ryzen 9 5900X",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i7-10710U", "AMD Ryzen 7 2700E",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i9-10980HK", "AMD Ryzen 5 3600X",
            "Intel Core i7-10700F", "AMD Ryzen 7 2700", "Intel Core i5-9400",
            "AMD Ryzen 3 1200", "Intel Core i3-8100", "AMD Ryzen 9 5900X",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i7-10710U", "AMD Ryzen 7 2700E",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i9-10980HK", "AMD Ryzen 5 3600X",
            "Intel Core i7-10700F", "AMD Ryzen 7 2700", "Intel Core i5-9400",
            "AMD Ryzen 3 1200", "Intel Core i3-8100", "AMD Ryzen 9 5900X",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i7-10710U", "AMD Ryzen 7 2700E",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i9-10980HK", "AMD Ryzen 5 3600X",
            "Intel Core i7-10700F", "AMD Ryzen 7 2700", "Intel Core i5-9400",
            "AMD Ryzen 3 1200", "Intel Core i3-8100", "AMD Ryzen 9 5900X",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i7-10710U", "AMD Ryzen 7 2700E",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i9-10980HK", "AMD Ryzen 5 3600X",
            "Intel Core i7-10700F", "AMD Ryzen 7 2700", "Intel Core i5-9400",
            "AMD Ryzen 3 1200", "Intel Core i3-8100", "AMD Ryzen 9 5900X",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i7-10710U", "AMD Ryzen 7 2700E",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i9-10980HK", "AMD Ryzen 5 3600X",
            "Intel Core i7-10700F", "AMD Ryzen 7 2700", "Intel Core i5-9400",
            "AMD Ryzen 3 1200", "Intel Core i3-8100", "AMD Ryzen 9 5900X",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i7-10710U", "AMD Ryzen 7 2700E",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i9-10980HK", "AMD Ryzen 5 3600X",
            "Intel Core i7-10700F", "AMD Ryzen 7 2700", "Intel Core i5-9400",
            "AMD Ryzen 3 1200", "Intel Core i3-8100", "AMD Ryzen 9 5900X",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i7-10710U", "AMD Ryzen 7 2700E",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i9-10980HK", "AMD Ryzen 5 3600X",
            "Intel Core i7-10700F", "AMD Ryzen 7 2700", "Intel Core i5-9400",
            "AMD Ryzen 3 1200", "Intel Core i3-8100", "AMD Ryzen 9 5900X",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i7-10710U", "AMD Ryzen 7 2700E",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i9-10980HK", "AMD Ryzen 5 3600X",
            "Intel Core i7-10700F", "AMD Ryzen 7 2700", "Intel Core i5-9400",
            "AMD Ryzen 3 1200", "Intel Core i3-8100", "AMD Ryzen 9 5900X",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i7-10710U", "AMD Ryzen 7 2700E",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i9-10980HK", "AMD Ryzen 5 3600X",
            "Intel Core i7-10700F", "AMD Ryzen 7 2700", "Intel Core i5-9400",
            "AMD Ryzen 3 1200", "Intel Core i3-8100", "AMD Ryzen 9 5900X",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i7-10710U", "AMD Ryzen 7 2700E",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i9-10980HK", "AMD Ryzen 5 3600X",
            "Intel Core i7-10700F", "AMD Ryzen 7 2700", "Intel Core i5-9400",
            "AMD Ryzen 3 1200", "Intel Core i3-8100", "AMD Ryzen 9 5900X",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i7-10710U", "AMD Ryzen 7 2700E",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i9-10980HK", "AMD Ryzen 5 3600X",
            "Intel Core i7-10700F", "AMD Ryzen 7 2700", "Intel Core i5-9400",
            "AMD Ryzen 3 1200", "Intel Core i3-8100", "AMD Ryzen 9 5900X",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i7-10710U", "AMD Ryzen 7 2700E",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i9-10980HK", "AMD Ryzen 5 3600X",
            "Intel Core i7-10700F", "AMD Ryzen 7 2700", "Intel Core i5-9400",
            "AMD Ryzen 3 1200", "Intel Core i3-8100", "AMD Ryzen 9 5900X",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i7-10710U", "AMD Ryzen 7 2700E",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i9-10980HK", "AMD Ryzen 5 3600X",
            "Intel Core i7-10700F", "AMD Ryzen 7 2700", "Intel Core i5-9400",
            "AMD Ryzen 3 1200", "Intel Core i3-8100", "AMD Ryzen 9 5900X",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i7-10710U", "AMD Ryzen 7 2700E",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i9-10980HK", "AMD Ryzen 5 3600X",
            "Intel Core i7-10700F", "AMD Ryzen 7 2700", "Intel Core i5-9400",
            "AMD Ryzen 3 1200", "Intel Core i3-8100", "AMD Ryzen 9 5900X",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i7-10710U", "AMD Ryzen 7 2700E",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i9-10980HK", "AMD Ryzen 5 3600X",
            "Intel Core i7-10700F", "AMD Ryzen 7 2700", "Intel Core i5-9400",
            "AMD Ryzen 3 1200", "Intel Core i3-8100", "AMD Ryzen 9 5900X",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i7-10710U", "AMD Ryzen 7 2700E",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i9-10980HK", "AMD Ryzen 5 3600X",
            "Intel Core i7-10700F", "AMD Ryzen 7 2700", "Intel Core i5-9400",
            "AMD Ryzen 3 1200", "Intel Core i3-8100", "AMD Ryzen 9 5900X",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i7-10710U", "AMD Ryzen 7 2700E",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i9-10980HK", "AMD Ryzen 5 3600X",
            "Intel Core i7-10700F", "AMD Ryzen 7 2700", "Intel Core i5-9400",
            "AMD Ryzen 3 1200", "Intel Core i3-8100", "AMD Ryzen 9 5900X",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i7-10710U", "AMD Ryzen 7 2700E",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i9-10980HK", "AMD Ryzen 5 3600X",
            "Intel Core i7-10700F", "AMD Ryzen 7 2700", "Intel Core i5-9400",
            "AMD Ryzen 3 1200", "Intel Core i3-8100", "AMD Ryzen 9 5900X",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i7-10710U", "AMD Ryzen 7 2700E",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i9-10980HK", "AMD Ryzen 5 3600X",
            "Intel Core i7-10700F", "AMD Ryzen 7 2700", "Intel Core i5-9400",
            "AMD Ryzen 3 1200", "Intel Core i3-8100", "AMD Ryzen 9 5900X",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i7-10710U", "AMD Ryzen 7 2700E",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i9-10980HK", "AMD Ryzen 5 3600X",
            "Intel Core i7-10700F", "AMD Ryzen 7 2700", "Intel Core i5-9400",
            "AMD Ryzen 3 1200", "Intel Core i3-8100", "AMD Ryzen 9 5900X",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i7-10710U", "AMD Ryzen 7 2700E",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i9-10980HK", "AMD Ryzen 5 3600X",
            "Intel Core i7-10700F", "AMD Ryzen 7 2700", "Intel Core i5-9400",
            "AMD Ryzen 3 1200", "Intel Core i3-8100", "AMD Ryzen 9 5900X",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i7-10710U", "AMD Ryzen 7 2700E",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i9-10980HK", "AMD Ryzen 5 3600X",
            "Intel Core i7-10700F", "AMD Ryzen 7 2700", "Intel Core i5-9400",
            "AMD Ryzen 3 1200", "Intel Core i3-8100", "AMD Ryzen 9 5900X",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i7-10710U", "AMD Ryzen 7 2700E",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i9-10980HK", "AMD Ryzen 5 3600X",
            "Intel Core i7-10700F", "AMD Ryzen 7 2700", "Intel Core i5-9400",
            "AMD Ryzen 3 1200", "Intel Core i3-8100", "AMD Ryzen 9 5900X",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i7-10710U", "AMD Ryzen 7 2700E",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i9-10980HK", "AMD Ryzen 5 3600X",
            "Intel Core i7-10700F", "AMD Ryzen 7 2700", "Intel Core i5-9400",
            "AMD Ryzen 3 1200", "Intel Core i3-8100", "AMD Ryzen 9 5900X",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i7-10710U", "AMD Ryzen 7 2700E",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i9-10980HK", "AMD Ryzen 5 3600X",
            "Intel Core i7-10700F", "AMD Ryzen 7 2700", "Intel Core i5-9400",
            "AMD Ryzen 3 1200", "Intel Core i3-8100", "AMD Ryzen 9 5900X",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i7-10710U", "AMD Ryzen 7 2700E",
            "Intel Core i5-9500", "AMD Ryzen 5 3400G", "Intel Core i3-8300",
            "AMD Ryzen 3 1300X", "Intel Core i9-10980HK", "AMD Ryzen 5 3600X",
            "Intel Core i7-10700F", "AMD Ryzen 7 2700", "Intel Core i5-9400"
        ]

        all_features = [
            "mmx",
            "sse",
            "sse2",
            "sse3",
            "ssse3",
            "sse4_1",
            "sse4_2",
            "avx",
            "avx2",
            "fma3",
            "aes",
            "pclmulqdq"
        ]

        cpu_features = random.sample(all_features, k=random.randint(4, len(all_features)))
        
        return {
            "cpuArchitecture":"x86_64",
            "cpuModel":random.choice(cpu_models),
            "cpuFeatures": cpu_features,
            "numOfProcessors":len(cpu_features) * 2,
            "totalMemory":random.randint(8 * 1024**3, 64 * 1024**3)
        }
    
    def generate_payload(self, hardware_id: str, ip_address: str):
        return {
            "ipAddress":ip_address,
            "hardwareId":hardware_id,
            "hardwareInfo":self.generate_hardware_info(),
            "extensionVersion":"0.1.7"
        }
        
    def mask_account(self, account):
        mask_account = account[:3] + '*' * 3 + account[-3:]
        return mask_account

    def print_message(self, account, pub_key, proxy, color, message):
        proxy_value = proxy.get("http") if isinstance(proxy, dict) else proxy
        self.log(
            f"{Fore.CYAN + Style.BRIGHT}[ Account:{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} {self.mask_account(account)} {Style.RESET_ALL}"
            f"{Fore.MAGENTA + Style.BRIGHT}-{Style.RESET_ALL}"
            f"{Fore.CYAN + Style.BRIGHT} Node ID: {Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT}{self.mask_account(pub_key)}{Style.RESET_ALL}"
            f"{Fore.MAGENTA + Style.BRIGHT} - {Style.RESET_ALL}"
            f"{Fore.CYAN + Style.BRIGHT}Proxy:{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} {proxy_value} {Style.RESET_ALL}"
            f"{Fore.MAGENTA + Style.BRIGHT}-{Style.RESET_ALL}"
            f"{Fore.CYAN + Style.BRIGHT} Status: {Style.RESET_ALL}"
            f"{color + Style.BRIGHT}{message}{Style.RESET_ALL}"
            f"{Fore.CYAN + Style.BRIGHT} ]{Style.RESET_ALL}"
        )

    def print_question(self):
        while True:
            try:
                print("1. Run With Monosans Proxy")
                print("2. Run With Private Proxy")
                print("3. Run Without Proxy")
                choose = int(input("Choose [1/2/3] -> ").strip())

                if choose in [1, 2, 3]:
                    proxy_type = (
                        "Run With Monosans Proxy" if choose == 1 else 
                        "Run With Private Proxy" if choose == 2 else 
                        "Run Without Proxy"
                    )
                    print(f"{Fore.GREEN + Style.BRIGHT}{proxy_type} Selected.{Style.RESET_ALL}")
                    return choose
                else:
                    print(f"{Fore.RED + Style.BRIGHT}Please enter either 1, 2 or 3.{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED + Style.BRIGHT}Invalid input. Enter a number (1, 2 or 3).{Style.RESET_ALL}")

    async def check_ip_address(self, token: str, pub_key: str, proxy=None, retries=5):
        url = "https://ip-check.bless.network/"
        for attempt in range(retries):
            try:
                response = await asyncio.to_thread(self.scraper.get, url=url, headers=self.headers, proxies=proxy, timeout=60)
                response.raise_for_status()
                result = response.json()
                return result['ip']
            except Exception as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue

                return self.print_message(token, pub_key, proxy, Fore.RED, f"GET IP Address Failed: {Fore.YELLOW+Style.BRIGHT}{str(e)}")
    
    async def node_status(self, token: str, pub_key: str, proxy=None, retries=5):
        url = f"https://gateway-run.bls.dev/api/v1/nodes/{pub_key}"
        headers = {
            **self.headers,
            "Authorization": f"Bearer {token}",
            "X-Extension-Version": "0.1.7",
        }
        for attempt in range(retries):
            try:
                response = await asyncio.to_thread(self.scraper.get, url=url, headers=headers, proxies=proxy, timeout=60)
                response.raise_for_status()
                return response.json()
            except Exception as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue

                return self.print_message(token, pub_key, proxy, Fore.RED, f"GET Node Status Failed: {Fore.YELLOW+Style.BRIGHT}{str(e)}")
    
    async def register_node(self, token: str, pub_key: str, hardware_id: str, ip_address: str, proxy=None, retries=5):
        url = f"https://gateway-run.bls.dev/api/v1/nodes/{pub_key}"
        data = json.dumps(self.generate_payload(hardware_id, ip_address))
        headers = {
            **self.headers,
            "Authorization": f"Bearer {token}",
            "Content-Length": str(len(data)),
            "Content-Type": "application/json",
            "X-Extension-Version": "0.1.7",
        }
        for attempt in range(retries):
            try:
                response = await asyncio.to_thread(self.scraper.post, url=url, headers=headers, data=data, proxies=proxy, timeout=60)
                response.raise_for_status()
                return response.json()
            except Exception as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue

                return self.print_message(token, pub_key, proxy, Fore.RED, f"Registering Node Failed: {Fore.YELLOW+Style.BRIGHT}{str(e)}")
    
    async def start_session(self, token: str, pub_key: str, proxy=None, retries=5):
        url = f"https://gateway-run.bls.dev/api/v1/nodes/{pub_key}/start-session"
        headers = {
            **self.headers,
            "Authorization": f"Bearer {token}",
            "Content-Length": "2",
            "Content-Type": "application/json",
            "X-Extension-Version": "0.1.7",
        }
        for attempt in range(retries):
            try:
                response = await asyncio.to_thread(self.scraper.post, url=url, headers=headers, json={}, proxies=proxy, timeout=60)
                response.raise_for_status()
                return response.json()
            except Exception as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue

                return self.print_message(token, pub_key, proxy, Fore.RED, f"Start Session Failed: {Fore.YELLOW+Style.BRIGHT}{str(e)}")
    
    async def send_ping(self, token: str, pub_key: str, proxy=None, retries=5):
        url = f"https://gateway-run.bls.dev/api/v1/nodes/{pub_key}/ping"
        data = json.dumps({"isB7SConnected":True})
        headers = {
            **self.headers,
            "Authorization": f"Bearer {token}",
            "Content-Length": str(len(data)),
            "Content-Type": "application/json",
            "X-Extension-Version": "0.1.7",
        }
        for attempt in range(retries):
            try:
                response = await asyncio.to_thread(self.scraper.post, url=url, headers=headers, data=data, proxies=proxy, timeout=60)
                response.raise_for_status()
                return response.json()
            except Exception as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue

                return self.print_message(token, pub_key, proxy, Fore.RED, f"PING Failed: {Fore.YELLOW+Style.BRIGHT}{str(e)}")
            
    async def process_check_ip_address(self, token: str, pub_key: str, use_proxy: bool):
        proxy = self.get_next_proxy_for_account(pub_key) if use_proxy else None
        ip_address = None
        while ip_address is None:
            ip_address = await self.check_ip_address(token, pub_key, proxy)
            if not ip_address:
                proxy = self.rotate_proxy_for_account(pub_key) if use_proxy else None
                await asyncio.sleep(5)
                continue

            self.print_message(token, pub_key, proxy, Fore.GREEN, f"IP Address: {Fore.WHITE+Style.BRIGHT}{ip_address}")
            return ip_address
        
    async def process_registering_node(self, token: str, pub_key: str, hardware_id: str, use_proxy: bool):
        ip_address = await self.process_check_ip_address(token, pub_key, use_proxy)
        if ip_address:
            proxy = self.get_next_proxy_for_account(pub_key) if use_proxy else None
            node = None
            while node is None:
                node = await self.register_node(token, pub_key, hardware_id, ip_address, proxy)
                if not node:
                    ip_address = await self.process_check_ip_address(token, pub_key, use_proxy)
                    proxy = self.rotate_proxy_for_account(pub_key) if use_proxy else None
                    await asyncio.sleep(5)
                    continue

                self.print_message(token, pub_key, proxy, Fore.GREEN, f"Registering Node Success")
                return node
        
    async def process_start_session(self, token, pub_key: str, hardware_id: str, use_proxy: bool):
        node = await self.process_registering_node(token, pub_key, hardware_id, use_proxy)
        if node:
            proxy = self.get_next_proxy_for_account(pub_key) if use_proxy else None
            session = None
            while session is None:
                session = await self.start_session(token, pub_key, proxy)
                if not session:
                    node = await self.process_registering_node(token, pub_key, hardware_id, use_proxy)
                    await asyncio.sleep(5)
                    continue
                
                self.print_message(token, pub_key, proxy, Fore.GREEN, f"Start Session Success")
                
                tasks = []
                tasks.append(asyncio.create_task(self.process_get_node_earning(token, pub_key, use_proxy)))
                tasks.append(asyncio.create_task(self.process_send_ping(token, pub_key, use_proxy)))
                await asyncio.gather(*tasks)
        
    async def process_get_node_earning(self, token, pub_key: str, use_proxy: bool):
        while True:
            proxy = self.get_next_proxy_for_account(pub_key) if use_proxy else None

            today_reward = "N/A"
            total_reward = "N/A"

            node = await self.node_status(token, pub_key, proxy)
            if node:
                today_reward = node.get("todayReward")
                total_reward = node.get("totalReward")

            self.print_message(token, pub_key, proxy, Fore.WHITE, 
                f"Earning Today: {today_reward} Minutes"
                f"{Fore.MAGENTA + Style.BRIGHT} - {Style.RESET_ALL}"
                f"{Fore.WHITE + Style.BRIGHT}Earning Total: {total_reward} Minutes{Style.RESET_ALL}"
            )

            await asyncio.sleep(15 * 60)
        
    async def process_send_ping(self, token, pub_key: str, use_proxy: bool):
        while True:
            proxy = self.get_next_proxy_for_account(pub_key) if use_proxy else None
            print(
                f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
                f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                f"{Fore.BLUE + Style.BRIGHT}Try to Sent Ping...{Style.RESET_ALL}                                         ",
                end="\r",
                flush=True
            )

            ping = await self.send_ping(token, pub_key, proxy)
            if ping:
                self.print_message(token, pub_key, proxy, Fore.GREEN, f"PING Success")

            print(
                f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
                f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                f"{Fore.BLUE + Style.BRIGHT}Wait For 10 Minutes For Next Ping...{Style.RESET_ALL}",
                end="\r"
            )
               
            await asyncio.sleep(10 * 60)

    async def process_accounts(self, token: str, nodes: list, use_proxy: bool):
        tasks = []
        for node in nodes:
            pub_key = node.get('PubKey')
            hardware_id = node.get('HardwareId')

            if pub_key and hardware_id:
                tasks.append(asyncio.create_task(self.process_start_session(token, pub_key, hardware_id, use_proxy)))

        await asyncio.gather(*tasks)

    async def main(self):
        try:
            accounts = self.load_accounts()
            if not accounts:
                self.log(f"{Fore.RED}No Accounts Loaded.{Style.RESET_ALL}")
                return

            use_proxy_choice = self.print_question()

            use_proxy = False
            if use_proxy_choice in [1, 2]:
                use_proxy = True

            self.clear_terminal()
            self.welcome()
            self.log(
                f"{Fore.GREEN + Style.BRIGHT}Account's Total: {Style.RESET_ALL}"
                f"{Fore.WHITE + Style.BRIGHT}{len(accounts)}{Style.RESET_ALL}"
            )

            if use_proxy:
                await self.load_proxies(use_proxy_choice)

            self.log(f"{Fore.CYAN + Style.BRIGHT}-{Style.RESET_ALL}"*75)

            while True:
                tasks = []
                for account in accounts:
                    if account:
                        token = account.get('Token')
                        nodes = account.get('Nodes', [])

                    if token and nodes:
                        tasks.append(asyncio.create_task(self.process_accounts(token, nodes, use_proxy)))

                await asyncio.gather(*tasks)
                await asyncio.sleep(10)

        except Exception as e:
            self.log(f"{Fore.RED+Style.BRIGHT}Error: {e}{Style.RESET_ALL}")

if __name__ == "__main__":
    try:
        bot = Bless()
        asyncio.run(bot.main())
    except KeyboardInterrupt:
        print(
            f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
            f"{Fore.RED + Style.BRIGHT}[ EXIT ] Bless - BOT{Style.RESET_ALL}                                       "                              
        )