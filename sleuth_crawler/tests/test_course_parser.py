from django.test import TestCase
from sleuth_crawler.tests.mocks import mock_response
from sleuth_crawler.scraper.scraper.items import ScrapyCourseItem
from sleuth_crawler.scraper.scraper.spiders.parsers import course_parser as parser
import re

class TestCourseParser(TestCase):
    """
    Test GenericCourseParser
    parsers.course_oarser
    """

    def test_parse_subjects(self):
        """
        Test subjects parsing
        """
        response = mock_response('/test_data/subjects.txt', 'https://courses.students.ubc.ca/cs/main?pname=subjarea&tname=subjareas&req=0')
        output = list(parser.parse_subjects(response))
        expected_subjects = [
            {
                "url": "https://courses.students.ubc.ca/cs/main?pname=subjarea&tname=subjareas&req=1&dept=AANB",
                "name": "AANB Applied Animal Biology",
                "faculty": "Faculty of Land and Food Systems"
            },
            {
                "url": "https://courses.students.ubc.ca/cs/main?pname=subjarea&tname=subjareas&req=1&dept=ACAM",
                "name": "ACAM Asian Canadian and Asian Migration Studies",
                "faculty": "Faculty of Arts"
            }
        ]
        self.assertEquals(output[0].callback.__name__, parser.parse_course.__name__)
        self.assertEquals(output[0].meta['data'],expected_subjects[0])
        self.assertEquals(output[1].meta['data'],expected_subjects[1])

    def test_parse_course(self):
        """
        Test courses parsing
        """
        response = mock_response(
            '/test_data/courses.txt', 
            'https://courses.students.ubc.ca/cs/main?pname=subjarea&tname=subjareas&req=1&dept=ASTR'
        )
        response.meta['data'] = {"url":"some_url"}
        output = list(parser.parse_course(response))
        expected_courses = [
            ScrapyCourseItem(
                subject={"url":"some_url"},
                url="https://courses.students.ubc.ca/cs/main?pname=subjarea&tname=subjareas&req=3&dept=GRSJ&course=101",
                name="GRSJ 101 Introduction to Social Justice"
            ),
            ScrapyCourseItem(
                subject={"url":"some_url"},
                url="https://courses.students.ubc.ca/cs/main?pname=subjarea&tname=subjareas&req=3&dept=GRSJ&course=102",
                name="GRSJ 102 Global Issues in Social Justice"
            )
        ]
        self.assertEquals(output[0].callback.__name__, parser.parse_course_details.__name__)
        self.assertEquals(output[0].meta['data'],expected_courses[0])
        self.assertEquals(output[1].meta['data'],expected_courses[1])

    def test_parse_course_details(self):
        """
        Test course details parsing
        """
        response = mock_response('/test_data/course_details.txt', 'https://courses.students.ubc.ca/cs/main?pname=subjarea&tname=subjareas&req=3&dept=ASTR&course=200')
        response.meta['data'] = ScrapyCourseItem(subject="",url="",name="")
        output = parser.parse_course_details(response)
        expected_course = ScrapyCourseItem(
            subject="", url="", name="",
            description="An overview of intersectional feminist debates and theoretical traditions. Credit will be granted for only one of WMST 100 or GRSJ 101."
        )
        self.assertEquals(output, expected_course)
        