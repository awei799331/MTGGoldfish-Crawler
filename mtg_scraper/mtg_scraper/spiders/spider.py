import scrapy
import csv
from scrapy.exporters import CsvItemExporter

class priceSpider(scrapy.Spider):
    name = "goldfishSpider"
    allowed_domains = ["mtggoldfish.com"]
    start_urls = []

    def __init__(self):
        with open("card_names.csv", "r") as card_names:
            readCSV = csv.reader(card_names, delimiter=",")
            myList = list(readCSV)
            for row in myList:
                self.start_urls.append("https://www.mtggoldfish.com/price/" + 
                row[1].strip().replace(" ", "+").replace("'", "") +  "/" + row[0].strip().replace(" ", "+").replace("'", "") + "#paper")


    def start_requests(self):
        for each in self.start_urls:
            yield scrapy.Request(each, callback = self.parse)

    def parse(self, response):
        yeet = response.xpath("//script[contains(., 'MTGGoldfishDygraph.bindTabs')]/text()").extract()
        with open('temp_file.txt', 'w') as f:
            for item in yeet:
                f.write("%s\n" % item)
            f.close()
            self.parse_helper()
        yield {
            "data":yeet
        }

    def parse_helper(self):
        lines = []
        with open('temp_file.txt', 'r') as textf:
            content = textf.readlines()
            content = [x.strip() for x in content]
            counter = 0
            all_found = False
            while counter < len(content):
                if "d += \"\\n" in content[counter]:
                    lines.append(content[counter].replace("d += \"\\n", "").replace("\";", ""))
                    all_found = True
                elif all_found:
                    break
                counter+=1

            del content

        with open("output.csv", "w") as output:
            for x in lines:
                output.write(x.replace(" ", "") + '\n')