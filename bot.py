from curl_cffi import requests
from datetime import datetime
from colorama import *
import asyncio, json, base64, hashlib, random, os, pytz

wib = pytz.timezone('Asia/Jakarta')

USER_AGENT = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.91 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.5672.127 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.5615.138 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.5563.65 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.5481.178 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_4_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.133 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_6_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.5672.93 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:115.0) Gecko/20100101 Firefox/115.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:114.0) Gecko/20100101 Firefox/114.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:113.0) Gecko/20100101 Firefox/113.0",
    "Mozilla/5.0 (Windows NT 10.0; rv:102.0) Gecko/20100101 Firefox/102.0",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:115.0) Gecko/20100101 Firefox/115.0",
    "Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:113.0) Gecko/20100101 Firefox/113.0",
    "Mozilla/5.0 (X11; Arch Linux; Linux x86_64; rv:112.0) Gecko/20100101 Firefox/112.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.5672.127 Safari/537.36 Edg/113.0.1774.35",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.5615.121 Safari/537.36 Edg/112.0.1722.64",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.5563.64 Safari/537.36 Edg/111.0.1661.54",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.5615.137 Safari/537.36 Edg/112.0.1722.68",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_4_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5.1 Safari/605.1.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_6_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.2 Safari/605.1.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_7_2) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.6 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.91 Safari/537.36 OPR/99.0.4788.77",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.5672.127 Safari/537.36 OPR/98.0.4759.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.91 Safari/537.36 Brave/1.52.129",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.5672.126 Safari/537.36 Brave/1.51.110",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.91 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.5672.127 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.91 Safari/537.36 Vivaldi/6.1.3035.100",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.5672.126 Safari/537.36 Vivaldi/6.0.2979.22",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chromium/114.0.5735.91 Safari/537.36"
]

