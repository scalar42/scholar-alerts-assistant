from html.parser import HTMLParser

class Paper():
    def __init__(self):
        self.title = ""
        self.source_link = ""
        self.authr_and_pub = ""
        # self.publication = ""
        self.abstract = ""
        self.star_link = ""

    def add_title(self, title):
        self.title = title
        return self.check_complete()

    def add_source_link(self, source_link):
        self.source_link = source_link
        return self.check_complete()

    def add_authr_and_pub(self, authr_and_pub):
        self.authr_and_pub = authr_and_pub
        return self.check_complete()

    # def add_publication(self, publication):
    #     self.publication = publication
    #     return self.check_complete()

    def add_abstract(self, abstract):
        self.abstract += abstract
        return self.check_complete()

    def add_star_link(self, star_link):
        self.star_link = star_link
        return self.check_complete()

    def check_complete(self):
        if self.title == "" or self.source_link == "" or self.authr_and_pub == "" or self.abstract == "" or self.star_link == "":
            return False
        return True

    def __str__(self):
        return self.title + "\n" + self.source_link + "\n" + self.authr_and_pub + "\n" + self.abstract + "\n" + self.star_link

    def __eq__(self, other):
        return self.title == other.title

    def __hash__(self):
        return hash(self.title)


class Parser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.is_title = False
        self.is_authr_and_pub = False
        self.is_abstract = False
        self.is_table = False
        self.papers = []
        self.current_paper = Paper()

    def move_to_next_paper(self):
        self.papers.append(self.current_paper)
        self.current_paper = Paper()
        self.is_title = False
        self.is_authr_and_pub = False
        self.is_abstract = False
        self.is_table = False

    def handle_starttag(self, tag, attrs):
        if tag == "h3":
            self.is_title = True
        elif tag == "a" and self.is_title:
            for attr in attrs:
                if attr[0].lower() == 'href':
                    self.current_paper.add_source_link(attr[1])
                    break
        elif tag == "a" and self.is_table:
            for attr in attrs:
                if attr[0].lower() == 'href':
                    self.current_paper.add_star_link(attr[1])
                    self.is_table = False
                    self.move_to_next_paper()
                    break

    def handle_data(self, data):
        if self.is_title:
            self.current_paper.add_title(data)
        elif self.is_authr_and_pub:
            self.current_paper.add_authr_and_pub(data)
        elif self.is_abstract:
            self.current_paper.add_abstract(data)

    def handle_endtag(self, tag):
        if tag == "h3":
            self.is_title = False
            self.is_authr_and_pub = True
        elif tag == "div":
            if self.is_authr_and_pub:
                self.is_authr_and_pub = False
                self.is_abstract = True
            elif self.is_abstract:
                self.is_abstract = False
                self.is_table = True

    def get_papers(self):
        return self.papers
