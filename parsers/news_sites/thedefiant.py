from logging import Logger

import aiohttp


class ThedefiantParser:

    def __init__(self, logger: Logger, news_count: int):
        self._logger = logger
        self._base_url = 'https://thedefiant.io/'
        self._base_api_url = 'https://thedefiant.io/api/infinite-scroll'
        self._cur_start = 0
        self._chunk_size = 25
        self._news_count = news_count

    def _process_data(self, data: dict) -> dict | None:
        return {
            'id': data.get('_id'),
            'category': data.get('categories')[0].get('name'),
            'title': data.get('title'),
            'subtitle': data.get('excerpt'),
            'main_image': data.get('mainImage').get('asset').get('url') if data.get('mainImage') else None,
            'author': data.get('author').get('name'),
            'published_at': data.get('publishedAt')
        }

    async def _parse_chunk(self):
        cur_posts = []
        params = {
            'after': self._cur_start,
            'type': 'page',
            'value': 'DeFi News',
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(self._base_api_url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    if data.get('posts'):
                        for post in data.get('posts'):
                            cur_data = self._process_data(data=post)
                            if cur_data:
                                cur_posts.append(cur_data)
                    else:
                        self._logger.error(f'[ThedefiantParser:_parse_chunk] - No posts found')
                else:
                    self._logger.error(f'[ThedefiantParser:_parse_chunk] - Failed to fetch data from {self._cur_start}'
                                       f' to {self._cur_start + self._chunk_size}. Status code: {response.status}')
        self._cur_start += self._chunk_size

    async def parse(self):
        while self._cur_start <= self._news_count:
            await self._parse_chunk()
        self._logger.info(f'[ThedefiantParser:parse] - Finished parsing {self._news_count} news')
