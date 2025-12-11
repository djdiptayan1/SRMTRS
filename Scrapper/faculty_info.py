import requests
from bs4 import BeautifulSoup
import json
import time

session = requests.Session()

SECURITY_TOKEN = "4d601211ca"

COLLEGES = [
    {"ID": 9812, "title": "Faculty of Engineering & Technology"},
    {"ID": 29288, "title": "Faculty of Management"},
    {"ID": 23702, "title": "Faculty of Science & Humanities"},
    {"ID": 24139, "title": "Medicine & Health Sciences"},
    {"ID": 29281, "title": "SRM School of Law"},
]


def fetch_college_page(page_number, college_id):
    url = "https://www.srmist.edu.in/wp-admin/admin-ajax.php"

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "https://www.srmist.edu.in",
        "Referer": "https://www.srmist.edu.in/staff-finder/",
    }

    payload = {
        "page": page_number,
        "formData": f"campus=78&college={college_id}&department=&faculty=&facultyType=&designation=",
        "security": SECURITY_TOKEN,
        "action": "list_faculties_default",
    }

    try:
        response = session.post(url, headers=headers, data=payload)
        return response
    except Exception as e:
        print(f"  [!] Request Error: {e}")
        return None


def main():
    all_data = []

    for college in COLLEGES:
        c_id = college["ID"]
        c_name = college["title"]
        print(f"--- Fetching: {c_name} (ID: {c_id}) ---")

        page = 1
        while True:
            response = fetch_college_page(page, c_id)

            if not response or response.status_code != 200:
                print(
                    f"  [!] Failed to fetch page {page}. Status: {response.status_code if response else 'None'}"
                )
                break
            html_content = ""
            try:
                # Attempt to parse as JSON first (just in case)
                json_resp = response.json()
                if isinstance(json_resp, dict) and "data" in json_resp:
                    html_content = json_resp["data"]
                else:
                    html_content = response.text
            except:
                # Fallback to raw text
                html_content = response.text

            if not html_content.strip():
                print("  [!] Empty content received. Ending loop.")
                break

            soup = BeautifulSoup(html_content, "html.parser")
            staff_cards = soup.find_all("div", class_="staff-card")

            if not staff_cards:
                print(
                    f"  [i] No more staff found on page {page}. Moving to next college."
                )
                break

            print(f"  > Page {page}: Found {len(staff_cards)} staff.")

            for card in staff_cards:
                try:
                    # Name & Link
                    title_tag = card.find("h3", class_="post-title")
                    name = title_tag.text.strip() if title_tag else "N/A"
                    link = (
                        title_tag.find("a")["href"]
                        if title_tag and title_tag.find("a")
                        else "N/A"
                    )

                    # Designation
                    desig_tag = card.find("div", class_="designation")
                    designation = desig_tag.text.strip() if desig_tag else "N/A"

                    # Specialization
                    spec_tag = card.find("div", class_="specialization_area")
                    specialization = spec_tag.text.strip() if spec_tag else "N/A"

                    # Image
                    img_tag = card.find("img")
                    image_url = img_tag["src"] if img_tag else "N/A"

                    all_data.append(
                        {
                            "College": c_name,
                            "Name": name,
                            "Designation": designation,
                            "Specialization": specialization,
                            "ProfileLink": link,
                            "ImageURL": image_url,
                        }
                    )
                except Exception as e:
                    print(f"  [!] Error parsing card: {e}")

            # --- Pagination Logic ---
            # Check if there is a 'Next' page active
            pagination = soup.find("div", class_="pagination-link")
            if pagination:
                current = pagination.find("li", class_="selected")
                if current:
                    # Find the next 'li' that has class 'active'
                    next_page = current.find_next_sibling("li", class_="active")
                    if next_page:
                        page += 1
                        # Small delay to be polite to the server
                        # time.sleep(0.5)
                    else:
                        break  # No next page
                else:
                    break  # Logic unclear, stop to prevent infinite loop
            else:
                break  # No pagination, likely single page results

    # Save Data
    filename = "srm_faculties_all_colleges.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(all_data, f, indent=4, ensure_ascii=False)

    print(f"\nCompleted! Total records: {len(all_data)}")
    print(f"Saved to {filename}")


