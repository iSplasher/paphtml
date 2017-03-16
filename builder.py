from html import HTML

class CSSElement:
    "A css element"

    def __init__(self, id, width=0, height=0):
        self.id = id
        self.width = width
        self.width = height

    def text(self):
        css = "#{} { \n" \
            + "position: absolute;" \
            + "width: {}; \n".format(self.width) \
            + "height: {}; \n".format(self.height) \
            + "}\n"
        return css

def build_header():
    ""
