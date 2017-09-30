import scrapy

class CourseSpider(scrapy.Spider):
    """
    Spider that crawls courses.students.ubc.ca
    For all detailed course data.
    """

    name = "courses"
    urls = [
        "https://courses.students.ubc.ca/cs/main?pname=subjarea&tname=subjareas&req=0"
    ]

    def start_requests(self):
        for url in self.urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        output = []
        rows = response.xpath('//tbody/tr')
        for row in rows:
            data = {}
            data['url'] = row.xpath('./td/a/@href').extract_first()
            data['col1'] = row.xpath('./td/a/text()').extract_first()
            data['col2'] = row.xpath('./td[2]/text()').extract_first()
            # doesn't always have 2nd column in child links
            data['col3'] = row.xpath('./td[3]/text()').extract_first()
            output.append(data)
        
        return output
