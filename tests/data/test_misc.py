from src.data.misc import sort_2d_points


class TestsMisc:

    def test_sort_2d_points(self):

        pts = [
            (0, 0),
            (0, 679),
            (487, 0),
            (487, 679)
        ]
        clockwise_points = [
            (0, 679),
            (487, 679),
            (487, 0),
            (0, 0)
        ]

        assert sort_2d_points(pts) == clockwise_points

        pts = [
            (824.0, 176.0),
            (1064.0, 1288.0000000000005),
            (218.0, 1460.0),
            (50.0, 332.0)
        ]
        clockwise_points = [
            (218.0, 1460.0),
            (1064.0, 1288.0000000000005),
            (824.0, 176.0),
            (50.0, 332.0)
        ]

        assert sort_2d_points(pts) == clockwise_points

        counterclockwise_points = [
            (50.0, 332.0),
            (824.0, 176.0),
            (1064.0, 1288.0000000000005),
            (218.0, 1460.0)
        ]

        assert sort_2d_points(pts, clockwise = False) == counterclockwise_points
