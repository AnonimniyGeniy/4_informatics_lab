import re


class Node:
    def __init__(self, name="node", content=""):
        self.kids = []
        self.name = name
        self.content = content

    def __str__(self):
        content = ""
        if len(self.kids) == 0:
            content = self.content

        for kid in self.kids:
            content += str(kid)

        return "<{0}>\n{1}</{2}>\n".format(self.name, content, self.name)


def match(line):
    pattern = r'- \S+:\s*'
    return re.fullmatch(pattern, line)


def resplit(line):
    pattern = r":"
    return re.split(pattern, line, maxsplit=1)


def getdata(lines, debug = False):
    data = []
    blocks = []
    block = []
    for i in lines:
        if match(i):  # <---------------------- regexp here
            if block:
                blocks.append(block)
            block = [i[2:-1]]
        else:
            block.append(i[2:-1])

    if block:
        blocks.append(block)

    for block in blocks:
        seq = {}
        name = ""
        tmp_data = {}
        for line in block:
            #if line[0] != " ":
            if not re.fullmatch(r'  .+', line): #<--------- regexp here
                if seq != {}:
                    tmp_data[name] = seq
                name = line[:-1]
                seq = {}
            else:
                # spl = line.split(":")
                spl = resplit(line)  # <--------------------- regexp here
                seq[spl[0][2:]] = spl[1]
        if seq != {}:
            tmp_data[name] = seq
        data.append(tmp_data)
        if debug:
            print(tmp_data)

    return data


def build(d, name):
    p = Node(name, "")
    for key in d.keys():
        if type(d[key]) is dict:
            p.kids.append(build(d[key], key))
        else:
            p.kids.append(Node(key, d[key]))
    return p


def buildxml():
    f = open("yaml_from_html.yaml")
    lines = f.readlines()
    data = getdata(lines)
    print(data)
    xml = Node("day", "")
    ln = 1
    for lesson in data:
        # print(lesson)
        xml.kids.append(build(lesson, "lesson{0}".format(ln)))
        ln += 1
    return xml


def writexml(xml):
    xml = buildxml()
    print(xml, file=open("xml_from_yaml_regexp.xml", "w", encoding="utf-8"))

buildxml()