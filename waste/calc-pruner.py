import math
from typing import List, Tuple

def get_priority_viewport_sizes() -> List[Tuple[int, int]]:
  return [
    (1920, 1080), (1366, 768), (768, 1024), (412, 915), (360, 800)
  ]

def get_secondary_viewport_sizes() -> List[Tuple[int, int]]:
  return [
    (1536, 864), (390, 844), (393, 873), (414, 896), (1280, 720), (360, 780), 
    (1440, 900), (375, 812), (385, 854), (428, 926), (360, 640), (393, 852), 
    (430, 932), (360, 760), (375, 667), (393, 851)
  ]

def get_divisors(n: int) -> List[int]:
  divisors = set()
  for i in range(1, int(math.sqrt(n)) + 1):
    if n % i == 0:
      divisors.add(i)
      divisors.add(n // i)
  return sorted(divisors)

def calculate_pixel_waste(viewport_width: int, viewport_height: int, tile_width: int, tile_height: int) -> int:
  num_tiles_x = math.ceil(viewport_width / tile_width)
  num_tiles_y = math.ceil(viewport_height / tile_height)

  covered_width = num_tiles_x * tile_width
  covered_height = num_tiles_y * tile_height

  waste_x = max(0, covered_width - viewport_width)
  waste_y = max(0, covered_height - viewport_height)

  return (waste_x * viewport_height) + (waste_y * viewport_width) - (waste_x * waste_y)

def optimal_tile_size(image_width: int, image_height: int, primary_breakpoints: List[Tuple[int, int]], secondary_breakpoints: List[Tuple[int, int]]) -> Tuple[Tuple[int, int], float]:
  min_tile_size = 120

  all_tile_sizes = set()

  for width, height in primary_breakpoints + secondary_breakpoints:
    divisors_width = get_divisors(width)
    divisors_height = get_divisors(height)

    for dw in divisors_width:
      if dw >= min_tile_size:
        for dh in divisors_height:
          if dh >= min_tile_size:
            all_tile_sizes.add((dw, dh))

  best_tile_size = None
  min_average_pixel_waste = float('inf')

  for tw, th in all_tile_sizes:
    total_pixel_waste = sum(
      calculate_pixel_waste(width, height, tw, th) 
      for width, height in primary_breakpoints + secondary_breakpoints
    )
    average_pixel_waste = total_pixel_waste / (len(primary_breakpoints) + len(secondary_breakpoints))

    if average_pixel_waste < min_average_pixel_waste:
      min_average_pixel_waste = average_pixel_waste
      best_tile_size = (tw, th)

  return best_tile_size, min_average_pixel_waste

def calculate_final_pixel_waste(image_width: int, image_height: int, final_tile_width: int, final_tile_height: int, primary_breakpoints: List[Tuple[int, int]], secondary_breakpoints: List[Tuple[int, int]]) -> float:
  total_pixel_waste = sum(
    calculate_pixel_waste(width, height, final_tile_width, final_tile_height)
    for width, height in primary_breakpoints + secondary_breakpoints
  )
  total_viewport_area = sum(width * height for width, height in primary_breakpoints + secondary_breakpoints)
  
  return (total_pixel_waste / total_viewport_area) * 100

def main() -> None:
  image_width = 1920
  image_height = 1080

  density_input = input("Enter the image density (1x, 1.5x, 2x): ").strip()
  if density_input == '1x':
    density = 1.0
  elif density_input == '1.5x':
    density = 1.5
  elif density_input == '2x':
    density = 2.0
  else:
    print("Invalid density input. Defaulting to 1x.")
    density = 1.0

  primary_breakpoints = get_priority_viewport_sizes()
  secondary_breakpoints = get_secondary_viewport_sizes()

  best_tile_size, average_pixel_waste = optimal_tile_size(
    image_width, 
    image_height, 
    primary_breakpoints, 
    secondary_breakpoints
  )

  if best_tile_size:
    tw, th = best_tile_size

    tw_scaled = tw * density
    th_scaled = th * density

    tw_scaled = max(tw_scaled, 120)
    th_scaled = max(th_scaled, 120)

    columns = math.ceil(image_width / tw)
    rows = math.ceil(image_height / th)
    total_tiles = columns * rows

    image_width_scaled = image_width * density
    image_height_scaled = image_height * density

    tile_width_scaled = image_width_scaled / columns
    tile_height_scaled = image_height_scaled / rows

    density_str = f"{int(density)}x" if density == int(density) else f"{density}x"

    average_pixel_waste_percentage = calculate_final_pixel_waste(
      image_width, 
      image_height, 
      tw, 
      th, 
      primary_breakpoints, 
      secondary_breakpoints
    )

    print("\nTile calculation complete!")
    print(f"Image dimensions ({density_str}) = {image_width_scaled} x {image_height_scaled}px")
    print(f"Columns = {columns}, Rows = {rows}")
    print(f"Total tiles = {total_tiles}")
    print(f"Tile dimensions ({density_str}) = {tile_width_scaled:.2f} x {tile_height_scaled:.2f}px")
    print(f"Average pixel waste (pre-scaling) = {average_pixel_waste_percentage:.2f}%")
  else:
    print("No suitable tile size found.")

if __name__ == "__main__":
  main()