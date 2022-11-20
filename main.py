import yamlToXmlLibrary
from yamlFromXmlRegExp import buildxml, writexml
import time


file = open("yaml_from_html.yaml")

start = time.time()
for i in range(100):
    yamlToXmlLibrary.convert()
end = time.time() - start
print("With libraries time", end)
start = time.time()
for i in range(100):
    writexml(buildxml())
end = time.time() - start
print("With regexp time", end)