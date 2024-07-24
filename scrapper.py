import requests
from bs4 import BeautifulSoup
import time
import pandas as pd

from openpyxl.styles import Alignment
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.hyperlink import Hyperlink

import json
from city_to_state_dictionary import city_to_state_dict

import os


global_url = "https://mywed.com/en/United-States-wedding-photographers/"
user_url = "https://mywed.com/en/photographer/"

classes = {
    "name": "profile-new-head-user__name",
    "nickname": "expert-name__item expert-name__nickname",
    "website": "profile-new-head-site",
    "location": "profile-new-head-user__place",
    "phone_number": "profile-new-head-btn profile-new-head-btn__phone profile-new-head-btn__ghost",
    "bio": "profile-new-head-info__text",
    "language": "profile-new-head-languages",
    "achievements": "profile-new-place-links__desc",
    "speciality": "mw-categories__link",
    "remuneration": "mw-categories__item",
    "experience": "profile-new-head-standing",
}


with open("states.json") as states_abr:
    states = json.load(states_abr)


def get_photographer_profile_urls():
    num_pages = 137
    photographer_urls = []
    for i in range(1, num_pages):
        url = f"{global_url}p{i}" if i != 1 else global_url
        print("Getting url: ", url)
        try:
            with requests.get(url) as r:
                r.raise_for_status()  
                soup = BeautifulSoup(r.content, "html.parser")
                user_names = soup.find_all("span", class_=classes["nickname"])
                photographer_urls.extend(
                    [f"{user_url}{name.text}/" for name in user_names]
                )
        except requests.RequestException as e:
            print(f"Error fetching URLs for page {i}: {e}")
        time.sleep(1)
    return photographer_urls


def get_photographer_info(photographer_urls):
    photographer_info = []
    for i, nickname in enumerate(photographer_urls, start=1):
        url = str(nickname)
        try:
            with requests.get(url) as r:
                r.raise_for_status()
                soup = BeautifulSoup(r.content, "html.parser")

                info = {}

                user_name = soup.find("h1", class_=classes["name"])
                if user_name:
                    print(f"({i}/{len(photographer_urls)}) Checking {url} - Found")
                else:
                    print(
                        f"({i}/{len(photographer_urls)}) Checking {url} - User Not Found"
                    )
                location = soup.find("p", class_=classes["location"])
                if location:
                    location = (
                        location.find("span").text if location.find("span") else ""
                    )
                website = soup.find("a", class_=classes["website"])
                if website:
                    website = website.get("href")
                phone_number = soup.find("a", class_=classes["phone_number"])
                if phone_number:
                    phone_number = (
                        phone_number.find("meta").get("content")
                        if phone_number.find("meta")
                        else ""
                    )
                    phone_number = phone_number if phone_number.startswith("+1") else ""
                bio = (
                    soup.find("p", class_=classes["bio"]).text
                    if soup.find("p", class_=classes["bio"])
                    else ""
                )
                languages = soup.find("div", class_=classes["language"])
                if languages:
                    languages = (
                        languages.find("span").text if languages.find("span") else ""
                    )
                achievements = [
                    (
                        achievement.text
                        if soup.find_all("a", class_=classes["achievements"])
                        else ""
                    )
                    for achievement in soup.find_all(
                        "a", class_=classes["achievements"]
                    )
                ]
                specialities = [
                    (
                        speciality.text
                        if soup.find_all("a", class_=classes["speciality"])
                        else ""
                    )
                    for speciality in soup.find_all("a", class_=classes["speciality"])
                ]
                for i, val in enumerate(specialities):
                    if val.split(":")[-1]:
                        specialities[i] = val.split(":")[-1]
                remuneration = soup.find_all("li", class_=classes["remuneration"])
                rem_text = []
                if remuneration:
                    for i in remuneration:
                        txt = ""
                        price = int(float(i.get("data-category-price-usd")))
                        category = i.get("data-category-cost-text")
                        if price > 0:
                            if price % 5 != 0:
                                price += 5 - price % 5
                            txt += f"{category}: {price} USD per hour"
                        rem_text.append(txt)

                experience = soup.find("div", class_=classes["experience"])
                if experience:
                    experience = (
                        (experience.find("span").text).replace("on MyWed", "").strip()
                        if experience.find("span")
                        else ""
                    )
                profile_pic_find = soup.find("image", id="profile-userpic")
                profile_pic = ""
                if profile_pic_find:
                    profile_pic = profile_pic_find.get("xlink:href")

                info["Name"] = " ".join(user_name.text.strip().split()[1:]) or ""
                info["Email"] = ""
                info["Phone"] = phone_number or ""
                info["Address"] = ""
                info["City"] = (location.replace("\xa0PRO", "")).split(",")[0] or ""

                info["State"] = ""
                for state in states:
                    st = city_to_state_dict.get(str(info["City"]).strip(), "")
                    if (
                        str(state["name"]).strip().lower()
                        == str(info["City"]).strip().lower()
                    ):
                        info["State"] = state["abbreviation"]
                    else:
                        if st:
                            if str(state["name"]).strip().lower() == st.lower():
                                info["State"] = state["abbreviation"]
                info["Zipcode"] = ""
                info["Website"] = website or ""
                info["Facebook"] = ""
                info["Instagram"] = ""
                info["Other Social media"] = ""
                info["Profile picture"] = profile_pic
                info["Bio"] = bio or ""

                info["Languages"] = (
                    [
                        lang.strip().title().rstrip(".")
                        for lang in languages.replace("I can speak", "")
                        .strip()
                        .split(",")
                    ]
                    if languages
                    else ""
                )
                info["Remuneration"] = rem_text or ""
                info["Services"] = ""
                info["Also available in states"] = ""
                info["Editing Style"] = ""
                info["Specialities"] = specialities or ""
                info["Source"] = url
                info["Achievements"] = achievements or ""
                info["Experience"] = experience or ""
                photographer_info.append(info)

        except requests.RequestException as e:
            print(f"Error fetching info for {url}: {e}")

        time.sleep(0.2)

    return photographer_info


