import os
import sys
import time
from bs4 import BeautifulSoup
import requests

# Force raw terminal streams to update in real-time line-by-line
sys.stdout.reconfigure(line_buffering=True)

# --- CONFIGURATION ---
USERNAME = os.getenv("SHANAPROJECT_USER", "YOUR_SHANAPROJECT_USERNAME")
PASSWORD = os.getenv("SHANAPROJECT_PASS", "YOUR_SHANAPROJECT_PASSWORD")

BASE_URL = "https://www.shanaproject.com"
REQUEST_TIMEOUT = 15.0


def parse_cli_arguments():
    """
    Parses command line arguments dynamically.
    Usage format: python subscribe_season.py [Season] [Year] [Subber]
    """
    season = "Fall"
    year = "2026"
    subber = "Don't care"

    if len(sys.argv) >= 2:
        season = sys.argv[1].capitalize()
    if len(sys.argv) >= 3:
        year = sys.argv[2]
    if len(sys.argv) >= 4:
        subber = " ".join(sys.argv[3:])

    season_url = f"{BASE_URL}/season/{season}-{year}/list"
    
    print(f"📋 Running Configuration:")
    print(f"   ➔ Target Season: {season} {year}")
    print(f"   ➔ Filter Subber: {subber}")
    print(f"   ➔ Source Layout: {season_url}\n")
    
    return season_url, subber


def subscribe_filtered_shows():
    if USERNAME == "YOUR_SHANAPROJECT_USERNAME" or PASSWORD == "YOUR_SHANAPROJECT_PASSWORD":
        print("❌ Error: Missing credentials. Please populate your SHANAPROJECT_USER environment variable.")
        sys.exit(1)

    target_season_url, preferred_subber = parse_cli_arguments()
    session = requests.Session()

    # 1. Login Handshake
    print("[1/4] Initiating secure backend session...")
    login_url = f"{BASE_URL}/login/"
    try:
        login_page_res = session.get(login_url, timeout=REQUEST_TIMEOUT)
        soup = BeautifulSoup(login_page_res.text, "html.parser")
        
        csrf_token_el = soup.find("input", {"name": "csrfmiddlewaretoken"})
        if not csrf_token_el:
            print("❌ Failure: Could not extract form token properties.")
            return
            
        csrf_token = csrf_token_el["value"]

        headers = {
            "Referer": login_url,
            "X-CSRFToken": csrf_token,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }

        payload = {
            "username": USERNAME,
            "password": PASSWORD,
            "csrfmiddlewaretoken": csrf_token,
            "next": "/"
        }

        post_login = session.post(login_url, data=payload, headers=headers, timeout=REQUEST_TIMEOUT)
        
        if not session.cookies.get("sessionid", None) and "login" in post_login.url:
            print("❌ Authentication failed. Check your password data variables.")
            return
            
        print("✅ Session validated successfully!")

        # 2. Query Subber ID or Apply Empty Fallback
        subber_id = ""  
        
        if preferred_subber.lower() != "don't care":
            print(f"\n[2/4] Querying database ID for subber group: '{preferred_subber}'")
            ajax_subber_url = f"{BASE_URL}/ajax/search/subber/"
            ajax_params = {
                "term": preferred_subber,
                "_type": "query",
                "q": preferred_subber
            }
            
            ajax_res = session.get(ajax_subber_url, params=ajax_params, timeout=REQUEST_TIMEOUT)
            
            try:
                subber_data = ajax_res.json()
                if subber_data and isinstance(subber_data, list) and len(subber_data) > 0:
                    subber_id = str(subber_data[0]["id"])
                    preferred_subber = subber_data[0]["value"]
                    print(f"✅ Found ID Mapping: '{preferred_subber}' ➔ ID: {subber_id}")
                else:
                    print(f"⚠️ Subber '{preferred_subber}' not found in ShanaProject database.")
                    print("   Falling back to a blank 'Don't care' rule configuration.")
                    preferred_subber = "Don't care"
                    subber_id = ""
            except Exception:
                print("⚠️ AJAX parsing error. Falling back to a blank 'Don't care' rule configuration.")
                preferred_subber = "Don't care"
                subber_id = ""
        else:
            print(f"\n[2/4] Bypassing subber querying. Enforcing general group fallback rules.")

        # 3. Extract Seasonal Data Directories
        print(f"\n[3/4] Extracting show collection IDs from: {target_season_url}")
        season_res = session.get(target_season_url, timeout=REQUEST_TIMEOUT)
        
        if season_res.status_code == 404:
            print(f"❌ Error: The seasonal grid map '{target_season_url}' doesn't exist.")
            return
            
        season_soup = BeautifulSoup(season_res.text, "html.parser")
        display_boxes = season_soup.find_all("div", class_=lambda x: x and "header_display_box" in x)
        
        unique_shows = {}
        for box in display_boxes:
            title_element = box.find("h3")
            follow_link = box.find("a", href=lambda x: x and "tid=" in x)
            
            if title_element and follow_link:
                show_name = title_element.get_text(strip=True)
                href_str = follow_link["href"]
                title_id = href_str.split("tid=")[-1]
                
                if title_id not in unique_shows:
                    unique_shows[title_id] = show_name

        print(f"-> Parsed {len(unique_shows)} unique seasonal show objects successfully.")

        if not unique_shows:
            print("⚠️ Parsed 0 items. Stopping execution loop.")
            return

        # 4. Submit Exact Payload matching the HAR specification exactly
        print("\n[4/4] Submitting precise parameter options to subscription engine...")
        
        for show_id, show_name in unique_shows.items():
            try:
                add_follow_endpoint = f"{BASE_URL}/follows/add/?tid={show_id}"
                session_csrf = session.cookies.get("csrftoken", "")

                follow_payload = {
                    "csrfmiddlewaretoken": session_csrf,
                    "title": str(show_id),  
                    "subber_tag": str(subber_id),      
                    "quality_preference": "180",       
                    "profile_preference": "8p",        
                    "source_preference": "ANY",
                    "back_date": "all"
                }

                # Matches your exact HAR post header rules
                action_headers = {
                    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
                    "content-type": "application/x-www-form-urlencoded",
                    "origin": BASE_URL,
                    "referer": add_follow_endpoint, # Exact HAR mapping change fixed here
                    "x-csrftoken": session_csrf,
                    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.0.0 Safari/537.36"
                }

                save_follow_res = session.post(
                    add_follow_endpoint, 
                    data=follow_payload, 
                    headers=action_headers, 
                    allow_redirects=False, 
                    timeout=REQUEST_TIMEOUT
                )
                
                # Check for HTTP 302 Redirection as requested by the server
                if save_follow_res.status_code == 302:
                    print(f"🔒 Enforced tracking rule: {show_name} ➔ [{preferred_subber} | 1080p | 8-bit]")
                else:
                    print(f"❌ Failed to submit rules on: {show_name} (Server rejected configuration with HTTP {save_follow_res.status_code})")

                time.sleep(2.0)

            except Exception as e:
                print(f"❌ Exception handling parameters on loop sequence for {show_name}: {e}")

    except Exception as e:
        print(f"❌ System processing error context: {e}")
    print("\n🏁 Automation routing sequence execution complete.")


if __name__ == "__main__":
    subscribe_filtered_shows()
