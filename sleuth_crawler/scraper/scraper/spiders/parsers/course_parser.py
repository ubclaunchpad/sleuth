import scrapy
from sleuth_crawler.scraper.scraper.spiders.parsers import utils
from sleuth_crawler.scraper.scraper.items import ScrapyCourseItem

BASE_URL = "https://courses.students.ubc.ca"

def parse_subjects(response):
    """
    Scrape for Courses.
    Iterates through Subjects in this page.
    Passes to parse_course, parse_course_details
    """
    rows = response.xpath('//tbody/tr')
    for row in rows:
        next_rel_url = utils.extract_element(row.xpath('./td/a/@href'), 0)
        if len(next_rel_url) > 1:
            next_url = BASE_URL + next_rel_url
            title = utils.extract_element(row.xpath('./td[2]/text()'), 0)
            code = utils.extract_element(row.xpath('./td/a/text()'), 0)
            subject = {
                "url": next_url,
                "name": code+" "+title.strip(),
                "faculty": utils.extract_element(row.xpath('./td[3]/text()'),0)
            }

            yield scrapy.Request(
                next_url,
                callback=parse_course,
                priority=100,
                meta={'data':subject}
            )

def parse_course(response):
    """
    Parse subjct page.
    Iterates through the Courses on this page.
    """
    subject = response.meta['data']
    rows = response.xpath('//tbody/tr')
    for row in rows:
        next_rel_url = utils.extract_element(row.xpath('./td/a/@href'), 0)
        course_code = utils.extract_element(row.xpath('./td/a/text()'), 0)
        course_title = utils.extract_element(row.xpath('./td[2]/text()'), 0)
        course_name = course_code+" "+course_title
        if len(next_rel_url) > 1:
            next_url = BASE_URL + next_rel_url
            course = ScrapyCourseItem(
                subject=subject,
                url=next_url,
                name=course_name,
            )
            yield scrapy.Request(
                next_url,
                callback=parse_course_details,
                priority=100,
                meta={'data':course}
            )

def parse_course_details(response):
    """
    Parse course details page.
    """
    course = response.meta['data']
    course['description'] = utils.extract_element(response.xpath('//p/text()'), 0).strip()
    # TODO: List of sections into course[sections], maybe parse as well
    return course
