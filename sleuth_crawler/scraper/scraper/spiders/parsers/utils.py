from bs4 import BeautifulSoup

def strip_content(data):
    """
    Remove garbage from raw web page content, return as list of lines
    """
    try:
        # strip JavaScript, HTML
        soup = BeautifulSoup(data, "html.parser")
        for script in soup(["script", "style"]):
            script.decompose()
        data = soup.get_text()
        # strip extraneous line breaks and sort into list
        lines = []
        for line in data.splitlines():
            line = line.strip()
            if line:
                lines.append(line)
        return lines
    except Exception:
        # if page is not a webpage, catch errors on attempted parse
        return []

def extract_element(item_list, index):
    """
    Safely extract indexed xpath element
    """
    if index < len(item_list):
        return item_list[index].extract()
    else:
        return ""
