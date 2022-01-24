"""
Script to download your files from Google Drive to the local disk.
Usage:
Required Arguments:-
--mail_id mail id of the user
--password password of the user
--filename name of the file to be downloaded
Note: The code is currently written to download files from one's own google-drive to their loca drive
"""
import os
import argparse
from keyboard import press
from selenium import webdriver
from selenium.webdriver import ActionChains


def download_file():
    """Download your files from Google Drive to the local disk."""
    # Initialize parser
    parser = argparse.ArgumentParser()

    # Adding optional argument
    parser.add_argument("--mail_id", help="Mail ID of the user")
    parser.add_argument("--password", help="Password of the user")
    parser.add_argument("--filename",
                        help="Name of the file to download to local drive, "
                             "if space exists in filename please replace it with -")
    parser.add_argument("--path", help="Path of the geckodriver")

    # Read arguments from command line
    args = parser.parse_args()

    # Replace - in filename with space
    if "-" in args.filename:
        args.filename = args.filename.replace("-", " ")

    # Load Chrome and launch browser
    driver = webdriver.Chrome(executable_path=fr'{args.path}')
    driver.get("https://drive.google.com/drive/u/0/my-drive")

    # Enter the mail ID given by the user
    mail_id_input_box = driver.find_element(by="xpath", value="//input[@type='email']")
    mail_id_input_box.send_keys(args.mail_id)
    driver.find_element(by="xpath", value="//*[@id='identifierNext']").click()

    # Enter the password given by the user
    password_id_input_box = driver.find_element(by="xpath", value="//input[@type='password']")
    password_id_input_box.send_keys(args.password)
    driver.find_element(by="xpath", value="//*[@id='identifierNext']").click()

    # Search for the given file name in browser
    driver.find_element(by="xpath", value="//input[@aria-label='Search in Drive']").send_keys(args.filename)
    press('enter')

    # Right-click on the file and click download
    action = ActionChains(driver)
    download_menu = driver.find_element(by="xpath",
                                        value="//*[@id=':47.14y2WF6tD-3rdiX5tGp6upHWl3SI2xu5cUNnkcn6QQ3c']"
                                              "/div[2]/div[2]/div/div/div[1]")
    action.context_click(download_menu)
    driver.find_element(by="xpath", value="//*[@id='Download']").click()

    # Close the browser
    driver.quit()

    # Check if the downloaded file is present in the local drive
    os.path.isfile(args.filename)


if __name__ == "__main__":
    download_file()
