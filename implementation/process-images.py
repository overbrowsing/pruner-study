import os
import shutil
from PIL import Image
import sys
import json
import random

methods = ['benchmark', 'picture-3', 'picture-5', 'srcset-3', 'srcset-5', 'pruner']
image_sizes = {
  'benchmark': [(1920, 1080)],
  'srcset-3': [(360, 800), (768, 1024), (1920, 1080)],
  'srcset-5': [(360, 800), (412, 915), (768, 1024), (1366, 768), (1920, 1080)],
  'picture-3': [(360, 800), (768, 1024), (1920, 1080)],
  'picture-5': [(360, 800), (412, 915), (768, 1024), (1366, 768), (1920, 1080)],
  'pruner': [(1920, 1080)]
}

with open('implementation/assets/keywords.json', 'r') as f:
  data = json.load(f)
  keywords = data['keywords']

def generate_random_filename(keywords, num_words=3):
  random_words = random.sample(keywords, num_words)
  return '-'.join(random_words).lower()

def resize_and_crop_image(image_path, target_width, target_height, output_path):
  target_width = int(target_width * 2)
  target_height = int(target_height * 2)

  with Image.open(image_path) as img:
    img_width, img_height = img.size
    aspect_ratio = img_width / img_height
    target_aspect_ratio = target_width / target_height

    if aspect_ratio > target_aspect_ratio:
      new_height = target_height
      new_width = int(new_height * aspect_ratio)
    else:
      new_width = target_width
      new_height = int(new_width / aspect_ratio)

    img_resized = img.resize((new_width, new_height), Image.LANCZOS)
    left = (img_resized.width - target_width) // 2
    top = (img_resized.height - target_height) // 2
    right = left + target_width
    bottom = top + target_height

    cropped_img = img_resized.crop((left, top, right, bottom))
    cropped_img.save(output_path, format="WebP", quality=80)

def generate_html(folder, method, output_folder, image_filename, columns, rows=None):
  method_folder_path = os.path.join(output_folder, folder, method)
  html_content = ""

  if method == 'benchmark':
    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{folder}</title>
</head>

<body>
  <img src="{image_filename}.webp" alt="{image_filename}">
</body>

<style>
* {{
  margin: 0 !important
}}

img {{
  width: 100%;
  height: 100svh;
  object-fit: cover
}}
</style>

</html>"""
  
  elif method in ['picture-3', 'picture-5']:
    breakpoints = image_sizes[method]
    sources = '\n'.join([
      f'  <source srcset="{image_filename}-{width}w.webp" media="(max-width: {width}px)">'
      for width, height in breakpoints
    ])
    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{folder}</title>
</head>

<body>
  <picture>
{sources}
    <img src="{image_filename}-1920w.webp" alt="{image_filename}">
  </picture>
</body>

<style>
* {{
  margin: 0 !important
}}

img {{
  width: 100%;
  height: 100svh;
  object-fit: cover
}}
</style>

</html>"""
  
  elif method in ['srcset-3', 'srcset-5']:
    sizes = image_sizes[method]
    srcset = ', '.join([f"{image_filename}-{size[0]}w.webp {size[0]}w" for size in sizes])
    sizes_attr = ', '.join([f"(max-width: {size[0]}px) {size[0]}px" for size in sizes]) + ", 1280px"
    
    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{folder}</title>
</head>

<body>
  <img 
    src="{image_filename}-{sizes[1][0]}w.webp" 
    srcset="{srcset}" 
    alt="{image_filename}" 
    loading="lazy">
</body>

<style>
* {{
  margin: 0 !important
}}

img {{
  width: 100%;
  height: 100svh;
  object-fit: cover
}}
</style>

</html>"""
  
  elif method == 'pruner':
    pruner_data = {
      "name": image_filename,
      "tile": f"{columns} {rows}",
      "path": ''
    }
    
    pruner_json = json.dumps(pruner_data)
    
    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{folder}</title>
</head>

<body>
  <img data-pruner='{pruner_json}' alt="{image_filename}" loading="lazy">
</body>

<style>
* {{
  margin: 0 !important
}}

img {{
  width: 100%;
  height: 100svh;
  object-fit: cover
}}
</style>

<script async src="pruner.min.js"></script>

</html>"""

  html_file_path = os.path.join(method_folder_path, 'index.html')
  with open(html_file_path, 'w') as f:
    f.write(html_content)

