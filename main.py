#  KindleTools -
#  @author     Walderlan Sena - <senawalderlan@gmail.com>
#  @license    MIT <https://opensource.org/licenses/MIT>
#  @warning    Redistributions of files must retain the above copyright notice.
#  @version    v1.0.0 - <https://github.com/WalderlanSena/kindletools>

from webbot import Browser
import json


def extractUserPass():
    with open('auth') as f:
        auth = f.read().splitlines()
        return auth


def login(web, auth):
    url = 'https://ler.amazon.com.br/kp/notebook'
    web.go_to(url)
    web.type(auth[0], id='ap_mail')
    web.type(auth[1], id='ap_password')
    web.press(web.Key.ENTER)


def extractBooks(web):
    h2s = web.find_elements(tag='h2')
    books = []
    for h in h2s:
        books.append(h.text)
    return books


def extractHighlights(web, book):
    web.click(book)
    elements = web.find_elements(id='highlight')
    highlights = []
    for e in elements:
        highlights.append(e.text)
    return highlights


if __name__ == '__main__':
    web = Browser(showWindow=True)  # easier debugging
    auth = extractUserPass()
    login(web, auth)
    books = extractBooks(web)
    book_highlights = {}
    for book in books:
        print("extracting highlights for " + book)
        try:
            hs = extractHighlights(web, book)
            book_highlights[book] = hs
        except:
            print("could not extract highlights for: " + book)
    print("writing to json file")
    js = json.dumps(book_highlights)
    f = open("highlights.json", 'w')
    f.write(js)
    f.close()
    print("done")
