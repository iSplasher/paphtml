import cv2
import numpy as np
import builder

class Node:

    def __init__(self, key):
        self.cnt = key
        self.children = []

class ShapeDetector:
    ""

    def __init__(self):
        ""
        self.image = None

    def _is_shape(self, cnt, shape_class):
        if shape_class == builder.Rect:
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.04 * peri, True)

            # check if rect
            if len(approx) == 4:
                return True

    def image_size(self):
        if self.image is not None:
            h, w, _ = self.image.shape
            return w, h
        return 0, 0

    def image_from_mem(self, image, cv2_flag=0):
        ""
        if isinstance(image, str):
            return cv2.imread(image)
        image.seek(0)
        image_array = np.asarray(bytearray(image.read()), dtype=np.uint8)
        return cv2.imdecode(image_array, 0)

    def process(self, image):
        ""
        shapes = []
        self.image = im_mat = self.image_from_mem(image)
        im_gray = cv2.cvtColor(im_mat, cv2.COLOR_BGR2GRAY)
        im_canny = cv2.Canny(im_gray, 50, 200)
        #ret, thresh = cv2.threshold(im_mat, 127,255,0);

        im2, countors, hiearachy = cv2.findContours(im_canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        hiearachy = hiearachy[0] # get the actual hierarchy

        objects = []

        for comp in zip(countors, hiearachy):
            curr_cnt = comp[0]
            curr_h = comp[1]

            # only do this for outer layout so check parent
            if curr_h[3] == -1:
                if self._is_shape(curr_cnt, builder.Rect):
                    # add to objects
                    n = Node(curr_cnt)
                    objects.append(n)

                    # go through every child
                    child = curr_h[2]
                    while child < -1:

                        child_cnt = countors[child]
                        child_h = hiearachy[child]



                        # next in line
                        child = child_h[0]


                
        sizes = []
        for cnt in countors:

            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.04 * peri, True)

            # check if rect
            if not len(approx) == 4:
                return

            # bounding box
            box = cv2.boundingRect(approx)

            # We want to remove duplicate countors
            u_box = hash(box)
            if u_box in sizes:
                continue
            sizes.append(u_box)

            rect_el = builder.Rect(*box)

            # Try to get color
            offset = 10
            color = tuple(im_mat[box[0]+offset, box[1]+offset])
            if len(color) == 3:
                rect_el.color = tuple(reversed(color)) # opencv is BGR not RGB

            shapes.append(rect_el)

            cv2.rectangle(im_gray, (box[0], box[1]), (box[0]+box[2], box[1]+box[3]), (130, 130, 255), 3)
        cv2.imshow("img", im_gray)
        return shapes
 
    def detect(self, image):
        "Detects shapes in image. Returns Shape objects"
        shapes = self.process(image)
        if shapes is None:
            return []
        return shapes
        



filename = 'test6.png'

shapedetector = ShapeDetector()
shapes = shapedetector.detect(filename)
img_width = shapedetector.image_size()[0]
html, css = builder.build_html(shapes, img_width if img_width else 1000)
htmlp, cssp = builder.generatefiles(html, css)

if cv2.waitKey(0) & 0xff == 27:
    cv2.destroyAllWindows()