import xml.etree.ElementTree as etree
import urllib.request

rss = urllib.request.urlopen("http://servis.idnes.cz/rss.asp?c=zpravodaj")

# print(repr(rss))
tree = etree.parse(rss)
root = tree.getroot()
channel = root.find('channel')
items = channel.findall('item')

for item in items:
    print('*', item.find('title').text)

