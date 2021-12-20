import xml.etree.ElementTree as ET


def process_xml():
    tree = ET.parse('utils/openSearchExample.xml')
    root = tree.getroot()

    for node in root.iter('{http://www.w3.org/2005/Atom}feed'):
        for element in node.iter():
           if element.tag=="{http://www.w3.org/2005/Atom}title":
                print('-----------------------------')
                print('title: ', element.text)
           if element.tag == "{http://www.w3.org/2005/Atom}link":
                print('link: ', element.attrib['href'])
           if element.attrib=={'name':'ingestiondate'}:
                print('Ingestion Date: ', element.text)
           if element.attrib=={'name':'size'}:
                print('Size: ',element.text)
           if element.attrib=={'name':'processinglevel'}:
                print('Processing Level: ', element.text)
           if element.attrib=={'name':'uuid'}:
                print('uuid: ', element.text)

if __name__ == '__main__':
    process_xml()