import requests
from bs4 import BeautifulSoup
import json
import yaml


def main(dump_json=False, reload_page=False, dump_yaml=False):
    dump_json = False
    reload_page = False
    dump_yaml = False
    if reload_page:
        url = "https://itmo.ru/ru/schedule/0/P3106/schedule.htm"
        page = requests.get(url)
        file = open("page.html", "w", encoding='utf-8')
        print(page.text, file=file)
    else:
        page = open("page.html", encoding="utf-8").read()

    soup = BeautifulSoup(page, "html.parser")
    html = page

    startIndex = html.index('<table id="1day"')
    endIndex = html.index('</table>', startIndex)
    html = html[startIndex:endIndex + 8]

    tables = soup.find_all("table", attrs={"class": "rasp_tabl", "id": "1day"})
    table_data = [[cell.text for cell in row("td")] for row in BeautifulSoup(html, features="html.parser")("tr")]

    table_data = []

    for row in BeautifulSoup(html, features="html.parser")("tr"):
        tmp_data = {}
        for cell in row("td"):
            if cell["class"][0] == "time":
                tmp_data["time"] = {"time": cell.span.text, "week": cell.div.text}

            elif cell["class"][0] == "lesson":
                tmp_data["lesson"] = {"name": cell.dd.text, "teacher": cell.b.text.strip(), "format": cell.td.text}

            elif cell["class"][0] == "room":
                tmp_data["place"] = {"class": cell.dd.text.strip(), "corpus": cell.dt.text}
        if tmp_data != {}:
            print(tmp_data)
            table_data.append(tmp_data)
    if dump_json:
        file = open("json_from_html1.json", "w", encoding='utf-8')
        file.writelines(str(table_data).replace("'", '"'))
        file.close()

    if dump_yaml:
        yaml_f = open("yaml_from_html.yaml", "w")
        yaml.safe_dump(table_data, yaml_f, sort_keys=False, allow_unicode=True, line_break="\n")


if __name__ == '__main__':
    main()
