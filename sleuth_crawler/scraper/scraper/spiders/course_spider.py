import scrapy
import urlparse
from scrapy_djangoitem import DjangoItem
from sleuth_backend.models import Subject, Course # TODO: setup on Django side

class SubjectItem(DjangoItem):
    """
    Subject model, as defined in Django
    """
    django_model = Subject

class CourseItem(DjangoItem):
    """
    Course model, as defined in Django
    """
    django_model = Course

class CourseSpider(scrapy.Spider):
    """
    Spider that crawls courses.students.ubc.ca
    For all detailed course data.
    """
    name = "courses"
    urls = [
        "https://courses.students.ubc.ca/cs/main?pname=subjarea&tname=subjareas&req=0"
    ]
    base_url = "https://courses.students.ubc.ca"
    custom_settings = {
        'ITEM_PIPELINES': {
            #'scraper.pipelines.CourseToDjangoPipeline': 400,
            'scraper.pipelines.JsonLogPipeline': 300,
        }
    }

    def start_requests(self):
        for url in self.urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        """
        Scrape for Subjects
        """
        output = []
        rows = response.xpath('//tbody/tr')
        for row in rows:
            subject = SubjectItem()
            next_url = self.base_url + row.xpath('./td/a/@href').extract_first()

            subject['subject_code'] = row.xpath('./td/a/text()').extract_first()
            title = row.xpath('./td[2]/text()').extract_first()
            subject['subject_title'] = title.rstrip()
            subject['faculty'] = row.xpath('./td[3]/text()').extract_first()
            
            yield scrapy.Request(
                next_url,
                callback = self.parse_courses,
                meta = {'data' : subject}
            )

    def parse_courses(self, response):
        """
        Scrape for Courses, each associated with a Subject
        """
        subject = response.meta['data']
        rows = response.xpath('//tbody/tr')
        courses = []
        for row in rows:
            course = CourseItem()
            next_url = row.xpath('./td/a/@href').extract_first()

            course['subject'] = subject
            course['code'] = row.xpath('./td/a/text()').extract_first()
            course['title'] = row.xpath('./td[2]/text()').extract_first()
            # course['prereqs'] = 
            courses.append(course)
        yield {subject, courses}
        """
        yield scrapy.Request(
            urlparse.urljoin(self.base_url, data['url']), 
            callback=self.parse_sections,
            meta={'data': data}
        )
        """

    """
    def parse_sections(self, response):
        data = response.meta['data']
        rows = response.xpath('//tbody/tr')
        sections = []
        for row in rows:
            rowdata = {}
            url = row.xpath('./td/a/@href').extract_first()
            rowdata['section'] = row.xpath('./td/a/text()').extract_first()
            rowdata['status'] = row.xpath('./td[0]/text()').extract_first()
            rowdata['type'] = row.xpath('./td[2]/text()').extract_first()
            sections.append(rowdata)
        data['sections'] = sections
        yield data
    """

    #def parse_section(self, response):