class Bless:
    def __init__(self) -> None:
        self.BASE_API = "https://gateway-run.bls.dev/api/v1"
        self.HEADERS = {}
        self.proxies = []
        self.proxy_index = 0
        self.account_proxies = {}
        self.auth_tokens = {}
        self.ip_address = {}
        self.signatures = {}

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
        {Fore.GREEN + Style.BRIGHT}Bless Network {Fore.BLUE + Style.BRIGHT}Auto BOT
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
                response = await asyncio.to_thread(requests.get, "https://raw.githubusercontent.com/monosans/proxy-list/refs/heads/main/proxies/http.txt")
                response.raise_for_status()
                content = response.text
                with open(filename, 'w') as f:
                    f.write(content)
                self.proxies = [line.strip() for line in content.splitlines() if line.strip()]
            else:
                if not os.path.exists(filename):
                    self.log(f"{Fore.RED + Style.BRIGHT}File {filename} Not Found.{Style.RESET_ALL}")
                    return
                with open(filename, 'r') as f:
                    self.proxies = [line.strip() for line in f.read().splitlines() if line.strip()]
            
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
    
    def decode_auth_token(self, token: str):
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
            { "model": "AMD Ryzen 9 5950X", "cores": 16 },
            { "model": "AMD Ryzen 9 7900X", "cores": 12 },
            { "model": "AMD Ryzen 9 7950X", "cores": 16 },
            { "model": "AMD Ryzen 9 5900X", "cores": 12 },
            { "model": "AMD Ryzen 7 7800X3D", "cores": 8 },
            { "model": "AMD Ryzen Threadripper 3970X", "cores": 32 },
            { "model": "AMD Ryzen Threadripper PRO 3995WX", "cores": 64 },
            { "model": "Intel Core i9-13900K", "cores": 24 },
            { "model": "Intel Core i9-12900K", "cores": 16 },
            { "model": "Intel Core i9-11900K", "cores": 8 },
            { "model": "Intel Core i7-13700K", "cores": 16 },
            { "model": "Intel Core i7-12700K", "cores": 12 },
            { "model": "Intel Core i9-10980XE", "cores": 18 },
            { "model": "Intel Xeon W-2295", "cores": 18 },
            { "model": "Intel Xeon W-3275", "cores": 28 },
            { "model": "Intel Xeon Gold 6248", "cores": 20 }
        ]

        cpu = random.choice(cpu_models)

        cpu_features = [
            "mmx", "sse", "sse2", "sse3", "ssse3",
            "sse4_1", "sse4_2", "avx", "avx2",
            "fma3", "aes", "pclmulqdq"
        ]

        total_memory_gb = random.choice([32, 64, 128, 256])
        total_memory_bytes = total_memory_gb * 1024**3
        
        return {
            "cpuArchitecture": "x86_64",
            "cpuModel": cpu["model"],
            "cpuFeatures": cpu_features,
            "numOfProcessors": cpu["cores"],
            "totalMemory": total_memory_bytes
        }
    
    def generate_payload(self, pubkey: str, hardware_id: str):
        return {
            "ipAddress": self.ip_address[pubkey],
            "hardwareId": hardware_id,
            "hardwareInfo": self.generate_hardware_info(),
            "extensionVersion": "0.1.8"
        }
    
    def generate_signature(self):
        random_data = os.urandom(32)
        hash_object = hashlib.sha512(random_data)
        return hash_object.hexdigest()
        
    def mask_account(self, account):
        try:
            mask_account = account[:6] + '*' * 6 + account[-6:]
            return mask_account
        except Exception as e:
            return None

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
                print(f"{Fore.WHITE + Style.BRIGHT}1. Run With Free Proxyscrape Proxy{Style.RESET_ALL}")
                print(f"{Fore.WHITE + Style.BRIGHT}2. Run With Private Proxy{Style.RESET_ALL}")
                print(f"{Fore.WHITE + Style.BRIGHT}3. Run Without Proxy{Style.RESET_ALL}")
                choose = int(input(f"{Fore.BLUE + Style.BRIGHT}Choose [1/2/3] -> {Style.RESET_ALL}").strip())

                if choose in [1, 2, 3]:
                    proxy_type = (
                        "With Free Proxyscrape" if choose == 1 else 
                        "With Private" if choose == 2 else 
                        "Without"
                    )
                    print(f"{Fore.GREEN + Style.BRIGHT}Run {proxy_type} Proxy Selected.{Style.RESET_ALL}")
                    break
                else:
                    print(f"{Fore.RED + Style.BRIGHT}Please enter either 1, 2 or 3.{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED + Style.BRIGHT}Invalid input. Enter a number (1, 2 or 3).{Style.RESET_ALL}")

        rotate = False
        if choose in [1, 2]:
            while True:
                rotate = input(f"{Fore.BLUE + Style.BRIGHT}Rotate Invalid Proxy? [y/n] -> {Style.RESET_ALL}").strip()

                if rotate in ["y", "n"]:
                    rotate = rotate == "y"
                    break
                else:
                    print(f"{Fore.RED + Style.BRIGHT}Invalid input. Enter 'y' or 'n'.{Style.RESET_ALL}")

        return choose, rotate
    
    async def check_connection(self, address: str, pubkey: str, proxy=None):
        url = "https://ip-check.bless.network/"
        proxies = {"http":proxy, "https":proxy} if proxy else None
        try:
            response = await asyncio.to_thread(requests.get, url=url, headers=self.HEADERS[pubkey], proxies=proxies, timeout=60, impersonate="chrome110")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            self.print_message(address, pubkey, proxy, Fore.RED, f"Connection Not 200 OK: {Fore.YELLOW+Style.BRIGHT}{str(e)}")
            return None
        
    async def node_uptime(self, address: str, pubkey: str, proxy=None):
        url = f"{self.BASE_API}/nodes/{pubkey}"
        headers = {
            **self.HEADERS[pubkey],
            "Authorization": f"Bearer {self.auth_tokens[address]}"
        }
        proxies = {"http":proxy, "https":proxy} if proxy else None
        try:
            response = await asyncio.to_thread(requests.get, url=url, headers=headers, proxies=proxies, timeout=60, impersonate="chrome110")
            if response.status_code == 429:
                self.print_message(address, pubkey, proxy, Fore.RED, f"GET Node Uptime Failed: {Fore.YELLOW+Style.BRIGHT}Too Many Request, Retrying in 1 Minutes...")
                await asyncio.sleep(60)
                return None

            response.raise_for_status()
            return response.json()
        except Exception as e:
            self.print_message(address, pubkey, proxy, Fore.RED, f"GET Node Uptime Failed: {Fore.YELLOW+Style.BRIGHT}{str(e)}")
            return None
    
    async def register_node(self, address: str, pubkey: str, hardware_id: str, proxy=None):
        url = f"{self.BASE_API}/nodes/{pubkey}"
        data = json.dumps(self.generate_payload(pubkey, hardware_id))
        headers = {
            **self.HEADERS[pubkey],
            "Authorization": f"Bearer {self.auth_tokens[address]}",
            "Content-Length": str(len(data)),
            "Content-Type": "application/json",
            "X-Extension-Signature": self.signatures[pubkey],
            "X-Extension-Version": "0.1.8"
        }
        proxies = {"http":proxy, "https":proxy} if proxy else None
        try:
            response = await asyncio.to_thread(requests.post, url=url, headers=headers, data=data, proxies=proxies, timeout=60, impersonate="chrome110")
            if response.status_code == 429:
                self.signatures[pubkey] = self.generate_signature()
                self.print_message(address, pubkey, proxy, Fore.RED, f"Registering Node Failed: {Fore.YELLOW+Style.BRIGHT}Too Many Request, Retrying in 1 Minutes...")
                await asyncio.sleep(60)
                return None

            response.raise_for_status()
            return response.json()
        except Exception as e:
            self.print_message(address, pubkey, proxy, Fore.RED, f"Registering Node Failed: {Fore.YELLOW+Style.BRIGHT}{str(e)}")
            return None
    
    async def start_session(self, address: str, pubkey: str, proxy=None):
        url = f"{self.BASE_API}/nodes/{pubkey}/start-session"
        headers = {
            **self.HEADERS[pubkey],
            "Authorization": f"Bearer {self.auth_tokens[address]}",
            "Content-Length": "2",
            "Content-Type": "application/json",
            "X-Extension-Signature": self.signatures[pubkey],
            "X-Extension-Version": "0.1.8"
        }
        proxies = {"http":proxy, "https":proxy} if proxy else None
        try:
            response = await asyncio.to_thread(requests.post, url=url, headers=headers, json={}, proxies=proxies, timeout=60, impersonate="chrome110")
            if response.status_code == 429:
                self.signatures[pubkey] = self.generate_signature()
                self.print_message(address, pubkey, proxy, Fore.RED, f"Starting Session Failed: {Fore.YELLOW+Style.BRIGHT}Too Many Request, Retrying in 1 Minutes...")
                await asyncio.sleep(60)
                return None

            response.raise_for_status()
            return response.json()
        except Exception as e:
            self.print_message(address, pubkey, proxy, Fore.RED, f"Starting Session Failed: {Fore.YELLOW+Style.BRIGHT}{str(e)}")
            return None
    
    async def send_ping(self, address: str, pubkey: str, proxy=None):
        url = f"{self.BASE_API}/nodes/{pubkey}/ping"
        data = json.dumps({"isB7SConnected":True})
        headers = {
            **self.HEADERS[pubkey],
            "Authorization": f"Bearer {self.auth_tokens[address]}",
            "Content-Length": str(len(data)),
            "Content-Type": "application/json",
            "X-Extension-Signature": self.signatures[pubkey],
            "X-Extension-Version": "0.1.8"
        }
        proxies = {"http":proxy, "https":proxy} if proxy else None
        try:
            response = await asyncio.to_thread(requests.post, url=url, headers=headers, data=data, proxies=proxies, timeout=60, impersonate="chrome110")
            if response.status_code == 429:
                self.signatures[pubkey] = self.generate_signature()
                self.print_message(address, pubkey, proxy, Fore.RED, f"PING Failed: {Fore.YELLOW+Style.BRIGHT}Too Many Request, Retrying in 1 Minutes...")
                await asyncio.sleep(60)
                return None

            response.raise_for_status()
            return response.json()
        except Exception as e:
            self.print_message(address, pubkey, proxy, Fore.RED, f"PING Failed: {Fore.YELLOW+Style.BRIGHT}{str(e)}")
            return None
        
    async def process_check_connection(self, address: str, pubkey: str, use_proxy: bool, rotate_proxy: bool):
        while True:
            proxy = self.get_next_proxy_for_account(pubkey) if use_proxy else None

            is_valid = await self.check_connection(address, pubkey, proxy)
            if is_valid:
                self.ip_address[pubkey] = is_valid["ip"]
                self.signatures[pubkey] = self.generate_signature()
                return True
            
            if rotate_proxy:
                proxy = self.rotate_proxy_for_account(pubkey)

            await asyncio.sleep(5)
        
    async def process_register_node(self, address: str, pubkey: str, hardware_id: str, use_proxy: bool):
        proxy = self.get_next_proxy_for_account(pubkey) if use_proxy else None

        while True:
            registered = await self.register_node(address, pubkey, hardware_id, proxy)
            if registered:
                self.print_message(address, pubkey, proxy, Fore.GREEN, "Registering Node Success")
                return True
            
            await asyncio.sleep(5)
        
    async def process_start_session(self, address: str, pubkey: str, hardware_id: str, use_proxy: bool):
        is_registered = await self.process_register_node(address, pubkey, hardware_id, use_proxy)
        if is_registered:
            proxy = self.get_next_proxy_for_account(pubkey) if use_proxy else None

            while True:
                started = await self.start_session(address, pubkey, proxy)
                if isinstance(started, dict) and started.get("status") == "ok":
                    self.print_message(address, pubkey, proxy, Fore.GREEN, "Starting Session Success")
                    return True
                
                await asyncio.sleep(5)
            
    async def process_send_ping(self, address: str, pubkey: str, hardware_id: str, use_proxy: bool):
        is_session_started = await self.process_start_session(address, pubkey, hardware_id, use_proxy)
        if is_session_started:
            while True:
                proxy = self.get_next_proxy_for_account(pubkey) if use_proxy else None

                print(
                    f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                    f"{Fore.BLUE + Style.BRIGHT}Try to Sent Ping...{Style.RESET_ALL}                                         ",
                    end="\r",
                    flush=True
                )

                ping = await self.send_ping(address, pubkey, proxy)
                if isinstance(ping, dict) and ping.get("status") == "ok":
                    self.print_message(address, pubkey, proxy, Fore.GREEN, "PING Success")

                else:
                    await asyncio.sleep(5)
                    continue

                print(
                    f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                    f"{Fore.BLUE + Style.BRIGHT}Wait For 10 Minutes For Next Ping...{Style.RESET_ALL}",
                    end="\r"
                )
                
                await asyncio.sleep(10 * 60)
        
    async def process_get_node_uptime(self, address: str, pubkey: str, use_proxy: bool):
        while True:
            proxy = self.get_next_proxy_for_account(pubkey) if use_proxy else None

            node = await self.node_uptime(address, pubkey, proxy)
            if node:
                today_reward = node.get("todayReward", 0)
                total_reward = node.get("totalReward", 0)

                self.print_message(address, pubkey, proxy, Fore.GREEN, "Uptime Updated"
                    f"{Fore.MAGENTA + Style.BRIGHT} - {Style.RESET_ALL}"
                    f"{Fore.CYAN + Style.BRIGHT}Uptime Today:{Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT} {today_reward} Minutes {Style.RESET_ALL}"
                    f"{Fore.MAGENTA + Style.BRIGHT}-{Style.RESET_ALL}"
                    f"{Fore.CYAN + Style.BRIGHT} Uptime Total: {Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT}{total_reward} Minutes{Style.RESET_ALL}"
                )

            await asyncio.sleep(30 * 60)

    async def process_accounts(self, address: str, nodes: list, use_proxy: bool, rotate_proxy: bool):
        tasks = []

        async def process_node_session(node):
            pubkey = node.get("PubKey")
            hardware_id = node.get("HardwareId")

            if pubkey and hardware_id:
                self.HEADERS[pubkey] = {
                    "Accept": "*/*",
                    "Accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
                    "Origin": "chrome-extension://pljbjcehnhcnofmkdbjolghdcjnmekia",
                    "Sec-Fetch-Dest": "empty",
                    "Sec-Fetch-Mode": "cors",
                    "Sec-Fetch-Site": "cross-site",
                    "User-Agent": random.choice(USER_AGENT)
                }

                checked = await self.process_check_connection(address, pubkey, use_proxy, rotate_proxy)
                if checked:
                    tasks.append(asyncio.create_task(self.process_get_node_uptime(address, pubkey, use_proxy)))
                    tasks.append(asyncio.create_task(self.process_send_ping(address, pubkey, hardware_id, use_proxy)))

        await asyncio.gather(*[process_node_session(node) for node in nodes if node])

        await asyncio.gather(*tasks)
        
    async def main(self):
        try:
            accounts = self.load_accounts()
            if not accounts:
                self.log(f"{Fore.RED}No Accounts Loaded.{Style.RESET_ALL}")
                return

            use_proxy_choice, rotate_proxy = self.print_question()

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

            self.log(f"{Fore.CYAN + Style.BRIGHT}={Style.RESET_ALL}"*75)

            tasks = []
            for idx, account in enumerate(accounts, start=1):
                if account:
                    auth_token = account["B7S_AUTH_TOKEN"]
                    nodes = account["Nodes"]

                    if not auth_token or not nodes:
                        self.log(
                            f"{Fore.CYAN + Style.BRIGHT}[ Account: {Style.RESET_ALL}"
                            f"{Fore.WHITE + Style.BRIGHT}{idx}{Style.RESET_ALL}"
                            f"{Fore.MAGENTA + Style.BRIGHT} - {Style.RESET_ALL}"
                            f"{Fore.CYAN + Style.BRIGHT}Status:{Style.RESET_ALL}"
                            f"{Fore.RED + Style.BRIGHT} Invalid Account Data {Style.RESET_ALL}"
                            f"{Fore.CYAN + Style.BRIGHT}]{Style.RESET_ALL}"
                        )
                        continue

                    address = self.decode_auth_token(auth_token)
                    if not address:
                        self.log(
                            f"{Fore.CYAN + Style.BRIGHT}[ Account: {Style.RESET_ALL}"
                            f"{Fore.WHITE + Style.BRIGHT}{idx}{Style.RESET_ALL}"
                            f"{Fore.MAGENTA + Style.BRIGHT} - {Style.RESET_ALL}"
                            f"{Fore.CYAN + Style.BRIGHT}Status:{Style.RESET_ALL}"
                            f"{Fore.RED + Style.BRIGHT} Invalid B7S Auth Token {Style.RESET_ALL}"
                            f"{Fore.CYAN + Style.BRIGHT}]{Style.RESET_ALL}"
                        )
                        continue

                    self.auth_tokens[address] = auth_token

                    tasks.append(asyncio.create_task(self.process_accounts(address, nodes, use_proxy, rotate_proxy)))

            await asyncio.gather(*tasks)

        except Exception as e:
            self.log(f"{Fore.RED+Style.BRIGHT}Error: {e}{Style.RESET_ALL}")
            raise e

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