import requests
from bs4 import BeautifulSoup

# Start a session to handle cookies
session = requests.Session()

# Define the initial URL to get the cookies (e.g., the landing page of the website)
initial_url = "https://www.srmist.edu.in"

# Define headers to mimic a browser
initial_headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9",
    "Cache-Control": "no-cache",
    "Dnt": "1",
    "Pragma": "no-cache",
    "Sec-Ch-Ua": '"Not/A)Brand";v="8", "Chromium";v="126"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": '"macOS"',
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
}

# Make an initial request to get the session cookies
initial_response = session.get(initial_url, headers=initial_headers)

# Check the response and cookies
print("Initial request status code:", initial_response.status_code)
print("Initial cookies:", session.cookies.get_dict())
print("Initial response headers:", initial_response.headers)


# Function to fetch a specific page
def fetch_page(page_number):
    post_url = "https://www.srmist.edu.in/wp-admin/admin-ajax.php"
    post_headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.9",
        "Cache-Control": "no-cache",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Cookie": "npfwg=1; npf_r=; npf_l=www.srmist.edu.in; npf_u=https://www.srmist.edu.in/staff-finder/?dept=13537; "
        + "; ".join([f"{k}={v}" for k, v in session.cookies.get_dict().items()]),
        "Dnt": "1",
        "Origin": "https://www.srmist.edu.in",
        "Pragma": "no-cache",
        "Referer": "https://www.srmist.edu.in/staff-finder/?dept=13537",
        "Sec-Ch-Ua": '"Not/A)Brand";v="8", "Chromium";v="126"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": '"macOS"',
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
    }
    post_data = {
        "page": page_number,
        "formData": "campus=&college=&department=24109&faculty=&facultyType=79&designation=33",
        "security": "53cc2ea29d",
        "action": "list_faculties_default",
    }

    # Make the POST request using the session
    response = session.post(post_url, headers=post_headers, data=post_data)

    return response


# Function to extract faculty information from HTML content
def extract_faculty_info(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    staff_cards = soup.find_all("div", class_="staff-card")
    faculty_info = []
    for card in staff_cards:
        name = card.find("h3", class_="post-title").text.strip()
        designation = card.find("div", class_="designation").text.strip()
        profile_link = card.find("h3", class_="post-title").find("a")["href"]
        faculty_info.append((name, designation, profile_link))
    return faculty_info


# Iterate over pages and extract faculty information
page_number = 1
all_faculty_info = []

while True:
    response = fetch_page(page_number)
    if response.status_code != 200 or "no more records" in response.text.lower():
        break
    faculty_info = extract_faculty_info(response.text)
    if not faculty_info:
        break
    all_faculty_info.extend(faculty_info)
    page_number += 1
    print(response.text)

# Print the extracted information
for name, designation, profile_link in all_faculty_info:
    print(f"Name: {name}, Designation: {designation}, Profile Link: {profile_link}")
