import requests
import os
import csv
import random
import json
from io import BytesIO
from PIL import Image

def ensure_directory_exists(directory):
  os.makedirs(directory, exist_ok=True)

def load_api_key(json_file='dataset/api-key.json'):
  try:
    with open(json_file, 'r') as f:
      data = json.load(f)
      print(f"API Key loaded successfully: {data['api_key'][:5]}...")
      return data['api_key']
  except FileNotFoundError:
    print(f"Error: The file {json_file} was not found.")
    raise
  except json.JSONDecodeError:
    print("Error: There was an issue decoding the JSON file.")
    raise

def search_photos(api_key, institution_id, num_photos=1500):
  url = 'https://api.flickr.com/services/rest/?method=flickr.photos.search'
  image_data = []
  page = 1

  while len(image_data) < num_photos:
    params = {
      'api_key': api_key,
      'user_id': institution_id,
      'extras': 'url_o,width_o,height_o',
      'format': 'json',
      'nojsoncallback': 1,
      'per_page': 100,
      'page': page
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
      photos = response.json().get("photos", {}).get("photo", [])
      for photo in photos:
        width = photo.get('width_o', 0)
        if photo.get('url_o') and width >= 1500 and width > photo.get('height_o', 0):
          image_data.append((photo['url_o'], photo['title'], width, photo['height_o']))

      if not photos or len(image_data) >= num_photos:
        break

      page += 1
    else:
      print(f"Failed to search photos: {response.status_code}")
      break

  random.shuffle(image_data)
  return image_data[:num_photos]

def download_and_save_image(image_url, title, save_dir='implementation/target', retries=3):
  ensure_directory_exists(save_dir)
  image_filename = os.path.join(save_dir, f"{title.replace('/', '_')}.jpg")

  if os.path.exists(image_filename):
    print(f"Image '{title}' already exists. Skipping download.")
    return os.path.getsize(image_filename) / 1024

  for attempt in range(retries):
    try:
      image_data = requests.get(image_url)
      image_data.raise_for_status()
      img = Image.open(BytesIO(image_data.content))
      img.save(image_filename)

      file_size_kb = os.path.getsize(image_filename) / 1024
      print(f"Image '{title}' saved as {image_filename} ({file_size_kb:.2f} KB)")
      return file_size_kb
    except Exception as e:
      print(f"Attempt {attempt + 1}: Failed to download or save the image '{title}': {e}")
      if attempt < retries - 1:
        print("Retrying...")
      else:
        return None

def create_csv(image_data, filename='dataset/dataset.csv'):
  ensure_directory_exists(os.path.dirname(filename))
  with open(filename, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Image URL', 'Title', 'Width', 'Height', 'File Size (KB)'])
    
    for url, title, width, height in image_data:
      print(f"Adding image to CSV: {title}")
      writer.writerow([url, title, width, height, ''])

  print(f"CSV file saved as '{filename}'.")

def download_images_from_csv(csv_filename='dataset/dataset.csv', max_downloads=1000):
  failed_downloads = []
  downloaded_images = 0
  try:
    with open(csv_filename, mode='r', encoding='utf-8') as file:
      reader = csv.reader(file)
      header = next(reader)
      data_rows = []

      for row in reader:
        if downloaded_images >= max_downloads:
          break

        image_url = row[0]
        title = row[1]
        file_size_kb = download_and_save_image(image_url, title)
        if file_size_kb is not None:
          data_rows.append([image_url, title, row[2], row[3], f"{file_size_kb:.2f}"])
          downloaded_images += 1
        else:
          failed_downloads.append((image_url, title))

    with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
      writer = csv.writer(file)
      writer.writerow(header)
      writer.writerows(data_rows)

  except FileNotFoundError:
    print("CSV file not found. Please create the CSV first.")

  print(f"Downloaded {downloaded_images} images.")
  return failed_downloads

def retry_failed_downloads(failed_downloads):
  if not failed_downloads:
    print("No failed downloads to retry.")
    return

  print("\nRetrying failed downloads...")
  for image_url, title in failed_downloads:
    print(f"Retrying download for '{title}'...")
    file_size_kb = download_and_save_image(image_url, title)
    if file_size_kb is not None:
      print(f"Successfully retried '{title}'")
    else:
      print(f"Failed to download '{title}' again.")

def main():
  api_key = load_api_key()
  institution_id = '44494372@N05'
  all_image_data = search_photos(api_key, institution_id)

  if all_image_data:
    create_csv(all_image_data)
    user_input = input("CSV file created. Do you want to download the images? (y/n): ").strip().lower()
    if user_input == 'y':
      failed_downloads = download_images_from_csv()
      retry_input = input("Do you want to retry failed downloads? (y/n): ").strip().lower()
      if retry_input == 'y':
        retry_failed_downloads(failed_downloads)
      else:
        print("Retry cancelled.")
    else:
      print("Download cancelled.")
  else:
    print("No landscape images found.")

main()