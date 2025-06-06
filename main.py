import requests
import time
import random
from colorama import Fore, init
init(autoreset=True)

def banner():
    print(Fore.GREEN + """
 ███╗   ██╗ █████╗ ██████╗ ███████╗███████╗███╗  ███╗
 ████╗  ██║██╔══██╗██╔══██╗██╔════╝██╔════╝████╗ ████║
 ██╔██╗ ██║███████║██║  ██║█████╗  █████╗  ██╔████╔██║
 ██║╚██╗██║██╔══██║██║  ██║██╔══╝  ██╔══╝  ██║╚██╔╝██║
 ██║ ╚████║██║  ██║██████╔╝███████╗███████╗██║ ╚═╝ ██║
 ╚═╝  ╚═══╝╚═╝  ╚═╝╚═════╝ ╚══════╝╚══════╝╚═╝     ╚═╝
             🔥 FACEBOOK REPORT BOMBER (SAFE) 🔥
    """)

def send_report(token, target_id, reason):
    headers = {
        "Authorization": f"OAuth {token}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "report_type": reason,
        "object": target_id,
        "feedback_source": "profile"
    }
    try:
        res = requests.post("https://graph.facebook.com/me/report", headers=headers, data=data, timeout=10)
        if res.status_code == 200:
            print(Fore.GREEN + f"[✓] REPORT SENT: Token ...{token[-5:]}")
            with open("log.txt", "a") as log:
                log.write(f"Reported ID: {target_id} | Reason: {reason} | Token: {token[:15]}...\n")
            return True
        else:
            print(Fore.RED + f"[✗] FAILED (Status {res.status_code}): Token ...{token[-5:]}")
            return False
    except requests.exceptions.RequestException as e:
        print(Fore.YELLOW + f"[!] NETWORK ERROR: {e} | Token ...{token[-5:]}")
        return False

def main():
    banner()
    target_id = input(Fore.CYAN + "[🎯] ENTER TARGET UID OR PROFILE LINK: ").strip()

    print(Fore.CYAN + "\n[1] Fake Account\n[2] Nudity\n[3] Spam\n[4] Harassment\n[5] Hate Speech")
    reason_map = {
        "1": "fake_account",
        "2": "nudity",
        "3": "spam",
        "4": "harassment",
        "5": "hate_speech"
    }
    reason_choice = input(Fore.CYAN + "[💥] SELECT REASON (1-5): ").strip()
    reason = reason_map.get(reason_choice, "fake_account")

    try:
        base_delay = int(input(Fore.CYAN + "[⏱️] BASE DELAY BETWEEN REPORTS (in seconds): ").strip())
        if base_delay < 3:
            print(Fore.YELLOW + "[!] Minimum delay is 3 seconds. Setting delay to 3.")
            base_delay = 3
    except:
        base_delay = 5
        print(Fore.YELLOW + "[!] Default delay set to 5 seconds.")

    try:
        with open("token.txt", "r") as f:
            tokens = [t.strip() for t in f if t.strip()]
    except:
        print(Fore.RED + "[✗] ERROR: token.txt file not found!")
        return

    if not tokens:
        print(Fore.RED + "[✗] No tokens found in token.txt!")
        return

    print(Fore.MAGENTA + f"\n[🚀] Starting SAFE Auto Report on ID: {target_id}")
    print(Fore.MAGENTA + f"[⚙️] Report Reason: {reason.upper()} | Base Delay: {base_delay}s\n")

    count = 0
    token_index = 0
    start_time = time.time()

    while True:
        token = tokens[token_index]
        success = send_report(token, target_id, reason)
        if success:
            count += 1
            print(Fore.CYAN + f"[🔁] Total Reports Sent: {count}")
        else:
            print(Fore.YELLOW + "[!] Skipping token due to error.")

        # Rotate tokens round-robin
        token_index = (token_index + 1) % len(tokens)

        # Wait random delay (base_delay to base_delay + 4 seconds)
        wait_time = base_delay + random.randint(0,4)
        print(Fore.MAGENTA + f"[⏳] Waiting {wait_time} seconds before next report...")
        time.sleep(wait_time)

        # Every 5 minutes, rest 10 seconds extra (to avoid rate limits)
        elapsed = time.time() - start_time
        if elapsed > 300:
            print(Fore.MAGENTA + "[💤] Taking a short break for 10 seconds to avoid detection...")
            time.sleep(10)
            start_time = time.time()


if __name__ == "__main__":
    main()
