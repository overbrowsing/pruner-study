import os
import csv
import matplotlib.pyplot as plt

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
    'benchmark': {'size': 0, 'html_size': 0, 'requests': 0},
    'picture_element_3': {'size': 0, 'html_size': 0, 'requests': 0},
    'picture_element_5': {'size': 0, 'html_size': 0, 'requests': 0},
    'srcset_3': {'size': 0, 'html_size': 0, 'requests': 0},
    'srcset_5': {'size': 0, 'html_size': 0, 'requests': 0},
    'pruner': {'size': 0, 'html_size': 0, 'requests': 0}
  }
  
  folder_count = 0

  with open(csv_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Folder ID', 'Pruner Images (KB)', 'Pruner HTML (KB)', 
                     'picture 3 Images (KB)', 'picture 3 HTML (KB)', 
                     'picture 5 Images (KB)', 'picture 5 HTML (KB)', 
                     'srcset 3 Images (KB)', 'srcset 3 HTML (KB)', 
                     'srcset 5 Images (KB)', 'srcset 5 HTML (KB)', 
                     'Benchmark Image (KB)', 'Benchmark HTML (KB)'])

    for folder_name in os.listdir(output_folder):
      folder_path = os.path.join(output_folder, folder_name)

      if os.path.isdir(folder_path):
        folder_count += 1

        folder_sizes = {key: {'size': 0, 'html_size': 0, 'requests': 0} for key in total_sizes.keys()}

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
            image_requests = count_image_assets(path)

            folder_sizes[folder_type]['size'] += folder_size
            folder_sizes[folder_type]['html_size'] += html_size
            folder_sizes[folder_type]['requests'] += image_requests

            total_sizes[folder_type]['size'] += folder_size
            total_sizes[folder_type]['html_size'] += html_size
            total_sizes[folder_type]['requests'] += image_requests

        writer.writerow([
          folder_name,
          bytes_to_kb(folder_sizes['pruner']['size']),
          bytes_to_kb(folder_sizes['pruner']['html_size']),
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
    for key in ['benchmark', 'picture_element_3', 'picture_element_5', 'srcset_3', 'srcset_5']:
      avg_size = total_sizes[key]['size'] / folder_count
      avg_html_size = total_sizes[key]['html_size'] / folder_count
      total_requests = total_sizes[key]['requests']
      print(f"\n{key.replace('_', ' ').title()}")
      print(f"+ Average total image assets size: {avg_size / 1024:.2f} KB")
      print(f"+ Average HTML size: {avg_html_size / 1024:.2f} KB")
      print(f"= Average total size (image + HTML): {((avg_size + avg_html_size) / 1024):.2f} KB")
      print(f"--- HTTP requests made: {total_requests // folder_count}")

    pruner_avg_size = total_sizes['pruner']['size'] / folder_count
    pruner_avg_html_size = total_sizes['pruner']['html_size'] / folder_count

    print("\nPruner")
    print(f"+ Average total image assets size: {pruner_avg_size / 1024:.2f} KB")
    print(f"+ Average HTML size: {pruner_avg_html_size / 1024:.2f} KB")
    print(f"= Average total size (image + HTML): {((pruner_avg_size + pruner_avg_html_size) / 1024):.2f} KB")
    print(f"--- HTTP requests made: {total_sizes['pruner']['requests'] // folder_count}")

    print("\nSavings")
    for key in ['picture_element_3', 'picture_element_5', 'srcset_3', 'srcset_5', 'benchmark']:
      if total_sizes[key]['size'] > 0:
        avg_method_size = total_sizes[key]['size'] / folder_count
        avg_method_html_size = total_sizes[key]['html_size'] / folder_count
        size_difference = pruner_avg_size - avg_method_size
        html_size_difference = pruner_avg_html_size - avg_method_html_size

        if avg_method_size > 0:
          savings_percentage = (size_difference / avg_method_size) * 100
        else:
          savings_percentage = 0

        if size_difference > 0:
          print(f"Pruner is larger than {key.replace('_', ' ').title()} by {savings_percentage:.2f}% ({size_difference / 1024:.2f} KB)")
        else:
          print(f"Pruner saves {-size_difference / 1024:.2f} KB ({-savings_percentage:.2f}%) vs {key.replace('_', ' ').title()}")

        if html_size_difference > 0:
          print(f"Pruner's HTML is larger than {key.replace('_', ' ').title()} by {html_size_difference / 1024:.2f} KB")
        else:
          print(f"Pruner's HTML saves {-html_size_difference / 1024:.2f} KB vs {key.replace('_', ' ').title()}")

    methods = ['Benchmark', 'Picture 3', 'Picture 5', 'Srcset 3', 'Srcset 5', 'Pruner']
    sizes = [
      total_sizes['benchmark']['size'] / folder_count,
      total_sizes['picture_element_3']['size'] / folder_count,
      total_sizes['picture_element_5']['size'] / folder_count,
      total_sizes['srcset_3']['size'] / folder_count,
      total_sizes['srcset_5']['size'] / folder_count,
      pruner_avg_size
    ]

    plt.bar(methods, [size / 1024 for size in sizes], color=['grey', 'green', 'green', 'purple', 'purple', 'cyan'])
    plt.xlabel('Methods')
    plt.ylabel('Average Size (KB)')
    plt.title('Installation Size by Method')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
  main()