def process_pruner_image(image_path, pruner_folder_path, columns, rows, image_filename):
  target_width, target_height = 1920, 1080
  target_width = int(target_width * 2)
  target_height = int(target_height * 2)

  with Image.open(image_path) as img:
    img_width, img_height = img.size
    aspect_ratio = img_width / img_height
    target_aspect_ratio = target_width / target_height

    if aspect_ratio > target_aspect_ratio:
      new_height = target_height
      new_width = int(new_height * aspect_ratio)
    else:
      new_width = target_width
      new_height = int(new_width / aspect_ratio)

    img_resized = img.resize((new_width, new_height), Image.LANCZOS)

    left = (img_resized.width - target_width) // 2
    top = (img_resized.height - target_height) // 2
    right = left + target_width
    bottom = top + target_height

    img_resized = img_resized.crop((left, top, right, bottom))

    width, height = img_resized.size
    cell_width = width // columns
    cell_height = height // rows

    os.makedirs(pruner_folder_path, exist_ok=True)

    for count, (row, col) in enumerate(((r, c) for r in range(rows) for c in range(columns)), 1):
      left = col * cell_width
      top = row * cell_height
      right = left + cell_width
      bottom = top + cell_height

      cropped_image = img_resized.crop((left, top, right, bottom))
      cropped_image.save(os.path.join(pruner_folder_path, f"{image_filename}-{count}.webp"), format="WebP", quality=80)

    shutil.copy('implementation/assets/pruner.min.js', pruner_folder_path)

def print_progress_bar(iteration, total, bar_length=40):
  percent = ("{0:.1f}").format(100 * (iteration / float(total)))
  filled_length = int(bar_length * iteration // total)
  bar = '█' * filled_length + '-' * (bar_length - filled_length)
  sys.stdout.write(f'\r|{bar}| {percent}% Complete')
  sys.stdout.flush()

def create_folders_and_html(target_folder, num_images, output_folder):
  valid_extensions = ['.jpg', '.jpeg', '.png', '.webp']
  images = [f for f in os.listdir(target_folder) if any(f.lower().endswith(ext) for ext in valid_extensions)]
  
  print(f"Found {len(images)} images in {target_folder}")
  
  images_to_process = images[:num_images]
  print(f"Processing {len(images_to_process)} images.")

  total_steps = len(images_to_process) * len(methods)
  current_step = 0

  for i, image_filename in enumerate(images_to_process, start=1):
    folder = str(i).zfill(4)
    output_image_folder = os.path.join(output_folder, folder)
    os.makedirs(output_image_folder, exist_ok=True)

    image_name = generate_random_filename(keywords, random.randint(3, 5))
    columns = 14
    rows = 6

    for method in methods:
      method_folder_path = os.path.join(output_image_folder, method)
      os.makedirs(method_folder_path, exist_ok=True)

      image_path = os.path.join(target_folder, image_filename)

      if method == 'benchmark':
        benchmark_image_path = os.path.join(method_folder_path, f"{image_name}.webp")
        resize_and_crop_image(image_path, 1920, 1080, benchmark_image_path)
      elif method != 'pruner':
        for width, height in image_sizes.get(method, []):
          resized_image_path = os.path.join(method_folder_path, f"{image_name}-{width}w.webp")
          resize_and_crop_image(image_path, width, height, resized_image_path)

      if method == 'pruner':
        pruner_folder_path = os.path.join(output_image_folder, 'pruner')
        process_pruner_image(image_path, pruner_folder_path, columns, rows, image_name)

      current_step += 1
      print_progress_bar(current_step, total_steps)

    for method in methods:
      generate_html(folder, method, output_folder, image_name, columns, rows)

  print("\nAll images processed successfully.")

target_folder = 'implementation/target'
output_folder = 'implementation/processed'
num_images = 1000

create_folders_and_html(target_folder, num_images, output_folder)