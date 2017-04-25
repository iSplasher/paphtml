import pyhtml
import tempfile
import os

class Shape:
    ""

    def __init__(self):
        self.name = ''
        self.x = 0
        self.y = 0

    def css(self):
        return ""

class Rect(Shape):

    def __init__(self, x, y, w, h):
        super().__init__()
        self.name = 'rect'
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.border = None
        self.color = None

    def css(self, id):
        c = "#{} {{ \n".format(id) \
            + "position: absolute; \n" \
            + "left: {}px; \n".format(self.x) \
            + "top: {}px; \n".format(self.y) \
            + "width: {}px; \n".format(self.w) \
            + "height: {}px; \n".format(self.h) \
            + "border: 2px solid red; \n".format(self.h) \
            + "}\n"
        return c

class Circle(Shape):

    def __init__(self, x, y, r):
        super().__init__()
        self.name = 'circle'
        self.x = x
        self.y = y
        self.r = r

class Element:
    "Et HTML element"

    def __init__(self, id):
        self.id = id
        self.css = None
        self.html = None


def build_html(shapes=None):
    """
    """
    assert isinstance(shapes, (tuple, list))

    if not shapes:
        shapes = []
        shapes.extend((
            Rect(0, 0, 800, 500),
            Rect(0, 510, 800, 300),
            Rect(0, 810, 800, 300),
            ))


    elements = []

    for n, shape in enumerate(shapes):
        assert isinstance(shape, Shape)
        el_id = shape.name+str(n)
        el = Element(el_id)
        el.html = pyhtml.div(id=el_id)("content")
        el.css = shape.css(el_id)

        elements.append(el)

    # byg HTML

    head = pyhtml.head(
            pyhtml.meta(charset="utf-8"),
            pyhtml.title("DrawHTML"),
            pyhtml.link(rel="stylesheet", href="PATH/TO/CSS")
        )
    divs = [x.html for x in elements if x.html],
    body = pyhtml.body(*divs)

    h = pyhtml.html(
        head,
        body
        )

    css = "* {" \
        + "margin: 0;" \
        + "padding: 0;" \
        + "}\n"

    for x in elements:
        css += x.css

    return h, css


def generatefiles(html, css, dir="website/static", include_css=True):
    "Generates a .html and .css file. Returns tuple with paths"

    files = []

    _, css_path = tempfile.mkstemp(".css", dir=dir)
    with open(css_path, "w") as f:
        f.write(css)

    if include_css:
        html = set_css_attr(html, os.path.split(css_path)[1])
    _, html_path = tempfile.mkstemp(".html", dir=dir)
    with open(html_path, "w") as f:
        f.write(html.render())

    return html_path, css_path

def set_css_attr(html, path_to_css):
    
    for e in html.children:
        if e.name == 'head':
            for h in e.children:
                if h.name == 'link':
                    h.attributes['href'] = path_to_css
    return html

