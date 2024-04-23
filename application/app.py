from flask import Flask, request, jsonify, render_template
import numpy as np
import cv2
import glob

app = Flask(__name__)


def calibrate_camera(pattern_size=(8, 6), square_size=25):
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    # Prepare object points
    objp = np.zeros((pattern_size[0] * pattern_size[1], 3), np.float32)
    objp[:, :2] = np.mgrid[0:pattern_size[0], 0:pattern_size[1]].T.reshape(-1, 2)

    objp = objp * square_size

    # Arrays to store object points and image points from all the images.
    obj_points = []  # 3D points in real world space
    img_points = []  # 2D points in image plane.

    # Read images
    images = glob.glob('../calibration_images/*')
    img_size = (640, 480)
    for image in images:
        image = cv2.imread(image)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        img_size = gray.shape[::-1]

        # Find the chessboard corners
        ret, corners = cv2.findChessboardCorners(gray, pattern_size, None)

        # If found, add object points, image points (after refining them)
        if ret:
            obj_points.append(objp)
            corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
            img_points.append(corners2)

    ret, mtx, dist, r_vecs, t_vecs = cv2.calibrateCamera(obj_points, img_points, img_size, None, None)
    return mtx


def process_point(point):
    splits = point.split(',')
    a, b = splits[0], splits[1]
    a, b = float(a), float(b)
    result = (a,b)
    return result


def calculate_object_dimensions(camera_matrix, distance_to_object, point1, point2):
    print('point1 is:', point1)
    print('point2 is:', point2)

    # Assuming point1 and point2 are tuples of (x, y) coordinates
    pixel_diameter = abs(point1[0] - point2[0])
    print(f"Diameter in pixels: {pixel_diameter}")

    # Extract the focal length from the camera matrix
    focal_length_px = camera_matrix[0][0]

    # Calculate the real-world dimension of the object
    calculated_dimension = (pixel_diameter * distance_to_object) / focal_length_px
    print(f'Derived dimension of the object: {calculated_dimension} mm')

    return calculated_dimension


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/calculate-dimensions', methods=['POST'])
def calculate_dimensions():
    if 'image' not in request.files:
        return "No image uploaded", 400

    print('request is:', request.form)
    distance_to_object = request.form.get('distance', type=float)
    point1 = request.form.get('point1')
    point1 = process_point(point1)
    point2 = request.form.get('point2')
    point2 = process_point(point2)

    matrix = calibrate_camera()
    calculated_diameter = calculate_object_dimensions(matrix, distance_to_object, point1, point2)

    return jsonify({"calculated_diameter": calculated_diameter})


if __name__ == '__main__':
    app.run(debug=True, port=5000)
