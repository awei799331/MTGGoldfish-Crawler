import scrapy
import csv
import os

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
        print(response.url)
        with open('temp_file.txt', 'w') as f:
            for item in yeet:
                f.write("%s\n" % item)
            f.close()
            temp_name = str(response.url)
            temp_name = temp_name.replace("https://www.mtggoldfish.com/price/", "").replace("+", "_").replace("/", "-")
            self.parse_helper(temp_name)

    def parse_helper(self, name):
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

        cur_path = os.path.dirname(__file__)
        #print("\n" + os.path.dirname(os.path.dirname(cur_path)) + "\n")
        new_path = os.path.dirname(os.path.dirname(cur_path)) + '\\output\\' + name + '.csv'
        #print("\n" + new_path + "\n")
        with open(new_path, "w") as output:
            for x in lines:
                output.write(x.replace(" ", "") + '\n')