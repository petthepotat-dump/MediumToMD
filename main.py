import os
import sys
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
import time
import requests

from selenium.webdriver.common.by import By


# ----------------------------------
intel = "chromedriver-intel"
arm64 = "chromedriver-arm64"

# detect if os uses arm64 or 32bit, mac silicon, or mac m chip

# check if windows or mac
if sys.platform == "win32":
    tt = intel
elif sys.platform == "darwin":
    if os.uname().machine == "x86_64":
        # intel
        print("Intel detected")
        tt = intel
    elif os.uname().machine == "arm64":
        # mac silicon
        print("Mac Silicon detected")
        tt = arm64


driver = webdriver.Chrome(tt)
# get article link
# link = input("Input Article Link: ")
# link = "https://dariusforoux.medium.com/protect-your-thinking-time-if-you-want-to-stay-productive-d66e63825d05"
# link = "https://jackiecolburn.medium.com/more-icebreakers-you-can-steal-for-better-meetings-72afad91067d"


def convert_to_css_selector(selector):
    return ".".join(selector.split())

# ----------------------------------


class Header:
    def __init__(self, text, priority=1):
        self.text = text
        self.priority = priority

    def to_markdown(self):
        return f"{'#'*self.priority} {self.text}"


class Paragraph:
    def __init__(self, text):
        self.text = text

    def to_markdown(self):
        return self.text


class List:
    def __init__(self, items):
        self.items = items

    def to_markdown(self):
        return "\n".join([f"- {item}" for item in self.items])


class Quote:
    def __init__(self, text):
        self.text = text

    def to_markdown(self):
        return f"```{self.text}```\n"


class Image:
    def __init__(self, filelink, link=None):
        self.flink = filelink
        self.link = link

    def to_markdown(self):
        return f"![Image]({self.flink})" if not self.link else f"![Image]({self.link})"

# ----------------------------------


class GetInformation:
    # functions for grabbing data
    # all functions have
    # `element`: the element to get data from -- parent div / p / figure / etc

    # ----------------------------------
    # auto determine which header
    @staticmethod
    def geth(element):
        # check if h1 or h2 if there is only one child elemnet
        try:
            # assuming h1
            return GetInformation.geth1(element.find_element(By.TAG_NAME, "h1"))
        except:
            # assuming h2
            return GetInformation.geth2(element.find_element(By.TAG_NAME, "h2"))

    @staticmethod
    def geth1(element):
        # get h1
        h1 = element.text
        return Header(text=h1, priority=1)

    @staticmethod
    def geth2(element):
        # get h2
        h2 = element.text
        return Header(text=h2, priority=2)

    # ----------------------------------
    # get paragraph
    @staticmethod
    def getp(element):
        # element is a p object
        return Paragraph(element.text)

    # ----------------------------------
    # get images
    @staticmethod
    def getimage(element, folderpath):
        # get picture object
        picture = element.find_element(By.TAG_NAME, "picture")
        # grab image link
        image = picture.find_element(By.TAG_NAME, "img").get_attribute("src")
        # get iamge name
        name = image.split("/")[-1][2:]
        # check if "assets" exists
        if not os.path.exists(os.path.join(folderpath, "assets")):
            os.mkdir(os.path.join(folderpath, "assets"))
        # check if "images" exists
        if not os.path.exists(os.path.join(folderpath, "assets/images")):
            os.mkdir(os.path.join(folderpath, "assets/images"))
        # create image path
        imagepath = os.path.join(folderpath, "assets/images/", name)
        # download image to folder using requests
        response = requests.get(image)
        if response.status_code == 200:
            with open(imagepath, "wb") as f:
                f.write(response.content)
                print("Image downloaded successfully.")
        else:
            print("Failed to download image.")

        return Image(os.path.relpath(imagepath, "assets"), image if response.status_code != 200 else None)

    # ----------------------------------
    # get quotes
    @staticmethod
    def getquote(element):
        # get quote
        quote = element.text
        return Quote(quote)

    # ----------------------------------
    # get lists
    @staticmethod
    def getlist(element):
        # get all li elements
        lis = element.find_elements(By.TAG_NAME, "li")
        # get text from each li
        listtext = [li.text for li in lis]
        # return list
        return List(listtext)

# ----------------------------------
<<<<<<< HEAD
=======


# load page
driver.get(link)
# wait for other things to load
print("Pausing for other sections to load")
time.sleep(3)
>>>>>>> 295deeb8dd3e057892cab2dc1d444b10bfa9bd87


def load_page(url, driver):
    driver.get(url)
    # wait for page to load
    time.sleep(3)
    
# check if product exists
if not os.path.exists("product"):
    os.mkdir("product")

# TODO -- add in videos + other custom things

def save_to_markdown(url, driver):
    load_page(url, driver)
    # remove config and header from link
    link = url.split("?")[0]

    name = "-".join(link.split("/")[-1].split('-')[:-1])
    filepath = "product/" + name + ".md"
    # collect all information and save to markdown file
    statsdiv = driver.find_element(By.CLASS_NAME, convert_to_css_selector("pw-post-byline-header"))
    authordiv = statsdiv.find_element(By.CLASS_NAME, convert_to_css_selector("pw-author"))
    author = authordiv.text

    # FOR non memebr
    # find the article tag
    article = driver.find_element(By.TAG_NAME, "article")
    section = article.find_element(By.TAG_NAME, "section")
    # get first div
    main = section.find_element(By.TAG_NAME, "div")
    # get second child div
    container = main.find_element(By.XPATH, "./*[2]")

    file = open(filepath, "w")
    folderpath = os.path.dirname(filepath)
    # TODO -- determine if more stats required -- date created, etc
    # print("if want to , write more collection code~!")
    file.write(f"# Author Information\nAuthor: {author}\n\n")

    # instead of printint to console, write to file'
    # get all elements in first level of container
    skip = 0
    for i, elem in enumerate(container.find_elements(By.XPATH, ".//*")):
        if skip > 0:
            skip -= 1
            continue
        # check if element is: p, div, ul, blockquote, or figure
        if elem.tag_name == "p":
            file.write(GetInformation.getp(elem).to_markdown())
        elif elem.tag_name == "h1":
            file.write(GetInformation.geth1(elem).to_markdown())
        elif elem.tag_name == "h2":
            file.write(GetInformation.geth2(elem).to_markdown())
        elif elem.tag_name == "ul":
            file.write(GetInformation.getlist(elem).to_markdown())
        elif elem.tag_name == "blockquote":
            file.write(GetInformation.getquote(elem).to_markdown())
            skip += 1
        elif elem.tag_name == "figure":
            file.write(GetInformation.getimage(elem, folderpath).to_markdown())
        file.write("\n")

    file.close()


# ----------------------------------

# DATA = input("Enter link/links: ")
DATA = open("links", "r").read()
for url in DATA.splitlines():
    save_to_markdown(url, driver)



# actually save the file to markdown
save_to_markdown(link, driver)