def adjust_column_width_and_wrap(worksheet, wrap_columns, link_columns):
    for column in worksheet.columns:
        max_length = 0
        for cell in column:
            try:
                if cell.value is not None:
                    cell_length = len(str(cell.value))
                    max_length = max(max_length, cell_length)
            except TypeError:
                pass

        adjusted_width = max_length + 2
        col_letter = get_column_letter(column[0].column)
        if col_letter not in wrap_columns:
            worksheet.column_dimensions[col_letter].width = adjusted_width
        else:
            if col_letter == "S":
                worksheet.column_dimensions[col_letter].width = adjusted_width // 2
            elif col_letter == "M":
                worksheet.column_dimensions[col_letter].width = adjusted_width // 6
            else:
                worksheet.column_dimensions[col_letter].width = adjusted_width // 4

        if col_letter in wrap_columns:
            for cell in column[1:]:
                cell.alignment = Alignment(wrap_text=True)

        if col_letter in link_columns:
            for cell in column[1:]:
                link_url = cell.value
                if link_url:
                    hyperlink = Hyperlink(ref=link_url, target="External")
                    cell.hyperlink = hyperlink


def to_excel(data, sheetname, excel_file):
    df = pd.DataFrame(data)

    df["Languages"] = df["Languages"].str.join(", ")
    df["Achievements"] = df["Achievements"].str.join("\n")
    df["Specialities"] = df["Specialities"].str.join(", ")
    df["Remuneration"] = df["Remuneration"].str.join("\n")

    wrap_columns = ["M", "U", "O", "S"]
    link_columns = ["L", "H", "T"]

    if not os.path.isfile(excel_file):
        df.to_excel(excel_file, index=False, engine="openpyxl", sheet_name=sheetname)

    with pd.ExcelWriter(excel_file, engine="openpyxl", mode="a") as writer:
        adjust_column_width_and_wrap(
            writer.sheets[sheetname], wrap_columns, link_columns
        )


def main():
    try:
        with open("photographer_urls.txt", "r") as file:
            photographer_urls = file.read().splitlines()
    except FileNotFoundError:
        photographer_urls = get_photographer_profile_urls()
        with open("photographer_urls.txt", "w") as file:
            print("writing to file")
            file.write("\n".join(photographer_urls))
    batch_size = 1500
    count = 0
    for i in range(0, len(photographer_urls), batch_size):
        photographer_info_one = get_photographer_info(
            photographer_urls[i : i + batch_size]
        )
        excel_file = f"myWed_{count}.xlsx"
        print("Writing to excel")
        to_excel(photographer_info_one, "myWed.com", excel_file)
        print("Completed")
        count += 1


if __name__ == "__main__":
    main()
