import sys

def build_coordinate_transforms():
    coordinates = []
    shit = [0, 1, -1]
    for x in shit:
      for y in shit:
        for z in shit:
          for w in shit:
            coordinates.append((x, y, z, w))


    return coordinates

COORDINATE_TRANSFORMS = build_coordinate_transforms()
ACTIVE = "#"
INACTIVE = "."

class CubeMap:
    def __init__(self):
        self.map = {}
    
    def get_value_at_coordinates(self, coordinates):
      x, y, z, w = coordinates

      if w not in self.map:
        return '.'
      
      hyper_layer = self.map[w]
      
      if z not in hyper_layer:
        return '.'
      
      layer = hyper_layer[z]
      
      if x not in layer:
        return '.'
      
      row = layer[x]

      if y not in row:
        return '.'
      
      return row[y]

    def set_value_at_coordinates(self, coordinates, value):
      x, y, z, w = coordinates
      #print(f"set value at {coordinates}")

      if w not in self.map:
        self.map[w] = {}
      
      if z not in self.map[w]:
        self.map[w][z] = {}
      
      if x not in self.map[w][z]:
        self.map[w][z][x] = {}
      
      if y not in self.map[w][z][x]:
        self.map[w][z][x][y]= {}
      
      self.map[w][z][x][y] = value

    def compute_next_cube_value(self, coordinates):
      current_cube_value = self.get_value_at_coordinates(coordinates)
      neighbor_count = self.relevant_active_neighbor_count(coordinates)
      
      if current_cube_value == ACTIVE:
        if neighbor_count == 2 or neighbor_count == 3:
          return ACTIVE
        return INACTIVE
      if current_cube_value == INACTIVE:
        if neighbor_count == 3:
          return ACTIVE
        return INACTIVE
      
  
    def relevant_active_neighbor_count(self, coordinates):
      active_neighbors = 0
      x,y,z,w = coordinates
      for transform in COORDINATE_TRANSFORMS:
        # none of our rules care about neighbor counts > 3, so we can just stop counting
        # and consider this cube to have no relevant active neighbors
        if active_neighbors > 3:
          return 0
        transform_x, transform_y, transform_z, transform_w = transform
        transformed_coordinates = (x + transform_x, y + transform_y, z + transform_z, w + transform_w)
        # you are not your own neighbor
        if transformed_coordinates == coordinates:
          continue
        neighbor_value = self.get_value_at_coordinates(transformed_coordinates)
        if neighbor_value == ACTIVE:
          active_neighbors += 1
      
      return active_neighbors
    
    def count_all_active_cubes(self):
      active_count = 0
      for hyper_layer in self.map.values():
        for layer in hyper_layer.values():
          for row in layer.values():
            for value in row.values():
              if value == ACTIVE:
                active_count += 1

      return active_count

    
    def ordered_keys(self, unordered_dict):
      keys_list = list(unordered_dict.keys())
      keys_list.sort()
      return keys_list
    
    def print_map(self):
      for w in self.ordered_keys(self.map):
        print(f"w={w}")
        hyper_layer = self.map[w]
        for z in self.ordered_keys(hyper_layer):
          print(f"z={z}")
          layer = hyper_layer[w]
          for x in self.ordered_keys(layer):
            row = layer[x]
            line = ""
            for y in self.ordered_keys(row):
              line += self.get_value_at_coordinates((x, y, z, w))
            print(line)
      print("\n")


def main():
    input_file = sys.argv[1]
    try:
        with open(input_file) as file_reader:
          initial_map = build_initial_map([line.rstrip() for line in file_reader.readlines()])
          initial_map.print_map()
          transformed_map = run_map_transforms(initial_map, 6)
          print(transformed_map.count_all_active_cubes())

    except Exception as error:
        print(error)
        raise

def build_initial_map(raw_map_layer):
  cube_map = CubeMap()
  for x_index, line in enumerate(raw_map_layer):
    for y_index, char in enumerate(line):
      coordinates = (x_index, y_index, 0, 0)
      cube_map.set_value_at_coordinates(coordinates, char)
  
  return cube_map

def run_map_transforms(cube_map, transform_count):
  transformed_map = cube_map
  for i in range(transform_count):
    transformed_map = transform_map(transformed_map)
    #transformed_map.print_map()
    print(f"finished transform {i}")
  
  return transformed_map

def transform_map(cube_map):
  transformed_map = CubeMap()

  wKeys = cube_map.ordered_keys(cube_map.map)
  zKeys = cube_map.ordered_keys(cube_map.map[0])
  xKeys = cube_map.ordered_keys(cube_map.map[0][0])
  yKeys = cube_map.ordered_keys(cube_map.map[0][0][0])

  wRange = range(wKeys[0] - 1, wKeys[-1] + 2)
  zRange = range(zKeys[0] - 1, zKeys[-1] + 2)
  xRange = range(xKeys[0] - 1, xKeys[-1] + 2)
  yRange = range(yKeys[0] - 1, yKeys[-1] + 2)

  for w in wRange:
    for z in zRange:
      for x in xRange:
        for y in yRange:
          coordinates = (x, y, z, w)
          transformed_map.set_value_at_coordinates(coordinates, cube_map.compute_next_cube_value(coordinates))
  
  return transformed_map

  

if __name__ == "__main__":
    main()