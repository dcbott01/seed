import requests
import time
from colorama import init, Fore, Back, Style
import sys
import os
import datetime
import pytz
from datetime import datetime

init(autoreset=True)

def display_welcome_message():
    print(r"""
 
  _  _   _    ____  _   ___    _   
 | \| | /_\  |_  / /_\ | _ \  /_\  
 | .` |/ _ \  / / / _ \|   / / _ \ 
 |_|\_/_/ \_\/___/_/ \_\_|_\/_/ \_\
                                   

    """)
    print(Fore.MAGENTA + Back.WHITE + Style.BRIGHT + "Mine SEED BOT")
    print(Fore.WHITE + Back.BLUE + Style.BRIGHT + "Support the developer :)")
    print(Fore.YELLOW + Back.BLUE + Style.BRIGHT + "0x5bc0d1f74f371bee6dc18d52ff912b79703dbb54")
    print(Fore.RED + Style.BRIGHT + "Update Link: https://github.com/dcbott01/seed")
    print(Fore.CYAN + Style.BRIGHT + "PLEASE DO NOT RENAME THE SCRIPT")

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# API endpoints
api_claim = 'https://elb.seeddao.org/api/v1/seed/claim'
api_balance = 'https://elb.seeddao.org/api/v1/profile/balance'
api_checkin = 'https://elb.seeddao.org/api/v1/login-bonuses'
api_upgrade_storage = 'https://elb.seeddao.org/api/v1/seed/storage-size/upgrade'
api_upgrade_mining = 'https://elb.seeddao.org/api/v1/seed/mining-speed/upgrade'
api_upgrade_holy = 'https://elb.seeddao.org/api/v1/upgrades/holy-water'
api_profile = 'https://elb.seeddao.org/api/v1/profile'

# Request headers
headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-ID,en-US;q=0.9,en;q=0.8,id;q=0.7',
    'content-length': '0',
    'dnt': '1',
    'origin': 'https://cf.seeddao.org',
    'priority': 'u=1, i',
    'referer': 'https://cf.seeddao.org/',
    'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'telegram-data': 'tokens',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
}

def read_tokens():
    try:
        with open('query.txt', 'r') as file:
            tokens = file.read().strip().split('\n')
        return tokens
    except FileNotFoundError:
        print(Fore.RED + "query.txt file is missing.")
        return []
    except Exception as e:
        print(Fore.RED + "Error reading tokens:", str(e))
        return []

