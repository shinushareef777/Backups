import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import urljoin, urlparse
import uuid


def download_image(url, folder, counter):
    if not os.path.isdir(folder):
        os.makedirs(folder)

    # Generate a unique identifier
    unique_id = uuid.uuid4().hex

    # Extract the file extension from the URL
    parsed_url = urlparse(url)
    file_extension = os.path.splitext(parsed_url.path)[1]

    # Create a new file name
    file_name = f"{counter}_{unique_id}{file_extension}"
    file_path = os.path.join(folder, file_name)

    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(file_path, "wb") as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        print(f"Image successfully downloaded: {file_path}")
    else:
        print(f"Failed to download image: {url}")


def get_images_from_website(url, folder="images"):
    # Set up Selenium WebDriver
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=options
    )

    driver.maximize_window()

    # Load the webpage
    driver.get(url)
    time.sleep(5)  # Let the page load

    # Scroll to the div with the class "js-images"
    js_images_div = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "js-images"))
    )
    driver.execute_script("arguments[0].scrollIntoView();", js_images_div)
    time.sleep(2)  # Wait for the content to load

    # Find all image elements within the "js-images" div
    img_tags = js_images_div.find_elements(By.TAG_NAME, "img")

    counter = 1

    # Loop through each image tag and process it
    for img_index in range(len(img_tags)):
        try:
            # Click the image to open the high-resolution version
            img_tags[img_index].click()
            time.sleep(3)  # Wait for the high-resolution image to load

            while True:
                # Extract the high-resolution image URL
                high_res_img = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.TAG_NAME, "img"))
                )
                high_res_url = high_res_img.get_attribute("src")
                full_url = urljoin(url, high_res_url)

                # Download the high-resolution image
                download_image(full_url, folder, counter)
                counter += 1

                # Try to find and click the next button
                try:
                    next_button = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable(
                            (
                                By.CSS_SELECTOR,
                                ".buttons_button__KzDvP.image-card_image-card__navigator-semi-circle-btn--right__0ZMJ5",
                            )
                        )
                    )
                    next_button.click()
                    time.sleep(3)  
                except Exception as e:
                    print(f"No more images or error finding next button: {e}")
                    break

            # Close the high-resolution image view (if there's a close button, else navigate back)
            driver.back()
            time.sleep(2)  # Wait for the gallery view to load again

            # Refresh the img_tags list to avoid stale element reference
            img_tags = js_images_div.find_elements(By.TAG_NAME, "img")

        except Exception as e:
            print(f"Error processing image: {e}")
            continue

    driver.quit()


if __name__ == "__main__":
    website_url = (
        # "https://playbackweddings.premagic.com/share/f96g8xJlTAmRD70-CNndmQ/#/" #wedding
        # "https://playbackweddings.premagic.com/share/WJP4swc7Tfimj9nnPcFhKg/#/" #reception
        # "https://playbackweddings.premagic.com/share/o-SmsySWQtabSs74XYQPDQ/#/"  # haldi
        # "https://playbackweddings.premagic.com/share/_lil171jRU2TflYePyWXFQ/#/" #pre-wedding
        # "https://playbackweddings.premagic.com/share/NM6K9yqLQ_uasHOs1Wf9YA/#/" # temple shooting - M
        "https://playbackweddings.premagic.com/share/JZimT6TKTEi-r_CfmjeXhw/#/" # temple-shooting - F
    )
    download_folder = "images"
    get_images_from_website(website_url, download_folder + "/temple-shooting")
