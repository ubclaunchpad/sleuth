from OpenSSL import SSL
from scrapy.core.downloader.contextfactory import ScrapyClientContextFactory

class CustomContextFactory(ScrapyClientContextFactory):
    """
    Custom context factory that allows SSL negotiation.
    """

    def __init__(self, method):
        # Use SSLv23_METHOD so we can use protocol negotiation
        self.method = SSL.SSLv23_METHOD