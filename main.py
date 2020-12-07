from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
import urllib.request
from PIL import Image
import cairosvg
from PyPDF2 import PdfFileMerger
import os
from PIL import Image

# Initiate the browser
browser = webdriver.Chrome(ChromeDriverManager().install())

# Open the Website
music_url = input("Enter the piece's URL: ")
save_location = ""
# save_location = "/Users/mayankjain/Documents/Sheet Music/"
browser.get(music_url)

input("Press Enter after all pages have rendered")
print("Page Loaded")

music_title = browser.find_element_by_css_selector('h1').text

pages = browser.find_elements_by_class_name('gXB83')


# for i, page in enumerate(pages):
#     browser.execute_script("return arguments[0].scrollIntoView(true);", page)
#     sleep(.5)

#     img = page.find_element_by_css_selector('img')
#     img_url = img.get_attribute('src')

#     img_url_cleaned = img_url[:img_url.find(
#         '.', img_url.find('scoredata')+1)] + '.png'

#     # print(img)
#     img_location = (save_location + music_title + "_" + str(i) + ".png")


urls = []
for i, page in enumerate(pages):
    browser.execute_script("return arguments[0].scrollIntoView(true);", page)
    sleep(.5)

    img = page.find_element_by_css_selector('img')
    img_url = img.get_attribute('src')

    if i == 0:
        img_url_cleaned = img_url[:img_url.find(
            '.', img_url.find('scoredata')+1)] + '.png'
        urls.append(img_url_cleaned)
    else:
        urls.append(img_url)

    # print(img, img_url)

print("Image URLs Found")


music_pages = []
for i, url in enumerate(urls):
    print(i)
    img_location = (save_location + music_title + "_" + str(i) + ".png")

    file_type = ""
    if "jpg" in url:
        file_type = "jpg"
    elif "png" in url:
        file_type = "png"
    elif "svg" in url:
        file_type = "svg"

    if i == 0:
        urllib.request.urlretrieve(url, img_location)
        pdf_place = img_location[:-3]+"pdf"
        # PNG to PDF
        Image.open(img_location).convert('RGB').save(pdf_place)
        music_pages.append(pdf_place)
    else:
        browser.get(url)
        sleep(.5)
        old_place = "/Users/mayankjain/Downloads/score_"+str(i)+"." + file_type
        new_place = save_location+music_title+"_"+str(i)+"."+file_type
        pdf_place = (new_place[:-3]+"pdf")
        os.rename(old_place, new_place)
        if file_type == "svg":
            cairosvg.svg2pdf(url=new_place, write_to=pdf_place)
        else:
            Image.open(new_place).convert('RGB').save(pdf_place)
        music_pages.append(pdf_place)
        os.remove(new_place)

print("Images downloaded")

merger = PdfFileMerger()

for pdf in music_pages:
    merger.append(pdf)

merger.write(save_location + music_title+".pdf")
merger.close()

for pdf in music_pages:
    os.remove(pdf)

browser.close()

print("PDF Created")
