import time, os, subprocess, socket, json, secrets, string, platform, psutil, shutil
from urllib.request import urlopen, Request
from datetime import datetime
import re
from threading import Thread

# High-Tech UI Colors
CYAN, GREEN, RED, YELLOW, BOLD, MAGENTA, WHITE, END = '\033[96m', '\033[92m', '\033[91m', '\033[93m', '\033[1m', '\033[95m', '\033[97m', '\033[0m'

class RudraOmni:
    def __init__(self):
        self.username = "CREATOR"
        self.version = "v16.0-ULTRA-PRO-FIXED"
        self.start_time = datetime.now()
        self.headers = {'User-Agent': 'Mozilla/5.0'}

    def clear(self): 
        os.system('cls' if os.name == 'nt' else 'clear')

    def draw_hud(self):
        self.clear()
        print(f"{MAGENTA}{BOLD}██████╗ ██╗   ██╗██████╗ ██████╗  █████╗ \n██╔══██╗██║   ██║██╔══██╗██╔══██╗██╔══██╗\n██████╔╝██║   ██║██║  ██║██████╔╝███████║\n██╔══██╗██║   ██║██║  ██║██╔══██╗██╔══██║\n██║  ██║╚██████╔╝██████╔╝██║  ██║██║  ██║\n╚═╝  ╚═╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝{END}")
        print(f"{CYAN}--- LIGHTNING SPEED | ALL SYSTEMS OPERATIONAL | VER: {self.version} ---{END}\n")

    def show_help(self):
        print(f"\n{BOLD}{WHITE}--- COMMAND CENTER ---{END}")
        cmds = {
            "MYIP/TRACE": "Network Identity & Geo-Trace.",
            "DNS/WHOIS": "Domain resolution & Registry info.",
            "SCAN/NET": "Port checking & Active connections.",
            "ARP-SCAN": "Instant Local Network Mapping.",
            "DNS-CACHE": "View system DNS history (Windows).",
            "SPEED/WEATHER": "Latency test & Local climate.",
            "SYS/PROCESS": "Hardware health & Process control.",
            "TASK-KILL": "Force stop process by PID.",
            "FILE-INFO": "Metadata & Size analysis.",
            "WEB-SCRAPE": "Extract links from any URL.",
            "SHRED": "Permanently destroy a file.",
            "LOCK/UNLOCK": "Hide or Restore folders.",
            "PASS/MAC": "Security keys & Hardware ID."
        }
        for c, d in cmds.items():
            print(f"{GREEN}{c.ljust(15)}{END} : {WHITE}{d}{END}")
        print(f"{MAGENTA}------------------------------------------------------------{END}\n")

    def get_data(self, url):
        try:
            req = Request(url, headers=self.headers)
            with urlopen(req, timeout=2) as response:
                return response.read().decode('utf-8', errors='ignore')
        except: return None

    def main(self):
        self.draw_hud()
        while True:
            try:
                raw_input = input(f"{BOLD}{CYAN}RUDRA_OMNI@{self.username}:~# {END}").strip()
                if not raw_input: continue
                parts = raw_input.split()
                cmd = parts[0].upper()

                # --- FIXED: ARP-SCAN (Lightning Fast Subnet Scan) ---
                if cmd == "ARP-SCAN":
                    print(f"{YELLOW}Initiating ARP Subnet Mapping...{END}")
                    local_ip = socket.gethostbyname(socket.gethostname())
                    base = ".".join(local_ip.split('.')[:-1])
                    print(f"{WHITE}Scanning Subnet: {base}.0/24{END}")
                    
                    def ping_check(ip):
                        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        s.settimeout(0.1)
                        if s.connect_ex((ip, 135)) == 0 or s.connect_ex((ip, 445)) == 0:
                            print(f"{GREEN}[+] Device Found: {ip}{END}")
                        s.close()

                    threads = []
                    for i in range(1, 255):
                        t = Thread(target=ping_check, args=(f"{base}.{i}",))
                        t.start()
                        threads.append(t)
                    for t in threads: t.join()
                    print(f"{CYAN}Scan Complete.{END}")

                # --- FIXED: DNS-CACHE (Windows Optimized) ---
                elif cmd == "DNS-CACHE":
                    if os.name == 'nt':
                        print(f"{YELLOW}Reading System DNS Resolver Cache...{END}")
                        output = subprocess.check_output("ipconfig /displaydns", shell=True).decode(errors='ignore')
                        records = re.findall(r"Record Name\s+\.\s+\.\s+\.\s+:\s+(.+)", output)
                        if records:
                            print(f"{GREEN}Recently Visited Domains:{END}")
                            for r in list(set(records))[:15]: print(f"{WHITE}- {r}{END}")
                        else: print(f"{RED}Cache empty or access denied.{END}")
                    else: print(f"{RED}This command requires Windows.{END}")

                # --- CORE FEATURES ---
                elif cmd == "DNS":
                    target = input(f"{CYAN}Domain: {END}")
                    print(f"{GREEN}IP: {socket.gethostbyname(target)}{END}")

                elif cmd == "SCAN":
                    target = input(f"{CYAN}Target IP: {END}")
                    for p in [21, 22, 80, 443, 3389]:
                        s = socket.socket()
                        s.settimeout(0.1)
                        res = s.connect_ex((target, p))
                        print(f"{WHITE}Port {p}: {'[OPEN]' if res==0 else '[CLOSED]'}{END}")
                        s.close()

                elif cmd == "SPEED":
                    start = time.time()
                    socket.gethostbyname("google.com")
                    print(f"{GREEN}Latency: {(time.time()-start)*1000:.2f}ms{END}")

                elif cmd == "TASK-KILL":
                    pid = int(input(f"{CYAN}PID to Kill: {END}"))
                    psutil.Process(pid).terminate()
                    print(f"{GREEN}Terminated.{END}")

                elif cmd == "MYIP":
                    local = socket.gethostbyname(socket.gethostname())
                    pub = json.loads(self.get_data('https://api.ipify.org?format=json') or '{"ip":"Offline"}')
                    print(f"{GREEN}Local: {local} | Public: {pub['ip']}{END}")

                elif cmd == "SYS":
                    print(f"{WHITE}CPU: {psutil.cpu_percent()}% | RAM: {psutil.virtual_memory().percent}%{END}")

                elif cmd == "WEATHER":
                    city = input(f"{CYAN}City: {END}")
                    res = self.get_data(f"https://wttr.in/{city}?format=%C+%t")
                    print(f"{GREEN}{res if res else 'Error'}{END}")

                elif cmd == "LOCK" and len(parts) > 1:
                    subprocess.run(["attrib", "+h", "+s", "+r", parts[1]], shell=True)
                    print(f"{GREEN}Locked {parts[1]}{END}")

                elif cmd == "UNLOCK" and len(parts) > 1:
                    subprocess.run(["attrib", "-h", "-s", "-r", parts[1]], shell=True)
                    print(f"{GREEN}Unlocked {parts[1]}{END}")

                elif cmd == "HELP": self.show_help()
                elif cmd == "CLEAR": self.draw_hud()
                elif cmd == "EXIT": break
                else: print(f"{RED}Unknown Command. Type 'HELP'.{END}")

            except Exception as e: print(f"{RED}Error: {e}{END}")

if __name__ == "__main__":
    RudraOmni().main()