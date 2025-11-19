import os
import re
import shutil
import urllib.parse

# Your actual paths
posts_dir = "/home/methum/literalbyte/content/blog/"
attachments_dir = "/home/methum/literalbyte/content/attachments/"  # <-- FIXED
static_images_dir = "/home/methum/literalbyte/static/images/"

# Regex for Obsidian-style embeds: ![[file.ext]]
pattern = r'!\[\[([^\]]+\.(?:png|jpg|jpeg|webp))\]\]'

for filename in os.listdir(posts_dir):
    if filename.endswith(".md"):
        filepath = os.path.join(posts_dir, filename)

        with open(filepath, "r") as file:
            content = file.read()

        matches = re.findall(pattern, content)

        for image in matches:
            # Encode spaces + symbols
            safe_url = urllib.parse.quote(image)

            # Convert Obsidian embed → Markdown
            markdown_image = f"![{image}](/images/{safe_url})"
            content = content.replace(f"![[{image}]]", markdown_image)

            # Copy the image to static/images
            src = os.path.join(attachments_dir, image)
            dest = os.path.join(static_images_dir, image)

            if os.path.exists(src):
                if not os.path.exists(dest):
                    shutil.copy(src, dest)
                else:
                    print(f"Skipped (already exists): {image}")
            else:
                print(f"WARNING: Attachment missing: {image}")

        # Save updated markdown
        with open(filepath, "w") as file:
            file.write(content)

print("Done — converted + copied.")
