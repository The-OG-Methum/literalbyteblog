import os
import re
import shutil

# Paths
posts_dir = "/home/methum/Documents/literalbyte/content/blog/"
attachments_dir = "/home/methum/Documents/second_brain/attachments/"
static_images_dir = "/home/methum/Documents/literalbyte/static/images/"

os.makedirs(static_images_dir, exist_ok=True)

# Regex: optional leading !, then [[filename.ext]]
image_pattern = r'(!?)\[\[([^]]+\.(?:png|jpg|jpeg|gif|webp))\]\]'

for filename in os.listdir(posts_dir):
    if filename.endswith(".md"):
        filepath = os.path.join(posts_dir, filename)
        with open(filepath, "r") as file:
            content = file.read()

        # Replacement function
        def replace_image(match):
            bang = match.group(1)  # '!' if exists, else ''
            image = match.group(2)
            # Copy the image
            image_source = os.path.join(attachments_dir, image)
            if os.path.exists(image_source):
                print(f"Copying: {image_source} -> {static_images_dir}")
                shutil.copy(image_source, static_images_dir)
            else:
                print(f"File not found: {image_source}")
            # Return proper Markdown image syntax
            return f"![Image Description](/images/{image.replace(' ', '%20')})"

        # Perform replacement
        content = re.sub(image_pattern, replace_image, content)

        # Write back
        with open(filepath, "w") as file:
            file.write(content)

print("Markdown files processed and images copied successfully.")
