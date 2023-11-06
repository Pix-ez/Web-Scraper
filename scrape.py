from selenium import webdriver
from bs4 import BeautifulSoup
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
import time
import csv
import argparse


# Initialize the Parser 
parser = argparse.ArgumentParser(description ='take mode to run!.') 
#Default open window of browser
parser.add_argument('--window', action='store_false', help='Run in headless mode', default=True )
parser.add_argument('--url', type=str, help='Specify the URL')

args = parser.parse_args()

# Your Instagram session ID
session_id = 'Your Session ID'


# url = 'https://www.instagram.com/reel/Cyrt3azoBWX/?utm_source=ig_web_copy_link'


if args.url:
    url = args.url
else:
    # print("specify url")
    url = 'https://www.instagram.com/reel/Cyrt3azoBWX/?utm_source=ig_web_copy_link'


path  = 'D:\chromedriver\chromedriver.exe'

# Set the HEADLESS_MODE flag based on the command line argument
HEADLESS_MODE = args.window
# Create ChromeOptions for headless 

if HEADLESS_MODE:
  chrome_options = Options()
  chrome_options.add_argument('--headless')
  chrome_options.add_argument('--disable-gpu')
  chrome_options.add_argument('--window-size=1920x1080')
  driver = webdriver.Chrome(path, options=chrome_options)
else:
    driver = webdriver.Chrome(path)


driver.get(url)

time.sleep(5)

# Add the sessionid cookie
driver.add_cookie({'name': 'sessionid', 'value': session_id, 'domain': '.instagram.com'})

# Refresh the page to apply the cookie
driver.refresh()


# # # driver.quit()
time.sleep(7)



script = """
var commentsContainer = document.querySelector("[class^='x5yr21d xw2csxc x1odjw0f x1n2onr6']");
var previousScrollHeight = 0;
var currentScrollHeight = -1;
var timeoutCounter = 0;

function scrollToEnd() {
    commentsContainer.scrollTop = commentsContainer.scrollHeight;
    currentScrollHeight = commentsContainer.scrollTop;

    if (currentScrollHeight !== previousScrollHeight) {
        previousScrollHeight = currentScrollHeight;
        timeoutCounter = 0;
        setTimeout(scrollToEnd, 3000); // Scroll again after 1 second
    } else if (timeoutCounter < 10) {
        // If no change in scroll height, and timeout counter is less than 10, wait and try again
        timeoutCounter++;
        setTimeout(scrollToEnd, 1000); // Wait for 1 second and try again
    }
}

scrollToEnd();
"""

#scroll
driver.set_script_timeout(120)
driver.execute_script(script)
# time.sleep(3)

# Wait for stability in page content
previous_page_source = None
stability_counter = 0

while stability_counter < 5:  # Adjust the number of checks as needed
    time.sleep(3)  # Adjust the sleep time as needed
    current_page_source = driver.page_source

    if current_page_source == previous_page_source:
        stability_counter += 1
    else:
        stability_counter = 0

    previous_page_source = current_page_source


# # # Get the page source
page_source = driver.page_source

# Parse the page source with BeautifulSoup
soup = BeautifulSoup(page_source, 'html.parser')

# Find comments using the appropriate XPath
comments = soup.findAll("span", {"class": "x1lliihq x1plvlek xryxfnj x1n2onr6 x193iq5w xeuugli x1fj9vlw x13faqbe x1vvkbs x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x1i0vuye xvs91rp xo1l8bm x5n08af x10wh9bi x1wdrske x8viiok x18hxmgj"})


csv_file_name = "data.csv"

comments_data = []
# Extract and print the comment text
for comment in comments:
    comments_data.append(comment.text)
    # print(comment.text)

comment_data = comments_data[1:-1]
print(comments_data)

data=[]
for i in range(len(comments_data)-1):
    if (i%2!=0):
        data.append({"name":comments_data[i], "comment":comments_data[i+1]})

        # print(f'name-{comments_data[i]} , comm-{comments_data[i+1]}')
       


with open(csv_file_name, mode='w', newline='',encoding='utf-8') as csv_file:
    fieldnames = ["name", "comment", ]
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    
    # Write the header row
    writer.writeheader()
    
    # Write the data rows
    for row in data:
        writer.writerow(row)

print(f"CSV file '{csv_file_name}' created successfully.")

##Close the WebDriver when you're done
# driver.quit()


