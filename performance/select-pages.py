import os
import shutil

def get_folder_size(folder):
  total_size = 0
  for dirpath, dirnames, filenames in os.walk(folder):
    for f in filenames:
      fp = os.path.join(dirpath, f)
      if os.path.isfile(fp):
        total_size += os.path.getsize(fp)
  return total_size

def get_average_size_folder(base_path):
  folder_sizes = {f: get_folder_size(os.path.join(base_path, f)) for f in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, f))}
  if not folder_sizes:
    return None
  avg_size = sum(folder_sizes.values()) / len(folder_sizes)
  closest_folder = min(folder_sizes, key=lambda k: abs(folder_sizes[k] - avg_size))
  return closest_folder, folder_sizes[closest_folder]

def copy_folder_to_performance(src_folder, dest_folder):
  shutil.rmtree(dest_folder, ignore_errors=True)
  shutil.copytree(src_folder, dest_folder)

def main():
  base_path = 'implementation/processed'
  performance_path = 'docs'
  
  result = get_average_size_folder(base_path)
  if result:
    average_folder, size = result
    copy_folder_to_performance(os.path.join(base_path, average_folder), os.path.join(performance_path, average_folder))

if __name__ == "__main__":
  main()