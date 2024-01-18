import asyncio

from utils.target_logger import get_logger
from parsers.news_sites.thedefiant import ThedefiantParser


logger = get_logger(name='crypto-news-parser', session_id='crypto-news-parser')

thedefiant = ThedefiantParser(logger=logger, news_count=50)


async def main():
    await thedefiant.parse()


if __name__ == '__main__':
    asyncio.run(main())
