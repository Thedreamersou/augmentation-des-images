import cv2
import numpy as np
import os

# Path to the folder containing the images
input_folder = r"C:\Users\....\images_resized"
output_folder = r"C:\Users\....\images_processed"

# Ensure the output folder exists
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Define a threshold for "black" pixels (you can adjust this value)
threshold = 40  # Adjust as needed, values closer to 0 will include darker pixels

# Loop through the images in the folder
for filename in os.listdir(input_folder):
    if filename.endswith(('.jpg', '.jpeg', '.png')):
        # Load the image
        image_path = os.path.join(input_folder, filename)
        image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)

        # Check if image is not None
        if image is not None:
            # If the image has 3 channels (RGB)
            if len(image.shape) == 3 and image.shape[2] == 3:
                # Convert the image to grayscale
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

                # Create a mask for black/near-black pixels
                mask = gray < threshold

                # Convert to 4 channels (BGRA) if not already
                image = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)

                # Set the black pixels to transparent (alpha channel = 0)
                image[mask] = [0, 0, 0, 0]

            # If the image has 4 channels (RGBA)
            elif len(image.shape) == 3 and image.shape[2] == 4:
                # Get the alpha channel (transparency) and the RGB part
                alpha_channel = image[:, :, 3]
                rgb = image[:, :, :3]

                # Create a mask for black/near-black pixels in RGB
                mask = np.all(rgb < threshold, axis=-1)

                # Set the black pixels to transparent (alpha = 0)
                image[mask] = [0, 0, 0, 0]

            # Save the processed image
            output_path = os.path.join(output_folder, filename)
            cv2.imwrite(output_path, image)

print("Images processed successfully!")
