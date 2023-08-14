from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import sqlite3

conn = sqlite3.connect('deneme.db')
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS tagler")
cursor.execute("CREATE TABLE tagler(tag text)")
add_command = """INSERT INTO tagler VALUES(?)"""

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    context.grant_permissions(['clipboard-read'])
    web_site = "https://www.shutterstock.com"

    veri_turu = 'vector'
    input_degeri = 'ağaç'
    arama_sayisi = 50

    if veri_turu == "vector" or veri_turu =="photo" or veri_turu == "illustration":
        url = web_site + "/tr/search/" + input_degeri + "?image_type=" + veri_turu + "&page="
    elif veri_turu == "editorial image":
        url = web_site + "/tr/editorial/search/" + input_degeri + "&page="
    elif veri_turu == "editorial video":
        url = web_site + "/tr/editorial/video/search/" + input_degeri + "&page="
    elif veri_turu == "video":
        url = web_site + "/tr/video/search/" + input_degeri + "&page="

    page = context.new_page()
    i = 0
    sayfa_sayaci = 1
    page.goto(url + str(sayfa_sayaci))
    page.mouse.wheel(0, 10000)
    html = page.inner_html("div.mui-1nl4cpc-gridContainer-root")
    soup = BeautifulSoup(html,"html.parser")
    hrefs = [a['href'] for a in soup.find_all('a', href=True)]
    print(len(hrefs))

    while(arama_sayisi>0):
        if(i == len(hrefs)-1):
            i = 0
            sayfa_sayaci += 1
            hrefs.clear()
            page.goto(url + str(sayfa_sayaci))
            page.mouse.wheel(0, 10000)
            html = page.inner_html("div.mui-1nl4cpc-gridContainer-root")
            soup = BeautifulSoup(html,"html.parser")
            hrefs = [a['href'] for a in soup.find_all('a', href=True)]
            print(len(hrefs))

        page.goto(web_site+hrefs[i])
        page.mouse.wheel(0, 1000)
        if page.is_visible("strong.mui-1isu8w6-empasis"):
            durum = page.inner_html("strong.mui-1isu8w6-empasis")
            if durum == "En iyi seçim!":
                arama_sayisi -= 1
                page.get_by_role("button", name="Anahtar sözcükleri panoya kopyalayın").click()
                title = page.inner_html(".mui-u28gw5-titleRow > h1")
                datas = page.evaluate("navigator.clipboard.readText()").split(',')
                for data in datas:
                    cursor.execute(add_command,(data.strip(),))
                print(title)
        i+=1
    browser.close()
    conn.commit()
    conn.close()