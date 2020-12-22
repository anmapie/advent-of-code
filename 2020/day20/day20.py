import sys


def main():
    input_file = sys.argv[1]
    try:
        with open(input_file) as file_reader:
            clean_lines = [line.rstrip() for line in file_reader.readlines()]
            tiles = build_tile_map(clean_lines)
            print(multiply_four_corners(tiles))
            print(build_image(tiles))

    except Exception as error:
        print(error)
        raise


def build_tile_map(raw_input):
    tiles = {}
    curr_tile_id = ""
    curr_tile = []
    for line in raw_input:
        if len(line) == 0:
            continue
        elif line.startswith("Tile"):
            if curr_tile_id:
                tiles[curr_tile_id] = curr_tile
                curr_tile = []
            curr_tile_id = int(line.split()[1].rstrip(":"))
        else:
            curr_tile.append(line)

    # ADD THE LAST TILE HOLY SHIT
    tiles[curr_tile_id] = curr_tile
    return tiles


def build_image(tile_map):
  # find all dem edges
  edge_map = find_all_edge_matches(tile_map)
  
  # pull off the four corners
  corners = []
  for tile_id, edges in edge_map.items():
    if len(edges) == 2:
        corners.append(tile_id)
  
  image = []
  # pick the upper left corner
  # it might not be the REAL upper left, but it will be a stable one to build off
  # we can always rotate the image into oblivion to find nessie
  upper_left_corner_id = pick_stable_upper_left_corner(corners, edge_map, tile_map) 
  return upper_left_corner_id

def pick_stable_upper_left_corner(corner_ids, edge_map, tile_map):
  for corner in corner_ids:
    corner_edges = build_edge_list(tile_map[corner])
    corner_adjacent_tiles = edge_map[corner]

    bottom_match = False
    right_match = False
    for tile_id in corner_adjacent_tiles:
      adjacent_tile_edges = build_edge_list(tile_map[tile_id])
      for adjacent_edge in adjacent_tile_edges:
        reverse_adjacent_edge = adjacent_edge[::-1]
        # our stable upper left will have matches on right and bottom only
        # these are [1] and [2] in our edge list, respectively
        if corner_edges[1] == adjacent_edge or corner_edges[1] == reverse_adjacent_edge:
          right_match = True
        elif corner_edges[2] == adjacent_edge or corner_edges[2] == reverse_adjacent_edge:
          bottom_match = True
    if right_match and bottom_match:
      return corner
        

def multiply_four_corners(tile_map):
    edge_map = find_all_edge_matches(tile_map)


    corner_ids = []
    for tile_id, edges in edge_map.items():
        if len(edges) == 2:
            corner_ids.append(tile_id)

    if len(corner_ids) != 4:
        raise Exception(f"Why don't you have four corners? corner_ids: {corner_ids}")

    corner_product = 1
    for corner in corner_ids:
        corner_product *= corner

    return corner_product


def find_all_edge_matches(tile_map):
    all_edge_matches = {}
    for source_tile_key, source_tile in tile_map.items():
        source_edge_matches = []
        for candidate_tile_key, candidate_tile in tile_map.items():
            if candidate_tile_key == source_tile_key:
                continue
            if tile_edge_matches(source_tile, candidate_tile):
                source_edge_matches.append(candidate_tile_key)
        all_edge_matches[source_tile_key] = source_edge_matches
    return all_edge_matches


def tile_edge_matches(source_tile, candidate_tile):
    source_edges = build_edge_list(source_tile)
    candidate_edges = build_edge_list(candidate_tile)

    for source_edge_index, source_edge in enumerate(source_edges):
        for candidate_edge_index, candidate_edge in enumerate(candidate_edges):
            if source_edge == candidate_edge or source_edge == candidate_edge[::-1]:
                return True

    return False


def build_edge_list(tile):
    end_index = len(tile) - 1

    # build columns
    left_col = ""
    right_col = ""
    for row_index in range(len(tile)):
        left_col += tile[row_index][0]
        right_col += tile[row_index][end_index]

    return [tile[0], right_col, tile[end_index], left_col]


if __name__ == "__main__":
    main()
