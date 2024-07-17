import requests
from bs4 import BeautifulSoup

def fetch_raw_html(faculty_id):
    url = f"https://www.srmist.edu.in/faculty/prof-v-chitra/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    # Fetch the HTML content
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        html_content = response.text
        return html_content
    else:
        print(f"Failed to fetch data for Faculty ID: {faculty_id}")
        return None

def extract_experience(html_content):
    # Parse HTML
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find all elements with class 'elementor-widget-container'
    widget_containers = soup.find_all('div', class_='elementor-widget-container')

    # Loop through each element to find the specific text
    for container in widget_containers:
        # Check if the element contains the text 'EXPERIENCE :'
        if 'EXPERIENCE :' in container.text:
            # Extract the experience information
            experience = container.text.strip()
            return experience
    
    # If not found, return a message indicating it wasn't found
    return "Experience information not found"

def extract_email(html_content):
    # Parse HTML
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find all <li> elements with class 'elementor-icon-list-item'
    list_items = soup.find_all('li', class_='elementor-icon-list-item')

    # Loop through each list item to find the email address
    for item in list_items:
        # Find the <span> with class 'elementor-icon-list-text'
        email_span = item.find('span', class_='elementor-icon-list-text')
        # Check if the email_span exists and contains '@' (basic email validation)
        if email_span and '@' in email_span.text:
            return email_span.text.strip()  # Return the email address
    
    # If not found, return None
    return None

def extract_phone_number(html_content):
    # Parse HTML
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find all <li> elements with class 'elementor-icon-list-item'
    list_items = soup.find_all('li', class_='elementor-icon-list-item')

    # Loop through each list item to find the phone number
    for item in list_items:
        # Find the <span> with class 'elementor-icon-list-text'
        phone_span = item.find('span', class_='elementor-icon-list-text')
        # Check if the phone_span exists and contains only digits (phone number format)
        if phone_span and phone_span.text.isdigit():
            return phone_span.text.strip()  # Return the phone number
    
    # If not found, return None
    return None

def main():
    faculty_id = 'professor-t-v-gopal'  # Replace with the faculty ID you want to fetch data for

    # Fetch HTML content
    html_content = fetch_raw_html(faculty_id)
    if html_content:
        # Extract experience information
        experience = extract_experience(html_content)
        
        # Extract email address
        email = extract_email(html_content)
        
        # Extract phone number
        phone_number = extract_phone_number(html_content)
        
        # Print or process the extracted information
        print("Experience:", experience)
        print("Email:", email)
        print("Phone Number:", phone_number)

if __name__ == "__main__":
    main()
