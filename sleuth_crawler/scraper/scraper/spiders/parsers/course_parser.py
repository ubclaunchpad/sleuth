import scrapy
from sleuth_crawler.scraper.scraper.items import ScrapyCourseItem

BASE_URL = "https://courses.students.ubc.ca"

def parse_subjects(response):
    """
    Scrape for Courses.
    Passes to parse_course_helper, parse_course_details
    """
    rows = response.xpath('//tbody/tr')
    for row in rows:
        next_url = BASE_URL + row.xpath('./td/a/@href').extract_first()
        title = row.xpath('./td[2]/text()').extract_first()
        subject = {
            "url": next_url,
            "name": row.xpath('./td/a/text()').extract_first()+" "+title.rstrip(),
            "faculty": row.xpath('./td[3]/text()').extract_first()
        }

        yield scrapy.Request(
            next_url,
            callback=parse_course_helper,
            meta={'data':subject}
        )
    return

def parse_course_helper(response):
    subject = response.meta['data']
    rows = response.xpath('//tbody/tr')
    for row in rows:
        next_url = BASE_URL + row.xpath('./td/a/@href').extract_first()
        course_name = row.xpath('./td/a/text()').extract_first()+" "+row.xpath('./td[2]/text()').extract_first()
        course = ScrapyCourseItem(
            subject=subject,
            url=next_url,
            name=course_name,
        )
        yield scrapy.Request(
            next_url,
            callback=parse_course_details,
            meta={'data':course}
        )
    return

def parse_course_details(response):
    course = response.meta['data']
    course['description'] = response.xpath('//p/text()')[0].extract()
    # TODO: List of sections into course[sections], maybe parse as well
    return course
