from math import sqrt


class Heuristics:
    """
    A class that houses the following heuristics:
        (1) Closest distance from 'conquered' area to the bottom right corner
        (2) Number of total cells 'conquered'
        (3) Number of border cells 'conquered'
        (4) Size of the perimeter
    There is also a method to return a weighted sum of these heuristics
    """

    def __init__(self, board):
        self.board = board
        self.all_neighbors = self.board.find_extended_neighbors(self.board.starting_point[0],
                                                                self.board.starting_point[1],
                                                                {self.board.starting_point})

    def distance_to_corner(self, dist_func=None):
        """
        Returns the shortest distance to the bottom right corner from the
        'conquered' area. Distance is calculated using the euclidean distance
        by default. If euclidean is set to False, then manhattan distance is used.
        :param board: A Board object to analyze
        :param dist_func: Function to use to calculate the distance.
        :return: A float
        """
        if not dist_func:
            dist_func = lambda x: sqrt(
                (x[0] - self.board.height + 1) ** 2 +
                (x[1] - self.board.width + 1) ** 2
            )
        min_point = min(self.all_neighbors, key=dist_func)
        return dist_func(min_point)

    def number_covered(self):
        """Returns the number of cells 'conquered' already"""
        return len(self.all_neighbors)

    def _vertical_perimeter_sum(self):
        """Returns all of the vertical perimeter edges"""
        total = 0
        for row in range(self.board.height):
            in_conquered = False
            for col in range(self.board.width):
                if (row, col) in self.all_neighbors:  # If our cell is 'inside' the perimeter
                    if not in_conquered:  # If the previous cell was 'outside' the perimeter
                        total += 1  # Add one for a 'left-border'
                        in_conquered = True  # Indicate that we are now within the perimeter
                elif in_conquered:  # Our cell is 'outside' the perimeter and the previous cell was 'inside'
                    total += 1  # Add one for a 'right-border'
                    in_conquered = False  # Indicate that we have left the perimeter
        return total

    def _horizontal_perimeter_sum(self):
        """Finds all of the horizontal perimeter edges"""
        total = 0
        for col in range(self.board.width):
            in_conquered = False
            for row in range(self.board.height):
                if (row, col) in self.all_neighbors:  # If our cell is 'inside' the perimeter
                    if not in_conquered:  # If the previous cell was 'outside' the perimeter
                        total += 1  # Add one for a 'left-border'
                        in_conquered = True  # Indicate that we are now within the perimeter
                elif in_conquered:  # Our cell is 'outside' the perimeter and the previous cell was 'inside'
                    total += 1  # Add one for a 'right-border'
                    in_conquered = False  # Indicate that we have left the perimeter
        return total

    def number_border_covered(self):
        """Returns the number of cells on the border covered"""
        total = 0
        for x, y in self.all_neighbors:  # Check corners individually
            if (x == 0 and y == 0) or \
                    (x == 0 and y == self.board.width - 1) or \
                    (x == self.board.height - 1 and y == 0) or \
                    (x == self.board.height - 1 and y == self.board.width - 1):
                total += 1
            elif x == 0 or y == 0 or x == self.board.height - 1 or y == self.board.width - 1:
                total += 1
        return total

    def number_corners_covered(self):
        """Returns the number of corners covered"""
        total = 0
        if (0, 0) in self.all_neighbors:
            total += 1
        if (0, self.board.width - 1) in self.all_neighbors:
            total += 1
        if (self.board.height - 1, 0) in self.all_neighbors:
            total += 1
        if (self.board.height - 1, self.board.width - 1) in self.all_neighbors:
            total += 1
        return total

    def perimeter(self):
        """Returns the size of the perimeter around the 'conquered' area"""
        horizontal_sum = self._horizontal_perimeter_sum()
        vertical_sum = self._vertical_perimeter_sum()
        num_border_edges = self.number_border_covered()
        num_corners_covered = self.number_corners_covered()
        return horizontal_sum + vertical_sum - num_border_edges - num_corners_covered

    def get_weighted_sum(self, null=False):
        """Returns a weighted sum of all of the heuristics in the class"""
        if null:  # Null heuristic
            return 0
        perimeter = self.perimeter()
        border = self.number_border_covered()
        corner_dist = self.distance_to_corner()
        total_covered = self.number_covered()

        perimeter_weight = 1
        border_weight = 1
        corner_dist_weight = 1
        total_covered_weight = 1

        return perimeter * perimeter_weight + border * border_weight + corner_dist * corner_dist_weight + total_covered * total_covered_weight


if __name__ == "__main__":
    from board import Board

    test = Board()
    print(test)
    heur = Heuristics(test)
    print(heur.number_covered())
