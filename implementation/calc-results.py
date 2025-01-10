import os
import csv
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = 'Times New Roman'

def get_folder_size(folder_path):
  total_size = 0
  for dirpath, dirnames, filenames in os.walk(folder_path):
    for filename in filenames:
      file_path = os.path.join(dirpath, filename)
      total_size += os.path.getsize(file_path)
  return total_size

def bytes_to_kb(bytes_size):
  return bytes_size / 1024

def get_html_file_size(folder_path):
  html_file_path = os.path.join(folder_path, 'index.html')
  return os.path.getsize(html_file_path) if os.path.exists(html_file_path) else 0

def get_pruner_js_size(folder_path):
  pruner_js_path = os.path.join(folder_path, 'pruner.min.js')
  return os.path.getsize(pruner_js_path) if os.path.exists(pruner_js_path) else 0

def count_image_assets(folder_path):
  images_folder = os.path.join(folder_path, 'images')
  if os.path.exists(images_folder):
    return len([f for f in os.listdir(images_folder) if f.lower().endswith('.webp')])
  return 0

def main():
  current_directory = os.getcwd()
  output_folder = os.path.join(current_directory, 'implementation', 'processed')
  csv_file = os.path.join(current_directory, 'implementation', 'results.csv')
  
  total_sizes = {
    'benchmark': {'size': 0, 'html_size': 0, 'requests': 0, 'pruner_js_size': 0},
    'picture_element_3': {'size': 0, 'html_size': 0, 'requests': 0, 'pruner_js_size': 0},
    'picture_element_5': {'size': 0, 'html_size': 0, 'requests': 0, 'pruner_js_size': 0},
    'srcset_3': {'size': 0, 'html_size': 0, 'requests': 0, 'pruner_js_size': 0},
    'srcset_5': {'size': 0, 'html_size': 0, 'requests': 0, 'pruner_js_size': 0},
    'pruner': {'size': 0, 'html_size': 0, 'requests': 0, 'pruner_js_size': 0}
  }
  
  folder_count = 0

  with open(csv_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Folder ID', 'Pruner.js Images (KB)', 'Pruner.js HTML (KB)', 'Pruner.js JS (KB)', 
                     'Picture-3 Images (KB)', 'Picture-3 HTML (KB)',
                     'Picture-5 Images (KB)', 'Picture-5 HTML (KB)',
                     'Srcset-3 Images (KB)', 'Srcset-3 HTML (KB)',
                     'Srcset-5 Images (KB)', 'Srcset-5 HTML (KB)',
                     'Benchmark Image (KB)', 'Benchmark HTML (KB)'])

    for folder_name in os.listdir(output_folder):
      folder_path = os.path.join(output_folder, folder_name)

      if os.path.isdir(folder_path):
        folder_count += 1

        folder_sizes = {key: {'size': 0, 'html_size': 0, 'requests': 0, 'pruner_js_size': 0} for key in total_sizes.keys()}

        folder_types = {
          'picture_element_3': os.path.join(folder_path, 'picture-3'),
          'picture_element_5': os.path.join(folder_path, 'picture-5'),
          'srcset_3': os.path.join(folder_path, 'srcset-3'),
          'srcset_5': os.path.join(folder_path, 'srcset-5'),
          'benchmark': os.path.join(folder_path, 'benchmark'),
          'pruner': os.path.join(folder_path, 'pruner')
        }

        for folder_type, path in folder_types.items():
          if os.path.exists(path):
            folder_size = get_folder_size(path)
            html_size = get_html_file_size(path)
            pruner_js_size = get_pruner_js_size(path) if folder_type == 'pruner' else 0
            image_requests = count_image_assets(path)

            folder_sizes[folder_type]['size'] += folder_size
            folder_sizes[folder_type]['html_size'] += html_size
            folder_sizes[folder_type]['pruner_js_size'] += pruner_js_size
            folder_sizes[folder_type]['requests'] += image_requests

            total_sizes[folder_type]['size'] += folder_size
            total_sizes[folder_type]['html_size'] += html_size
            total_sizes[folder_type]['pruner_js_size'] += pruner_js_size
            total_sizes[folder_type]['requests'] += image_requests

        writer.writerow([
          folder_name,
          bytes_to_kb(folder_sizes['pruner']['size']),
          bytes_to_kb(folder_sizes['pruner']['html_size']),
          bytes_to_kb(folder_sizes['pruner']['pruner_js_size']),
          bytes_to_kb(folder_sizes['picture_element_3']['size']),
          bytes_to_kb(folder_sizes['picture_element_3']['html_size']),
          bytes_to_kb(folder_sizes['picture_element_5']['size']),
          bytes_to_kb(folder_sizes['picture_element_5']['html_size']),
          bytes_to_kb(folder_sizes['srcset_3']['size']),
          bytes_to_kb(folder_sizes['srcset_3']['html_size']),
          bytes_to_kb(folder_sizes['srcset_5']['size']),
          bytes_to_kb(folder_sizes['srcset_5']['html_size']),
          bytes_to_kb(folder_sizes['benchmark']['size']),
          bytes_to_kb(folder_sizes['benchmark']['html_size']),
        ])

  if folder_count > 0:
    methods = ['Benchmark', 'Picture-3', 'Picture-5', 'Srcset-3', 'Srcset-5', 'Pruner.js']
    image_sizes = [
      total_sizes['benchmark']['size'] / folder_count,
      total_sizes['picture_element_3']['size'] / folder_count,
      total_sizes['picture_element_5']['size'] / folder_count,
      total_sizes['srcset_3']['size'] / folder_count,
      total_sizes['srcset_5']['size'] / folder_count,
      total_sizes['pruner']['size'] / folder_count
    ]
    html_sizes = [
      total_sizes['benchmark']['html_size'] / folder_count,
      total_sizes['picture_element_3']['html_size'] / folder_count,
      total_sizes['picture_element_5']['html_size'] / folder_count,
      total_sizes['srcset_3']['html_size'] / folder_count,
      total_sizes['srcset_5']['html_size'] / folder_count,
      total_sizes['pruner']['html_size'] / folder_count
    ]
    pruner_js_sizes = [
      total_sizes['benchmark']['pruner_js_size'] / folder_count,
      total_sizes['picture_element_3']['pruner_js_size'] / folder_count,
      total_sizes['picture_element_5']['pruner_js_size'] / folder_count,
      total_sizes['srcset_3']['pruner_js_size'] / folder_count,
      total_sizes['srcset_5']['pruner_js_size'] / folder_count,
      total_sizes['pruner']['pruner_js_size'] / folder_count
    ]

    plt.figure(figsize=(10, 6))
    plt.bar(methods, image_sizes, label='Images', color='#C0C0C0')
    plt.bar(methods, html_sizes, bottom=image_sizes, label='HTML', color='black')
    plt.bar(methods, pruner_js_sizes, bottom=[i + j for i, j in zip(image_sizes, html_sizes)], label='Pruner.js', color='lightgreen')

    plt.xlabel('Methods')
    plt.ylabel('Average Size (KB)')
    plt.title('Installation Size by Method')
    plt.xticks(rotation=45)
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1))

    plt.ylim(0, max([sum(i) for i in zip(image_sizes, html_sizes, pruner_js_sizes)]) * 1.2)

    plt.tight_layout()

    plt.show()

if __name__ == "__main__":
  main()