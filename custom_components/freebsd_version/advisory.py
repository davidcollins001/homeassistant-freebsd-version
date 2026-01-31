import aiohttp
from html.parser import HTMLParser

from .const import FREEBSD_URL


class AdvisoryParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.is_table_row = False
        self.is_table_data = False
        self.is_table_body = False
        self.table_data = []
        self.row_data = []
        self.is_list_block = False
        self.is_list_item = False
        self.production_release = False
        self.production_releases = []

    def handle_starttag(self, tag, attrs):
        if tag == 'tbody':
            self.is_table_body = True
        elif tag == 'tr':
            self.is_table_row = True
            self.row_data = []
        elif tag == 'td' or tag == 'th':
            self.is_table_data = True
        elif tag == 'ul':
            self.is_list_block = True
        elif tag == 'li':
            self.is_list_item = True

    def handle_endtag(self, tag):
        if tag == 'tbody' and self.is_table_body:
            self.is_table_body = False
        elif tag == 'tr' and self.is_table_row:
            if self.row_data:
                self.table_data.append(self.row_data)
            self.is_table_row = False
        elif tag == 'td' or tag == 'th':
            self.is_table_data = False
        elif tag == 'ul':
            self.is_list_block = False
        elif tag == 'li':
            self.is_list_item = False

    def handle_data(self, data):
        data = data.strip()
        if data and self.is_table_body and self.is_table_data:
            self.row_data.append(data.strip())

        if self.is_list_block and self.is_list_item:
            if 'Production Release' in data:
                self.production_release = True

        if self.production_release:
            try:
                self.production_releases.append(float(data))
                self.production_release = False
            except ValueError:
                pass


async def get_advisory(version, url=FREEBSD_URL):
    async with aiohttp.ClientSession() as session:
        async with session.get(url.format(version)) as response:
            html = await response.text()

    parser = AdvisoryParser()
    parser.feed(html)

    return {"errata": parser.table_data,
            "releases": parser.production_releases}