def fetch_worm_status():
    response = requests.get('https://elb.seeddao.org/api/v1/worms', headers=headers)
    if response.status_code == 200:
        worm_info = response.json()['data']
        next_refresh = worm_info.get('next_worm')
        worm_caught = worm_info.get('is_caught', False)

        if next_refresh:
            next_refresh_dt = datetime.fromisoformat(next_refresh[:-1] + '+00:00')
            now_utc = datetime.now(pytz.utc)
            time_difference_seconds = (next_refresh_dt - now_utc).total_seconds()
            hours = int(time_difference_seconds // 3600)
            minutes = int((time_difference_seconds % 3600) // 60)
            print(f"{Fore.GREEN+Back.BLACK+Style.BRIGHT}[ Worms ]: Next in {hours} hours {minutes} minutes - Status: {'Caught' if worm_caught else 'Available'}")
        else:
            print(f"{Fore.RED+Back.BLACK+Style.BRIGHT}[ Worms ]: 'next_worm' data not available.")
        return worm_info
    else:
        print(f"{Fore.RED+Back.BLACK+Style.BRIGHT}[ Worms ]: Error retrieving worm data.")
        return None

def capture_worm():
    worm_info = fetch_worm_status()
    if worm_info and not worm_info.get('is_caught', True):
        response = requests.post('https://elb.seeddao.org/api/v1/worms/catch', headers=headers)
        if response.status_code == 200:
            print(f"{Fore.GREEN+Back.BLACK+Style.BRIGHT}[ Worms ]: Worm captured successfully")
        elif response.status_code == 400:
            print(f"{Fore.RED+Back.BLACK+Style.BRIGHT}[ Worms ]: Already captured")
        elif response.status_code == 404:
            print(f"{Fore.RED+Back.BLACK+Style.BRIGHT}[ Worms ]: Worm not found")
        else:
            print(f"{Fore.RED+Back.BLACK+Style.BRIGHT}[ Worms ]: Capture failed, status code:", response)
    else:
        print(f"{Fore.RED+Back.BLACK+Style.BRIGHT}[ Worms ]: Worm unavailable or already captured.")

def fetch_profile():
    response = requests.get(api_profile, headers=headers)
    if response.status_code == 200:
        profile_info = response.json()
        user_name = profile_info['data']['name']
        print(f"{Fore.CYAN+Back.BLACK+Style.BRIGHT}============== [ Profile | {user_name} ] ==============")

        upgrade_levels = {}
        for upgrade in profile_info['data']['upgrades']:
            upgrade_type = upgrade['upgrade_type']
            upgrade_level = upgrade['upgrade_level']
            if upgrade_type in upgrade_levels:
                if upgrade_level > upgrade_levels[upgrade_type]:
                    upgrade_levels[upgrade_type] = upgrade_level
            else:
                upgrade_levels[upgrade_type] = upgrade_level

        for upgrade_type, level in upgrade_levels.items():
            print(f"{Fore.BLUE+Back.BLACK+Style.BRIGHT}[ {upgrade_type.capitalize()} Level ]: {level + 1}")
    else:
        print(Fore.RED + "Error retrieving profile data, status code:", response.status_code)
        return None

def verify_balance():
    response = requests.get(api_balance, headers=headers)
    if response.status_code == 200:
        balance_info = response.json()
        print(f"{Fore.YELLOW+Back.BLACK+Style.BRIGHT}[ Balance ]: {balance_info['data'] / 1000000000}")
        return True
    else:
        print(f"{Fore.RED+Back.BLACK+Style.BRIGHT}[ Balance ]: Error | {response.status_code}")
        return False

def perform_daily_checkin():
    response = requests.post(api_checkin, headers=headers)
    if response.status_code == 200:
        checkin_data = response.json()
        day = checkin_data.get('data', {}).get('no', '')
        print(f"{Fore.GREEN+Back.BLACK+Style.BRIGHT}[ Check-in ]: Successfully checked in | Day {day}")
    else:
        checkin_data = response.json()
        if checkin_data.get('message') == 'already claimed for today':
            print(f"{Fore.RED+Back.BLACK+Style.BRIGHT}[ Check-in ]: Already checked in today")
        else:
            print(f"{Fore.RED+Back.BLACK+Style.BRIGHT}[ Check-in ]: Failed | {checkin_data}")

def upgrade_storage(confirm):
    if confirm.lower() == 'y':
        response = requests.post(api_upgrade_storage, headers=headers)
        if response.status_code == 200:
            return '[ Upgrade Storage ]: Successful'
        else:
            return '[ Upgrade Storage ]: Insufficient balance'
    else:
        return None

def upgrade_mining(confirm):
    if confirm.lower() == 'y':
        response = requests.post(api_upgrade_mining, headers=headers)
        if response.status_code == 200:
            return '[ Upgrade Mining ]: Successful'
        else:
            return '[ Upgrade Mining ]: Insufficient balance'
    else:
        return None

def upgrade_holy(confirm):
    if confirm.lower() == 'y':
        response = requests.post(api_upgrade_holy, headers=headers)
        if response.status_code == 200:
            return '[ Upgrade Holy ]: Successful'
        else:
            return '[ Upgrade Holy ]: Requirements not met'
    else:
        return None

def fetch_tasks():
    response = requests.get('https://elb.seeddao.org/api/v1/tasks/progresses', headers=headers)
    tasks = response.json()['data']
    for task in tasks:
        if task['task_user'] is None or not task['task_user']['completed']:
            mark_task_complete(task['id'], task['name'])

def mark_task_complete(task_id, task_name):
    response = requests.post(f'https://elb.seeddao.org/api/v1/tasks/{task_id}', headers=headers)
    if response.status_code == 200:
        print(f"{Fore.GREEN+Back.BLACK+Style.BRIGHT}[ Tasks ]: Task {task_name} marked complete.")
    else:
        print(f"{Fore.RED+Back.BLACK+Style.BRIGHT}[ Tasks ]: Failed to complete task {task_name}, status code: {response.status_code}")

def main():
    display_welcome_message()
    tokens = read_tokens()

    auto_upgrade_storage = input("Upgrade storage? (y/n): ")
    auto_upgrade_mining = input("Upgrade mining? (y/n): ")
    auto_upgrade_holy = input("Upgrade holy? (y/n): ")
    auto_clear_tasks = input("Clear tasks? (y/n): ")

    while True:
        storage_upgrade_result = upgrade_storage(auto_upgrade_storage)
        mining_upgrade_result = upgrade_mining(auto_upgrade_mining)
        holy_upgrade_result = upgrade_holy(auto_upgrade_holy)
        
        for index, token in enumerate(tokens):
            headers['telegram-data'] = token
            profile_info = fetch_profile()
            if profile_info:
                print(f"Processing for token {profile_info['data']['name']}")

            if storage_upgrade_result:
                print(storage_upgrade_result)
                time.sleep(1)
            if mining_upgrade_result:
                print(mining_upgrade_result)
                time.sleep(1)
            if holy_upgrade_result:
                print(holy_upgrade_result)
                time.sleep(1)

            if verify_balance():
                response = requests.post(api_claim, headers=headers)
                if response.status_code == 200:
                    print(f"{Fore.GREEN+Back.BLACK+Style.BRIGHT}[ Claim ]: Claim successful")
                elif response.status_code == 400:
                    response_data = response.json()
                    print(f"{Fore.RED+Back.BLACK+Style.BRIGHT}[ Claim ]: Not yet time to claim")
                else:
                    print("An error occurred, status code:", response.status_code)

                perform_daily_checkin()
                capture_worm()
                if auto_clear_tasks.lower() == 'y':
                    fetch_tasks()

            print(Fore.CYAN + Back.BLACK + Style.BRIGHT + f"\nFinished processing account. Moving to the next...\n")
            time.sleep(5)
        
        for i in range(3600, 0, -1):
            sys.stdout.write(f"\r{Fore.CYAN+Back.BLACK+Style.BRIGHT}============ Completed, waiting {i} seconds.. ============")
            sys.stdout.flush()
            time.sleep(1)
        print()

        clear_screen()

if __name__ == "__main__":
    main()