if __name__ == "__main__":
    main()


# import pandas as pd
# import requests
# from bs4 import BeautifulSoup
# import json

# session = requests.Session()


# def fetch_page(page_number, department_code):
#     post_url = "https://www.srmist.edu.in/wp-admin/admin-ajax.php"
#     post_headers = {
#         "Accept": "*/*",
#         "Accept-Encoding": "gzip, deflate, br, zstd",
#         "Accept-Language": "en-US,en;q=0.9",
#         "Cache-Control": "no-cache",
#         "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
#         "Cookie": "; ".join(
#             [f"{k}={v}" for k, v in session.cookies.get_dict().items()]
#         ),
#         "Dnt": "1",
#         "Origin": "https://www.srmist.edu.in",
#         "Pragma": "no-cache",
#         "Referer": "https://www.srmist.edu.in/staff-finder/?dept=13537",
#         "Sec-Ch-Ua": '"Not/A)Brand";v="8", "Chromium";v="126"',
#         "Sec-Ch-Ua-Mobile": "?0",
#         "Sec-Ch-Ua-Platform": '"macOS"',
#         "Sec-Fetch-Dest": "empty",
#         "Sec-Fetch-Mode": "cors",
#         "Sec-Fetch-Site": "same-origin",
#         "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
#         "X-Requested-With": "XMLHttpRequest",
#     }
#     post_data = {
#         "page": page_number,
#         "formData": f"campus=&college=&department={department_code}&faculty=&facultyType=79&designation=33",
#         "security": "53cc2ea29d",
#         "action": "list_faculties_default",
#     }

#     response = session.post(post_url, headers=post_headers, data=post_data)

#     return response


# def read_departments_from_excel(file_path):
#     df = pd.read_excel(file_path)
#     departments = df.to_dict("records")
#     return departments


# def main():
#     departments = read_departments_from_excel("../data/SRM_Departments.xlsx")

#     faculties_data = []

#     for dept in departments:
#         department_code = dept["DeptCode"]
#         department_name = dept["DeptName"]

#         print(f"Fetching data for Department: {department_name} ({department_code})")

#         page_number = 1
#         while True:
#             response = fetch_page(page_number, department_code)
#             if response.status_code == 200:
#                 soup = BeautifulSoup(response.text, "html.parser")
#                 staff_cards = soup.find_all("div", class_="staff-card")

#                 for card in staff_cards:
#                     faculty_name = card.find("h3", class_="post-title").text.strip()
#                     designation = card.find("div", class_="designation").text.strip()
#                     specialization = card.find(
#                         "div", class_="specialization_area"
#                     ).text.strip()
#                     image_url = card.find("img")["src"]
#                     faculty_link = card.find("h3", class_="post-title").find("a")[
#                         "href"
#                     ]

#                     faculties_data.append(
#                         {
#                             "DepartmentCode": department_code,
#                             "DepartmentName": department_name,
#                             "FacultyName": faculty_name,
#                             "ProfileLink": faculty_link,
#                             "Designation": designation,
#                             "Specialization": specialization,
#                             "ImageURL": image_url,
#                         }
#                     )

#                 pagination_links = soup.find("div", class_="pagination-link")
#                 if pagination_links:
#                     next_page = pagination_links.find(
#                         "li", class_="selected"
#                     ).find_next_sibling("li", class_="active")
#                     if next_page:
#                         page_number = int(next_page.get("p"))
#                     else:
#                         break
#                 else:
#                     break
#             else:
#                 print(
#                     f"Failed to fetch data for Department: {department_name} ({department_code})"
#                 )

#     json_file_path = "faculties_data_new.json"
#     with open(json_file_path, "w", encoding="utf-8") as json_file:
#         json.dump(faculties_data, json_file, ensure_ascii=False, indent=4)

#     print(f"Data saved to {json_file_path}")


# if __name__ == "__main__":
#     main()
