from scrapy.http import Request, TextResponse

def mock_response(file_name, url=None):
    """
    Create a Scrapy fake HTTP response from a given HTML file
    """

    if not url:
        url = 'http://www.ubc.ca'

    file_path = "sleuth_crawler/tests" + file_name

    request = Request(url=url)
    file_content = open(file_path, 'r').read()

    response = TextResponse(
        url=url,
        request=request,
        body=file_content,
        encoding='utf-8'
    )

    return response
