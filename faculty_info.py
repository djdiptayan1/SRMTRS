import pandas as pd
import requests
from bs4 import BeautifulSoup
import json

session = requests.Session()


def fetch_page(page_number, department_code):
    post_url = "https://www.srmist.edu.in/wp-admin/admin-ajax.php"
    post_headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.9",
        "Cache-Control": "no-cache",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Cookie": "; ".join(
            [f"{k}={v}" for k, v in session.cookies.get_dict().items()]
        ),
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
        "formData": f"campus=&college=&department={department_code}&faculty=&facultyType=79&designation=33",
        "security": "53cc2ea29d",
        "action": "list_faculties_default",
    }

    response = session.post(post_url, headers=post_headers, data=post_data)

    return response


def read_departments_from_excel(file_path):
    df = pd.read_excel(file_path)
    departments = df.to_dict("records")
    return departments


def main():
    departments = read_departments_from_excel("SRM_Departments.xlsx")

    faculties_data = []

    for dept in departments:
        department_code = dept["DeptCode"]
        department_name = dept["DeptName"]

        print(f"Fetching data for Department: {department_name} ({department_code})")

        page_number = 1
        while True:
            response = fetch_page(page_number, department_code)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                staff_cards = soup.find_all("div", class_="staff-card")

                for card in staff_cards:
                    faculty_name = card.find("h3", class_="post-title").text.strip()
                    designation = card.find("div", class_="designation").text.strip()
                    specialization = card.find(
                        "div", class_="specialization_area"
                    ).text.strip()
                    image_url = card.find("img")["src"]
                    faculty_link = card.find("h3", class_="post-title").find("a")[
                        "href"
                    ]

                    faculties_data.append(
                        {
                            "DepartmentCode": department_code,
                            "DepartmentName": department_name,
                            "FacultyName": faculty_name,
                            "ProfileLink": faculty_link,
                            "Designation": designation,
                            "Specialization": specialization,
                            "ImageURL": image_url,
                        }
                    )

                # Check for next page
                pagination_links = soup.find("div", class_="pagination-link")
                if pagination_links:
                    next_page = pagination_links.find(
                        "li", class_="selected"
                    ).find_next_sibling("li", class_="active")
                    if next_page:
                        page_number = int(next_page.get("p"))
                    else:
                        break
                else:
                    break
            else:
                print(
                    f"Failed to fetch data for Department: {department_name} ({department_code})"
                )

    json_file_path = "faculties_data.json"
    with open(json_file_path, "w", encoding="utf-8") as json_file:
        json.dump(faculties_data, json_file, ensure_ascii=False, indent=4)

    print(f"Data saved to {json_file_path}")


if __name__ == "__main__":
    main()
