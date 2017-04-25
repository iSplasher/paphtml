import cv2
import numpy as np
import builder

class ShapeDetector:
    ""

    def __init__(self):
        ""
        pass

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
        im_mat = self.image_from_mem(image)
        im_gray = cv2.cvtColor(im_mat, cv2.COLOR_BGR2GRAY)
        im_canny = cv2.Canny(im_gray, 50, 190)
        #ret, thresh = cv2.threshold(im_mat, 127,255,0);

        im2, countors, hiearchy = cv2.findContours(im_canny, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)

        for cnt in countors:

            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.04 * peri, True)

            # check if rect
            if not len(approx) == 4:
                return

            # bounding box
            box = cv2.boundingRect(approx);
            shapes.append(builder.Rect(*box))

            cv2.rectangle(im_mat, (box[0], box[1]), (box[0]+box[2], box[1]+box[3]), (130, 130, 130), 5)
        cv2.imshow("img", im_mat)
        return shapes
 
    def detect(self, image):
        "Detects shapes in image. Returns Shape objects"
        shapes = self.process(image)
        if shapes is None:
            return []
        return shapes
        



filename = 'test5.png'

shapedetector = ShapeDetector()
shapes = shapedetector.detect(filename)
html, css = builder.build_html(shapes)
htmlp, cssp = builder.generatefiles(html, css)

if cv2.waitKey(0) & 0xff == 27:
    cv2.destroyAllWindows()