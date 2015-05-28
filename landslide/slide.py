import re


HEADER_RE = r'(<h(\d+?).*?>(.+?)</h\d>)\s?(.+)?'


class Slide(object):
    def __init__(self, html, source):
        self.html = html
        self.source = source

        self.classes = []

        self.process_header()

    def process_header(self):
        m = re.search(HEADER_RE, self.html, re.DOTALL | re.UNICODE)

        if m:
            self.header = m.group(1)
            self.level = int(m.group(2))
            self.title = m.group(3)
            self.content = m.group(4).strip() if m.group(4) else m.group(4)
        else:
            self.content = self.html.strip()
