import xml.etree.ElementTree as ET


def process_xml():
    tree = ET.parse('utils/openSearchExample.xml')
    root = tree.getroot()
    for child in root:
        print(f"tag: {child.tag} attrib: {child.text}")
        # child.attrib['href'] funciona para obtener el link solo si el tag tiene el atributo href


if __name__ == '__main__':
    process_xml()