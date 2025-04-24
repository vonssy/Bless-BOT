from curl_cffi import requests
from fake_useragent import FakeUserAgent
from datetime import datetime
from colorama import *
import asyncio, json, base64, hashlib, string, random, os, pytz

wib = pytz.timezone('Asia/Jakarta')

class Bless:
    def __init__(self) -> None:
        self.headers = {
            "Accept": "*/*",
            "Accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "Origin": "chrome-extension://pljbjcehnhcnofmkdbjolghdcjnmekia",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "cross-site",
            "User-Agent": FakeUserAgent().random
        }
        self.BASE_API = "https://gateway-run.bls.dev/api/v1"
        self.IP_URL = "https://ip-check.bless.network/"
        self.EXTENSION_VERSION = "0.1.8"
        self.EXTENSION_SIGNATURES = {}
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
    
    def load_accounts(self):
        filename = "accounts.json"
        try:
            if not os.path.exists(filename):
                self.log(f"{Fore.RED}File {filename} Not Found.{Style.RESET_ALL}")
                return

            with open(filename, 'r') as file:
                data = json.load(file)
                if isinstance(data, list):
                    return data
                return []
        except json.JSONDecodeError:
            return []
    
    async def load_proxies(self, use_proxy_choice: int):
        filename = "proxy.txt"
        try:
            if use_proxy_choice == 1:
                response = await asyncio.to_thread(requests.get, "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/all.txt")
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
            return proxies
        return f"http://{proxies}"

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
    
    def decode_token(self, token: str):
        try:
            header, payload, signature = token.split(".")
            decoded_payload = base64.urlsafe_b64decode(payload + "==").decode("utf-8")
            parsed_payload = json.loads(decoded_payload)
            address = parsed_payload["publicAddress"]
            
            return address
        except Exception as e:
            return None

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
    
    def generate_hardware_id(self):
        hardware_id = ''.join(random.choices(string.hexdigits.lower(), k=64))
        return hardware_id
    
    def generate_payload(self, hardware_id: str, ip_address: str):
        return {
            "ipAddress":ip_address,
            "hardwareId":hardware_id,
            "hardwareInfo":self.generate_hardware_info(),
            "extensionVersion":self.EXTENSION_VERSION
        }
    
    def generate_extension_signature(self):
        random_data = os.urandom(32)
        hash_object = hashlib.sha512(random_data)
        return hash_object.hexdigest()
        
    def mask_account(self, account):
        mask_account = account[:6] + '*' * 6 + account[-6:]
        return mask_account

    def print_message(self, account, pub_key, proxy, color, message):
        self.log(
            f"{Fore.CYAN + Style.BRIGHT}[ Account:{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} {self.mask_account(account)} {Style.RESET_ALL}"
            f"{Fore.MAGENTA + Style.BRIGHT}-{Style.RESET_ALL}"
            f"{Fore.CYAN + Style.BRIGHT} Pub Key: {Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT}{self.mask_account(pub_key)}{Style.RESET_ALL}"
            f"{Fore.MAGENTA + Style.BRIGHT} - {Style.RESET_ALL}"
            f"{Fore.CYAN + Style.BRIGHT}Proxy:{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} {proxy} {Style.RESET_ALL}"
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

    async def check_ip_address(self, pub_key: str, address: str, proxy=None, retries=5):
        for attempt in range(retries):
            try:
                response = await asyncio.to_thread(requests.get, url=self.IP_URL, headers=self.headers, proxy=proxy, timeout=60, impersonate="chrome110")
                response.raise_for_status()
                return response.json()
            except Exception as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                return self.print_message(address, pub_key, proxy, Fore.RED, f"GET IP Address Failed: {Fore.YELLOW+Style.BRIGHT}{str(e)}")
    
    async def node_uptime(self, token: str, pub_key: str, address: str, proxy=None, retries=5):
        url = f"{self.BASE_API}/nodes/{pub_key}"
        headers = {
            **self.headers,
            "Authorization": f"Bearer {token}"
        }
        for attempt in range(retries):
            try:
                response = await asyncio.to_thread(requests.get, url=url, headers=headers, proxy=proxy, timeout=60, impersonate="chrome110")
                response.raise_for_status()
                return response.json()
            except Exception as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                return self.print_message(address, pub_key, proxy, Fore.RED, f"GET Node Uptime Failed: {Fore.YELLOW+Style.BRIGHT}{str(e)}")
    
    async def registering_node(self, token: str, pub_key: str, address: str, hardware_id: str, ip_address: str, proxy=None, retries=5):
        url = f"{self.BASE_API}/nodes/{pub_key}"
        data = json.dumps(self.generate_payload(hardware_id, ip_address))
        headers = {
            **self.headers,
            "Authorization": f"Bearer {token}",
            "Content-Length": str(len(data)),
            "Content-Type": "application/json",
            "X-Extension-Signature": self.EXTENSION_SIGNATURES[pub_key],
            "X-Extension-Version": self.EXTENSION_VERSION
        }
        for attempt in range(retries):
            try:
                response = await asyncio.to_thread(requests.post, url=url, headers=headers, data=data, proxy=proxy, timeout=60, impersonate="chrome110")
                response.raise_for_status()
                return response.json()
            except Exception as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                return self.print_message(address, pub_key, proxy, Fore.RED, f"Registering Node Failed: {Fore.YELLOW+Style.BRIGHT}{str(e)}")
    
    async def start_session(self, token: str, pub_key: str, address: str, proxy=None, retries=5):
        url = f"{self.BASE_API}/nodes/{pub_key}/start-session"
        headers = {
            **self.headers,
            "Authorization": f"Bearer {token}",
            "Content-Length": "2",
            "Content-Type": "application/json",
            "X-Extension-Signature": self.EXTENSION_SIGNATURES[pub_key],
            "X-Extension-Version": self.EXTENSION_VERSION
        }
        for attempt in range(retries):
            try:
                response = await asyncio.to_thread(requests.post, url=url, headers=headers, json={}, proxy=proxy, timeout=60, impersonate="chrome110")
                response.raise_for_status()
                return response.json()
            except Exception as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                return self.print_message(address, pub_key, proxy, Fore.RED, f"Node Not Connected: {Fore.YELLOW+Style.BRIGHT}{str(e)}")
    
    async def send_ping(self, token: str, pub_key: str, address: str, use_proxy: bool, proxy=None, retries=5):
        url = f"{self.BASE_API}/nodes/{pub_key}/ping"
        data = json.dumps({"isB7SConnected":True})
        headers = {
            **self.headers,
            "Authorization": f"Bearer {token}",
            "Content-Length": str(len(data)),
            "Content-Type": "application/json",
            "X-Extension-Signature": self.EXTENSION_SIGNATURES[pub_key],
            "X-Extension-Version": self.EXTENSION_VERSION
        }
        for attempt in range(retries):
            try:
                response = await asyncio.to_thread(requests.post, url=url, headers=headers, data=data, proxy=proxy, timeout=60, impersonate="chrome110")
                response.raise_for_status()
                return response.json()
            except Exception as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                self.print_message(address, pub_key, proxy, Fore.RED, f"PING Failed: {Fore.YELLOW+Style.BRIGHT}{str(e)}")
                if not any(code in str(e) for code in ["500", "501", "502", "503", "504"]):
                    proxy = self.rotate_proxy_for_account(pub_key) if use_proxy else None
                return None
        
    async def process_get_node_uptime(self, token: str, pub_key: str, address: str, use_proxy: bool):
        while True:
            proxy = self.get_next_proxy_for_account(pub_key) if use_proxy else None

            today_reward = "N/A"
            total_reward = "N/A"

            node = await self.node_uptime(token, pub_key, address, proxy)
            if node:
                today_reward = node.get("todayReward")
                total_reward = node.get("totalReward")

            self.print_message(address, pub_key, proxy, Fore.GREEN, "Uptime Updated"
                f"{Fore.MAGENTA + Style.BRIGHT} - {Style.RESET_ALL}"
                f"{Fore.CYAN + Style.BRIGHT}Uptime Today:{Style.RESET_ALL}"
                f"{Fore.WHITE + Style.BRIGHT} {today_reward} Minutes {Style.RESET_ALL}"
                f"{Fore.MAGENTA + Style.BRIGHT}-{Style.RESET_ALL}"
                f"{Fore.CYAN + Style.BRIGHT} Uptime Total: {Style.RESET_ALL}"
                f"{Fore.WHITE + Style.BRIGHT}{total_reward} Minutes{Style.RESET_ALL}"
            )

            await asyncio.sleep(30 * 60)

    async def process_send_ping(self, token: str, pub_key: str, address: str, use_proxy: bool):
        while True:
            proxy = self.get_next_proxy_for_account(pub_key) if use_proxy else None

            print(
                f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
                f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                f"{Fore.BLUE + Style.BRIGHT}Try to Sent Ping...{Style.RESET_ALL}                                         ",
                end="\r",
                flush=True
            )

            ping = await self.send_ping(token, pub_key, address, proxy)
            if ping:
                self.print_message(address, pub_key, proxy, Fore.GREEN, "PING Success")

            self.EXTENSION_SIGNATURES[pub_key] = self.generate_extension_signature()

            print(
                f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
                f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                f"{Fore.BLUE + Style.BRIGHT}Wait For 10 Minutes For Next Ping...{Style.RESET_ALL}",
                end="\r"
            )
               
            await asyncio.sleep(10 * 60)

    async def process_check_ip_address(self, pub_key: str, address: str, use_proxy: bool):
        proxy = self.get_next_proxy_for_account(pub_key) if use_proxy else None

        checked = None
        while checked is None:
            checked = await self.check_ip_address(pub_key, address, proxy)
            if not checked:
                proxy = self.rotate_proxy_for_account(pub_key) if use_proxy else None
                await asyncio.sleep(5)
                continue

            ip_address = checked.get("ip")

            self.print_message(address, pub_key, proxy, Fore.GREEN, "Checking IP Address Success "
                f"{Fore.MAGENTA+Style.BRIGHT}-{Style.RESET_ALL}"
                f"{Fore.CYAN+Style.BRIGHT} IP: {Style.RESET_ALL}"
                f"{Fore.WHITE+Style.BRIGHT}{ip_address}{Style.RESET_ALL}"
            )

            return ip_address
        
    async def process_registering_node(self, token: str, pub_key: str, address: str, hardware_id: str, use_proxy: bool):
        ip_address = await self.process_check_ip_address(pub_key, address, use_proxy)
        if ip_address:
            proxy = self.get_next_proxy_for_account(pub_key) if use_proxy else None

            registered = None
            while registered is None:
                registered = await self.registering_node(token, pub_key, address, hardware_id, ip_address, proxy)
                if not registered:
                    ip_address = await self.process_check_ip_address(token, pub_key, use_proxy)
                    proxy = self.rotate_proxy_for_account(pub_key) if use_proxy else None
                    await asyncio.sleep(5)
                    continue

                self.print_message(address, pub_key, proxy, Fore.GREEN, "Registering Node Success")

                return True
            
    async def process_start_session(self, token: str, pub_key: str, address: str, hardware_id: str, use_proxy: bool):
        is_registered = await self.process_registering_node(token, pub_key, address, hardware_id, use_proxy)
        if is_registered:
            proxy = self.get_next_proxy_for_account(pub_key) if use_proxy else None

            connected = None
            while connected is None:
                connected = await self.start_session(token, pub_key, proxy)
                if not connected:
                    await self.process_registering_node(token, pub_key, address, hardware_id, use_proxy)
                    await asyncio.sleep(5)
                    continue
                
                self.print_message(address, pub_key, proxy, Fore.GREEN, f"Node Connected")

                tasks = [
                    asyncio.create_task(self.process_get_node_uptime(token, pub_key, address, use_proxy)),
                    asyncio.create_task(self.process_send_ping(token, pub_key, address, use_proxy))
                ]

                await asyncio.gather(*tasks)
                
    async def process_accounts(self, token: str, pub_keys: dict, address: str, use_proxy: bool):
        tasks = []
        for pub_key in pub_keys:
            if pub_key:
                hardware_id = self.generate_hardware_id()
                self.EXTENSION_SIGNATURES[pub_key] = self.generate_extension_signature()

                tasks.append(asyncio.create_task(self.process_start_session(token, pub_key, address, hardware_id, use_proxy)))

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
                        token = account.get("Token")
                        pub_keys = account.get("PubKeys", [])

                        if token and pub_keys:
                            address = self.decode_token(token)

                            if address:
                                tasks.append(asyncio.create_task(self.process_accounts(token, pub_keys, address, use_proxy)))

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