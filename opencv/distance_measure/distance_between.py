# import the necessary packages
from scipy.spatial import distance as dist
from imutils import perspective
from imutils import contours
import numpy as np
import argparse
import imutils
import cv2


def midpoint(pointA: tuple, pointB: tuple):
    """Find the midpoints of the bounding boxes. i.e:
        Top left corner     : (x1, y1),
        bottom right corner : (x2, y2)
        
        and the coordinates of the mid point is:
        mid_x = (x1 + x2) / 2
        mid_y = (y1 + y2) / 2"""
    return ((pointA[0] + pointB[0]) * 0.5, (pointA[1] + pointB[1]) * 0.5)

# construct the argument parse and parse the arguments
parser = argparse.ArgumentParser()
parser.add_argument("-i", "--image", type=str, required=True, help="path to the input image")
parser.add_argument("-w", "--width", type=float, required=True, help="width of the left-most object of the image(in inches)")
args = vars(parser.parse_args())  # {'image': 'example.JPG', 'width': 0.955}

# load the image, convert it to grayscale, and blur it slightly
image = cv2.imread(args["image"])
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (7, 7), 0)

# perform edge detection, then perform a dilation + erosion to
# close gaps in between object edges
edged = cv2.Canny(gray, threshold1=50, threshold2=100)
edged = cv2.dilate(edged, None, iterations=1)
edged = cv2.erode(edged, None, iterations=1)

# find contours in the edge map
cntrs = cv2.findContours(
    image=edged.copy(),
    mode=cv2.RETR_EXTERNAL,
    method=cv2.CHAIN_APPROX_SIMPLE
    )
cntrs = imutils.grab_contours(cntrs)

# sort the contours from left-to-right and, then initialize the
# distance colors and reference object
(cntrs, _) = contours.sort_contours(cntrs)
colors = (
    (0, 0, 255),  # Red
    (240, 0, 159),  # Purple
    (0, 165, 255),  # Orange
    (255, 255, 0),  # Cyan
    (255, 0, 255),  # Pink
)
ref_obj = None
# Why left-to-right?
# Since we know that our reference object will always be the left-most object
# in this image, sorting the contours from left-to-right ensures that the
# contour corresponding to the reference object will always
# be the first entry in the cnts list.

# loop over the contours individually
for c in cntrs:
    # if the contour is not sufficiently large, ignore it
    if cv2.contourArea(c) < 200:
        continue
    # compute the rotated bounding box of the contour
    bbox = cv2.minAreaRect(c)
    bbox = cv2.boxPoints(bbox)
    # bbox = cv2.cv.BoxPoints(bbox) if imutils.is_cv2() else cv2.boxPoints(bbox)
    bbox = np.array(bbox, dtype="int")

    # order the points in the contour such that they appear
	# in top-left, top-right, bottom-right, and bottom-left order
	# then draw the outline of the rotated bounding box
    bbox = perspective.order_points(bbox)

    # compute the center of the bbox
    cX = np.average(bbox[:, 0])
    cY = np.average(bbox[:, 1])

	# if this is the first contour we are examining (i.e.,
	# the left-most contour), we presume this is the
	# reference object
    if ref_obj is None:
        # unpack the ordered bounding box, then compute the midpoint between 
		# the top-left and top-right points,
		# followed by the midpoint between the top-right and bottom-right
        (TL, TR, BR, BL) = bbox
        (ML_X, ML_Y) = midpoint(TL, BL)  # Mid point Left
        (MR_X, MR_Y) = midpoint(TR, BR)  # Mid point Right

        # compute the Euclidean distance between the midpoints,
		# then construct the reference object
        D = dist.euclidean((ML_X, ML_Y), (MR_X, MR_Y))
        ref_obj = (bbox, (cX, cY), D / args["width"])
        continue

	# draw the contours on the image
    original_img = image.copy()
    cv2.drawContours(
        image=original_img,
        contours=[bbox.astype("int")],
        contourIdx=-1,
        color=(0, 255, 0),
        thickness=2
        )
    cv2.drawContours(
        image=original_img,
        contours=[ref_obj[0].astype("int")],
        contourIdx=-1,
        color=(0, 255, 0),
        thickness=2
        )
    # stack the reference coordinates and the object coordinates
	# to include the object center
    ref_coords = np.vstack([ref_obj[0], ref_obj[1]])
    obj_coords = np.vstack([bbox, (cX, cY)])

    # loop over the original points
    for ((xA, yA), (xB, yB), color) in zip(ref_coords, obj_coords, colors):
        # draw circles corresponding to the current points and
		# connect them with a line
        cv2.circle(
            img=original_img,
            center=(int(xA), int(yA)),
            radius=5,
            color=color,
            thickness=-1
            )
        cv2.circle(
            img=original_img,
            center=(int(xB), int(yB)),
            radius=5,
            color=color,
            thickness=-1
            )
        cv2.line(
            img=original_img,
            pt1=(int(xA), int(yA)),
            pt2=(int(xB), int(yB)),
            color=color,
            thickness=2
            )
        # compute the Euclidean distance between the coordinates,
		# and then convert the distance in pixels to distance in units
        D = dist.euclidean((xA, yA), (xB, yB)) / ref_obj[2]
        (mX, mY) = midpoint((xA, yA), (xB, yB))
        cv2.putText(
            img=original_img,
            text=f"{D:.1f}in",
            org=(int(mX), int(mY-10)),
            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
            fontScale=0.55,
            color=color,
            thickness=2
            )
        # show the output image
        cv2.imshow("Image", original_img)
        cv2.waitKey(0)
cv2.destroyAllWindows()

# example command:
# $ python3 distance_between.py --width 0.955 --image "my_desk.JPG"