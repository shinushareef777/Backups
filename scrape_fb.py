from bs4 import BeautifulSoup
import re

from selenium import webdriver
from selenium.webdriver.common.by import By

import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
import os
import pandas as pd
from selenium.webdriver.chrome.options import Options


df = pd.read_excel("./PhotographersDirectoryFinal.xlsx", sheet_name="Sheet1")


def get_empty_email():
    sheet = df[(df["email"].isna() | df["phone"].isna()) & ~df["facebook"].isna()][
        ["email", "phone", "facebook"]
    ]

    return sheet


def write_to_txt(url):
    with open("fburls.txt", "a") as file:
        file.write(str(url) + "\n")


def get_fb_data(data):
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Uncomment to run in headless mode

    count = 1

    for index, row in data.iterrows():
        fb_url = row["facebook"]
        # name = row["name"]
        print(f"Checking ({count}/{data.shape[0]}): {fb_url}")

        count += 1

        facebook_pattern = re.compile(r"(?i)(fb\.com|facebook\.com)")
        match = bool(re.search(facebook_pattern, fb_url))
        if not match:
            # print("Invalid URL:", fb_url)
            # write_to_txt(fb_url)
            continue

        if fb_url.startswith("www.facebook.com"):
            fb_url = "http://" + fb_url


        driver = webdriver.Chrome(options=chrome_options)
        try:
            driver.get(fb_url)
        except Exception as e:
            write_to_txt(fb_url)
            print("Error opening URL:")
            continue

        time.sleep(1)  # Wait for the page to load

        if is_login_required(driver):
            try:
                login(driver)
            except Exception as e:
                write_to_txt(fb_url)
                print("Error during login:")
                driver.quit()
                continue

        try:
            email, phone_number = extract_contact_info(driver)
            update_dataframe(df, index, email, phone_number)
        except Exception as e:
            write_to_txt(fb_url)
            print("Error extracting contact info:")

        driver.quit()
        print()


def is_login_required(driver):
    soup = BeautifulSoup(driver.page_source, "html.parser")
    return soup.find("div", {"class": "x4l50q0"}) or soup.find(
        "form", {"id": "login_form"}
    )


def login(driver):
    # Replace with your own login credentials or use environment variables
    email = "youremail"
    password = "yourpassword"

    username_box = driver.find_element(By.ID, "email")
    username_box.send_keys(email)
    print("Email entered")

    password_box = driver.find_element(By.ID, "pass")
    password_box.send_keys(password)
    print("Password entered")

    login_box = driver.find_element(By.ID, "loginbutton")
    login_box.click()
    print("Login completed")

    time.sleep(1)  # Wait for the page to load after login


def extract_contact_info(driver):
    soup = BeautifulSoup(driver.page_source, "html.parser")
    items = soup.find("div", {"class": "x1yztbdb"})

    email = ""
    phone_number = ""

    if items:
        all_details = items.find("ul") or items.find_all("ul")

        for contact in all_details:
            email_addresses = re.findall(
                r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", contact.text
            )
            phone_numbers = re.findall(
                r"\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b", contact.text
            )

            if email_addresses:
                email = email_addresses[0]
                print("--> Got email -->", email)

            if phone_numbers:
                phone_number = f"+1 {''.join(phone_numbers[0])}"
                print("--> Got phone number", phone_number)

    return email, phone_number


def update_dataframe(data, index, email, phone_number):
    if pd.isna(data.at[index, "email"]) and email:
        data.at[index, "email"] = email
    if pd.isna(data.at[index, "phone"]) and phone_number:
        data.at[index, "phone"] = phone_number


def add_to_excel(excel_file, sheet_name, df):

    # Check if the Excel file already exists
    if os.path.isfile(excel_file):
        print(f"Appending data to existing file: {excel_file}")

        # Open the existing Excel file in append mode
        with pd.ExcelWriter(excel_file, engine="openpyxl", mode="a") as writer:
            # Create a DataFrame from your data (replace fb_data with your actual data)
            df = pd.DataFrame(df)

            # Write the DataFrame to a new sheet in the existing Excel file
            df.to_excel(writer, index=False, sheet_name=sheet_name)

        print(f"Completed appending data to sheet: {sheet_name}")
    else:
        print("File does not exist. Creating a new file.")
        df = pd.DataFrame(df)
        df.to_excel(excel_file, index=False, engine="xlsxwriter", sheet_name=sheet_name)
        print(f"Completed writing to new sheet: {sheet_name}")


def main():

    batch_size = 15000
    num_batches = (len(df) // batch_size) + 1

    print("Num batches ---> ", num_batches)

    # Iterate over batches
    # for i in range(num_batches):
    #     start_index = i * batch_size
    #     end_index = (i + 1) * batch_size

    #     # Extract a batch of data
    #     batch_df = df.iloc[start_index:end_index]

    data = get_empty_email()
    get_fb_data(data)

        # Call the function to add the batch to the Excel file
        # add_to_excel(
        #     "PhotographersDirectoryNew.xlsx",
        #     f"Sheet{i}",
        #     batch_df
        # )
        # print(f"Completed adding batch {i + 1} to the Excel file.")


if __name__ == "__main__":
    main()
