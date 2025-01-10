from typing import List, Tuple

def get_three_breakpoint() -> List[Tuple[int, int]]:
  return [(1920, 1080), (768, 1024), (360, 800)]

def get_five_breakpoint() -> List[Tuple[int, int]]:
  return [(1920, 1080), (1366, 768), (768, 1024), (412, 915), (360, 800)]

def get_common_viewport_sizes() -> List[Tuple[int, int]]:
  return [(1920, 1080), (1366, 768), (768, 1024), (412, 915), (360, 800), (1536, 864),
          (390, 844), (393, 873), (414, 896), (1280, 720), (360, 780), (1440, 900),
          (375, 812), (385, 854), (428, 926), (360, 640), (393, 852), (430, 932),
          (360, 760), (375, 667), (393, 851)]

def calculate_pixel_waste(primary_sizes: List[Tuple[int, int]], common_sizes: List[Tuple[int, int]], byte_per_pixel: int = 3) -> float:
  primary_sizes.sort(key=lambda x: (x[0], x[1]))
  total_waste, total_area = 0, 0

  for viewport_width, viewport_height in common_sizes:
    selected_image = next(((w, h) for w, h in primary_sizes if w >= viewport_width and h >= viewport_height), None)
    
    if selected_image:
      image_width, image_height = selected_image
      image_area = image_width * image_height
      viewport_area = viewport_width * viewport_height
      waste = image_area - viewport_area
      total_waste += waste
      total_area += image_area
      image_bytes = image_area * byte_per_pixel
      viewport_bytes = viewport_area * byte_per_pixel
      byte_waste = image_bytes - viewport_bytes
      print(f"Viewport: {viewport_width}x{viewport_height}, Image: {image_width}x{image_height}, Waste: {waste}, Byte Waste: {byte_waste}")

  return total_waste / total_area * 100

def calculate_single_image_waste(image_width: int, image_height: int, common_sizes: List[Tuple[int, int]], byte_per_pixel: int = 3) -> float:
  total_waste, total_area = 0, 0

  for viewport_width, viewport_height in common_sizes:
    image_area = image_width * image_height
    viewport_area = viewport_width * viewport_height
    waste = image_area - viewport_area
    total_waste += waste
    total_area += image_area
    image_bytes = image_area * byte_per_pixel
    viewport_bytes = viewport_area * byte_per_pixel
    byte_waste = image_bytes - viewport_bytes
    print(f"Viewport: {viewport_width}x{viewport_height}, Image: {image_width}x{image_height}, Waste: {waste}, Byte Waste: {byte_waste}")

  return total_waste / total_area * 100

common_sizes = get_common_viewport_sizes()

average_waste_3 = calculate_pixel_waste(get_three_breakpoint(), common_sizes)
print(f"\nAverage pixel waste for 3-breakpoint model: {average_waste_3:.2f}%\n")

average_waste_5 = calculate_pixel_waste(get_five_breakpoint(), common_sizes)
print(f"\nAverage pixel waste for 5-breakpoint model: {average_waste_5:.2f}%\n")

single_image_waste = calculate_single_image_waste(1920, 1080, common_sizes)
print(f"\nAverage pixel waste for benchmark: {single_image_waste:.2f}%\n")