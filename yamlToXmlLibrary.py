from yaml import load, Loader
import xml.etree.ElementTree as ET


def subEl(d, root, name):
    p = ET.SubElement(root, name)
    for key in d.keys():
        if type(d[key]) is dict:
            subEl(d[key], p, key)
        else:
            ET.SubElement(p, key).text = d[key]


def convert(debug=False):
    data = load(open("yaml_from_html.yaml"), Loader=Loader)
    root = ET.Element("day")
    ln = 1
    for lesson in data:
        subEl(lesson, root, "lesson" + str(ln))
        ln += 1

    tree = ET.ElementTree(root)
    tree.write("xml_from_yaml_lib.xml", encoding="utf-8")


convert()
