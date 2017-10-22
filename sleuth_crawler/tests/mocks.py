from scrapy.http import Request, TextResponse

def mock_response(file_name=None, url=None):
    """
    Create a fake Scrapy HTTP response
    """

    if not url:
        url = 'http://www.ubc.ca'

    if file_name:
        file_path = "sleuth_crawler/tests" + file_name
        request = Request(url=url)
        file_content = open(file_path, 'r').read()
    else:
        file_content = ""

    return TextResponse(
        url=url,
        request=request,
        body=file_content,
        encoding='utf-8'
    )
