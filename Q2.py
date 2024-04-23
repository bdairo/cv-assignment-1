import numpy as np
import cv2
import glob

def calibrate_camera(images_path, pattern_size, square_size):
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    # Prepare object points
    objp = np.zeros((pattern_size[0] * pattern_size[1], 3), np.float32)
    objp[:, :2] = np.mgrid[0:pattern_size[0], 0:pattern_size[1]].T.reshape(-1, 2)

    objp = objp * square_size

    # Arrays to store object points and image points from all the images.
    obj_points = []  # 3D points in real world space
    img_points = []  # 2D points in image plane.

    # Read images
    images = glob.glob(images_path)
    img_size = (640, 480)
    for image in images:
        img = cv2.imread(image)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img_size = gray.shape[::-1]

        # Find the chessboard corners
        ret, corners = cv2.findChessboardCorners(gray, pattern_size, None)

        # If found, add object points, image points (after refining them)
        if ret:
            obj_points.append(objp)
            corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
            img_points.append(corners2)

            # Draw and display the corners
            cv2.drawChessboardCorners(img, pattern_size, corners2, ret)
            cv2.imshow('img', img)
            cv2.waitKey(500)

    cv2.destroyAllWindows()

    ret, mtx, dist, r_vecs, t_vecs = cv2.calibrateCamera(obj_points, img_points, img_size, None, None)

    return mtx,dist,r_vecs


path = './calibration_images/*.png'
chessboard_size = (8, 6)
square_size_mm = 25

mtx, dist,rvecs = calibrate_camera(path, chessboard_size, square_size_mm)

# Print the results
print("Intrinsic matrix:\n", mtx)
print("Distortion coefficients:\n", dist)

# Compute rotation angles for the first image's extrinsic parameters
if rvecs:
    R, _ = cv2.Rodrigues(rvecs[0])
    thetaX = np.degrees(np.arctan2(R[2, 1], R[2, 2]))
    thetaY = np.degrees(np.arctan2(-R[2, 0], np.sqrt(R[2, 1]**2 + R[2, 2]**2)))
    thetaZ = np.degrees(np.arctan2(R[1, 0], R[0, 0]))

    print("Rotation Angles (degrees):\n X: {:.2f}, Y: {:.2f}, Z: {:.2f}".format(thetaX, thetaY, thetaZ))
