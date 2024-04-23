import matplotlib.pyplot as plt
import matplotlib.image as mpimg


def object_dimensions(image_path, focal_length_px, distance_to_object, actual_dimensions):
    image = mpimg.imread(image_path)
    plt.imshow(image)
    plt.title('Click on the two opposite edges of the object')

    # Use pltinput to select points on the object
    selected_points = plt.ginput(2)
    plt.close()

    pixel_diameter = abs(selected_points[0][0] - selected_points[1][0])
    print(f"Diameter in pixels: {pixel_diameter}")

    # Calculate the real-world diameter of the object
    # Using the formula: real_diameter = (pixel_diameter * real_distance) / focal_length_px
    calculated_diameter = (pixel_diameter * distance_to_object) / focal_length_px

    print(f'Derived dimensions of the object: {calculated_diameter} mm')
    print(f'Actual dimensions of the object: {actual_dimensions} mm')
    return calculated_diameter

square_size_mm = 25
chessboard_size = (8, 6)
focal_length = 442.5930392 

# calculate the diameter of a coin using the coin image and distance from camera to coin in mm
coin_image = './coin_images/1710647661887.png'
distance = 55.4  # Distance of the camera to the coin in mm
actual_dimensions_mm = 24.26  # Actual diameter of the coin in mm
derived_dimensions = object_dimensions(coin_image, focal_length, distance, actual_dimensions_mm)
