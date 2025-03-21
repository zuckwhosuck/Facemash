import os

# Set the folder path where images are located
folder_path = "/Users/harshpatel/Downloads/Everything/K7ishn/F2003/facemash/static/images"  # Change this to your folder path

# Set the prefix for renamed images and desired file extension
prefix = "image"
file_extension = ".jpg"  # Change this if needed (e.g., .png, .jpeg)

# Get a list of all files in the folder
files = os.listdir(folder_path)

# Filter to include only image files with the desired extension
image_files = [f for f in files if f.endswith(file_extension)]

# Sort files to maintain order before renaming
image_files.sort()

# Rename each image file
for index, file_name in enumerate(image_files):
    # Create the new file name
    new_name = f"{prefix}_{index + 50}{file_extension}"
    # Get the full path of the original and new file
    old_path = os.path.join(folder_path, file_name)
    new_path = os.path.join(folder_path, new_name)
    
    # Rename the file
    os.rename(old_path, new_path)
    print(f"Renamed: {file_name} -> {new_name}")

print("Image renaming completed!")
