from scrapy.http import Request, TextResponse

def mock_response(file_name=None, url=None):
    """
    Create a fake Scrapy HTTP response
    file_name can be a relative file path or the desired contents of the mock
    """

    if not url:
        url = 'http://www.ubc.ca'
    request = Request(url=url)

    if file_name:
        try:
            file_path = "sleuth_crawler/tests" + file_name
            file_content = open(file_path, 'r').read()
        except OSError:
            # Allow mocker to directly input desired mock content
            file_content = file_name
    else:
        file_content = ""

    return TextResponse(
        url=url,
        request=request,
        body=file_content,
        encoding='utf-8'
    )
