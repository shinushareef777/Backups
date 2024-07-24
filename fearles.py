import requests
from bs4 import BeautifulSoup
import time
import json
import pandas as pd
import os
from openpyxl.styles import Alignment
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.hyperlink import Hyperlink
import re

url = "https://www.fearlessphotographers.com/best-wedding-photographers-directory.cfm"
main_url = "https://www.fearlessphotographers.com"

classes = {
    "profile_link": "content",
    "info": "info",  # main class all the info like name, social media and website is within this class
    "name": "big",  # h1
    "social_media": "social",  # div containing all the social media and website
    # div.social contains links to various website. title is unique. It has Facebook, Website, Instagram as title
    "bio": "photog-bio",  # div
    "profile_pic": "pic",  # image
}

headers = [
    "Name",
    "Email",
    "Phone",
    "Address",
    "City",
    "State",
    "Zipcode",
    "Website",
    "Facebook",
    "Instagram",
    "Other social media",
    "Profile picture",
    "Bio",
    "Languages",
    "Remuneration",
    "Services",
    "Also available in states",
    "Editing style",
    "Specialites",
    "Source",
]

with open("states.json") as f:
    states = json.load(f)


def get_us_urls():
    united_states_links = []
    with requests.get(url) as r:
        r.raise_for_status()
        soup = BeautifulSoup(r.content, "html.parser")
        for data in soup.find_all("div", class_="region-listing"):
            if data.find("h2").text == "UNITED STATES":
                for h in data.find_all("a"):
                    united_states_links.append(f"{main_url}{h.get('href')}")
    print("Completed getting state urls")
    return united_states_links


def get_photographers_url():
    us_links = get_us_urls()
    profiles = []
    for i, links in enumerate(us_links):
        print(f"({i+1}/{len(us_links)}) Checking: {links}")
        with requests.get(links) as r:
            r.raise_for_status()
            soup = BeautifulSoup(r.content, "html.parser")
            profile = soup.find("div", class_=classes["profile_link"])
            if profile:
                for user in soup.find_all("a"):
                    url = user.get("href")
                    if str(url).startswith("/photographer/"):
                        profiles.append(f"{main_url}{url}")
    time.sleep(0.6)
    return profiles


def scrape_contact_info(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract email addresses
        email_addresses = re.findall(
            r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", soup.get_text()
        )

        # Extract phone numbers (simple regex, adjust based on the format used on the websites)
        phone_numbers = re.findall(
            r"\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b", soup.get_text()
        )
        print("Got email phone from: ", url)
        data = {
            "email_addresses": email_addresses,
            "phone_numbers": phone_numbers,
        }
        return data
    else:
        print(
            f"Failed to fetch content from {url}. Status code: {response.status_code}"
        )
        return None


def get_photographer_info(photographers_url):
    photgrapher_details = []
    for i, links in enumerate(photographers_url):
        info = {key: "" for key in headers}
        print(f"({i+1}/{len(photographers_url)}) Checking: {links}")
        with requests.get(links) as r:
            r.raise_for_status()
            soup = BeautifulSoup(r.content, "html.parser")
            name = soup.find("h1", class_=classes["name"])
            if not name:
                continue
            name = name.text
            infos = soup.find("div", class_=classes["info"])
            bio = soup.find("div", class_=classes["bio"])
            profile_picture = soup.find("div", class_=classes["profile_pic"])
            if profile_picture:
                profile_picture = f"{main_url}{profile_picture.find('img').get('src')}"
            city = ""
            facebook = ""
            website = ""
            instagram = ""
            for data in infos.find_all("a"):
                link = str(data.get("href"))
                if link.startswith("/location/"):
                    city = data.text.split()[-1] if link else ""
                if data.get("title") == "Website":
                    website = link
                if data.get("title") == "Facebook":
                    facebook = link
                if data.get("title") == "Instagram":
                    instagram = link
            get_states = (soup.find("div", id="breadcrumb").find_all("a")[2]).text or ""
            info["State"] = ""
            for state in states:
                if str(state["name"]).strip() == get_states.strip():
                    info["State"] = state["abbreviation"]
            info["Name"] = name if name else ""
            try:
                email_phone = scrape_contact_info(website)
                info["Email"] = email_phone["email_addresses"][-1] if email_phone.get("email_addresses", "") else ""
                info["Phone"] = email_phone["phone_numbers"][-1] if email_phone.get("phone_numbers", "") else ""
            except Exception as e:
                info["Email"] = ""
                info["Phone"] = ""

            print("Email: ", info["Email"], "Phone: ", info["Phone"])
            info["City"] = city
            info["Website"] = website
            info["Facebook"] = facebook
            info["Instagram"] = instagram
            info["Bio"] = bio.text.strip().replace("\xa0", "").replace("\n", "") if bio else ""
            info["Source"] = links
            info["Profile picture"] = profile_picture
            photgrapher_details.append(info)

        time.sleep(0.5)
    print()
    return photgrapher_details


def clean_spread_sheet(worksheet, columns):
    for column in worksheet.columns:
        col_letter = get_column_letter(column[0].column)

        max_length = 0
        for cell in column:
            try:
                if cell.value is not None:
                    cell_length = len(str(cell.value))
                    max_length = max(max_length, cell_length)
            except TypeError:
                pass

        if col_letter in columns:
            for cell in column[1:]:
                link_url = cell.value
                if link_url:
                    hyperlink = Hyperlink(ref=link_url, target="External")
                    cell.hyperlink = hyperlink

        if col_letter == "M":
            worksheet.column_dimensions[col_letter].width = max_length // 8

        worksheet.column_dimensions[col_letter].width = max_length + 1


def upload_to_excel(data, excel_file, sheetname):
    df = pd.DataFrame(data)
    try:
        if not os.path.isfile(excel_file):
            print("Writing to excel")
            df.to_excel(excel_file, index=False, engine="xlsxwriter", sheet_name=sheetname)
            print("Completed writing to excel")
        with pd.ExcelWriter(excel_file, engine="openpyxl", mode="a") as writer:
            clean_spread_sheet(writer.sheets[sheetname], ["H", "I", "J", "L", "T"])
    except Exception as e:
        print(f"Error: {e}")


def main():
    try:
        with open("fearles_urls.txt", "r") as file:
            profiles = file.read().splitlines()
    except FileNotFoundError:
        profiles = get_photographers_url()
        with open("fearles_urls.txt", "w") as file:
            file.write("\n".join(profiles))

    data = get_photographer_info(profiles)
    excel_file = "fearless.xlsx"
    upload_to_excel(data, excel_file, sheetname="fearlessphotographers")


if __name__ == "__main__":
    main()
