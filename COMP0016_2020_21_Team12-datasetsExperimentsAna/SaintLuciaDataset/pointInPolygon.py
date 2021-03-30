import Geometry

INT_MAX = 360

class Polygon:
    def __init__(self, vertices):
        self.points = vertices

    def contains(self, p):
        n = len(self.points)
        # There must be at least 3 vertices in polygon
        if n < 3:
            return False
        # Create a point for line segment from p to infinite
        extreme = (INT_MAX, p[1])
        count = i = 0
        while True:
            next = (i + 1) % n
            # Check if the line segment from 'p' to 'extreme' intersects with the line
            # segment from 'polygon[i]' to 'polygon[next]'
            if (Geometry.doIntersect(self.points[i], self.points[next], p, extreme)):
                # If the point 'p' is colinear with line segment 'i-next', then check if it lies
                # on segment. If it lies, return true, otherwise false
                if Geometry.orientation(self.points[i], p, self.points[next]) == 0:
                    return Geometry.onSegment(self.points[i], p, self.points[next])
                count += 1
            i = next
            if (i == 0):
                break
        # Return true if count is odd, false otherwise
        return (count % 2 == 1)
