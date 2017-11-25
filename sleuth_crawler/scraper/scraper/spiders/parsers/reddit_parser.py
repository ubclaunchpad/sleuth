import scrapy
from sleuth_crawler.scraper.scraper.spiders.parsers import utils
from sleuth_crawler.scraper.scraper.items import ScrapyRedditPost

POST_KARMA_THRESHOLD = 4
COMMENT_KARMA_THRESHOLD = 2

def parse_post(response, links):
    '''
    Parses a reddit post's comment section
    '''

    post_section = response.xpath('//*[@id="siteTable"]')

    # check karma and discard if below post threshold
    karma = utils.extract_element(
        post_section.xpath('//div/div/div[@class="score unvoted"]/text()'), 0
    )
    if karma == "" or int(karma) < POST_KARMA_THRESHOLD:
        return

    # get post content
    post_content = utils.extract_element(
        post_section.xpath('//div/div[@class="entry unvoted"]/div/form/div/div'), 0
    )
    post_content = utils.strip_content(post_content)

    # get post title
    titles = utils.extract_element(response.xpath('//title/text()'), 0)
    titles = titles.rsplit(':', 1)
    title = titles[0].strip()
    subreddit = titles[1].strip()

    # get comments
    comments = []
    comment_section = response.xpath('/html/body/div[4]/div[2]')
    comment_section = comment_section.xpath('//div/div[@class="entry unvoted"]/form/div/div')
    for comment in comment_section:
        # TODO: get user of each comment as well?
        comment = utils.strip_content(comment.extract())
        if len(comment) > 0:
            comments.append(' '.join(c for c in comment))

    return ScrapyRedditPost(
        url=response.url,
        title=title,
        subreddit=subreddit,
        post_content=post_content,
        comments=comments,
        links=links
    )
