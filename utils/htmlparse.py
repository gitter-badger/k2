import htmllib, formatter

class LinksParser(htmllib.HTMLParser):
    "HTML links parser class."

    def __init__(self, formatter):
        htmllib.HTMLParser.__init__(self, formatter)
        # create an empty list for storing hyperlinks
        self.links = []

    def start_a(self, attrs):
        # override handler of <A ...>...</A> tags
        # process the attributes
        if len(attrs) > 0:
            for attr in attrs:
                if attr[0] == "href":
                    # ignore all non HREF attributes
                    self.links.append(attr[1])

    def get_links(self):
        '''return the list of extracted links'''
        return self.links

class TitleParser(htmllib.HTMLParser):
    "HTML title parser class."

    def __init__(self, formatter=None, verbose=0):
        "Initialise an object, passing 'verbose' to the superclass."
        htmllib.HTMLParser.__init__(self, formatter, verbose)
        self.title = self.data = None

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()

    def handle_data(self, data):
        if self.data is not None:
            self.data.append(data)

    def start_title(self, attrs):
        self.data = []

    def end_title(self):
        self.title = "".join(self.data)

    def get_title(self):
        '''return parsed title'''
        return self.title