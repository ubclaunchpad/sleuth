import scrapy

class CourseSpider(scrapy.Spider):
    """Spider that crawls courses.students.ubc.ca
    For all detailed course data.
    """

    name = "courses"

    def start_requests(self):
        urls = [
            "https://courses.students.ubc.ca/cs/main?pname=subjarea&tname=subjareas&req=0"
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        child_urls = []
        column0 = []
        column1 = []
        column2 = []

        rows = response.xpath('//tbody/tr')
        for row in rows:
            child_urls.append(row.xpath('./td/a/@href').extract_first())
            column0.append(row.xpath('./td/a/text()').extract_first())
            column1.append(row.xpath('./td[2]/text()').extract_first())
            # doesn't always have 2nd column in child links
            column2.append(row.xpath('./td[3]/text()').extract_first())

        self.__write_to_log("child-links", child_urls)
        self.__write_to_log("column0", column0)
        self.__write_to_log("column1", column1)
        self.__write_to_log("column2", column2)

    def __write_to_log(self, filename, items):
        with open(filename + ".txt", "wb") as page:
            for item in items:
                page.write(str(item) + "\n")
