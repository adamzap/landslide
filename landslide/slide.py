import re


HEADER_RE = re.compile(r'(<h(\d+?).*?>(.+?)</h\d>)\s?(.+)?', re.S | re.U)
NOTES_RE = re.compile(r'<p>\.notes:\s?(.*?)</p>', re.S)


class Slide(object):
    def __init__(self, html, source):
        self.html = html
        self.source = source

        self.classes = []

        self.process_header()
        self.process_notes()

    def process_header(self):
        m = HEADER_RE.search(self.html)

        if m:
            self.header_source = m.group(1)
            self.header_level = int(m.group(2))
            self.title = m.group(3)
            self.html = m.group(4) if m.group(4) else ''
        else:
            self.header_source = None
            self.header_level = None
            self.title = None
            self.html = self.html

        self.html = self.html.strip()

    def process_notes(self):
        self.html = NOTES_RE.sub(r'<p class="notes">\1</p>', self.html)
