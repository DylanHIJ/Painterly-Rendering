class Style:
    def __init__(self):
        self.brush_radii = [16, 8, 4, 2]
        self.approximation_threshold = 100
        self.curvature_filter = 1.0
        self.blur_factor = 0.5
        self.min_stroke_length = 16
        self.max_stroke_length = 4
        self.grid_size = 1

class Impressionist(Style):
    def __init__(self):
        self.brush_radii = [8, 4, 2]
        self.approximation_threshold = 100
        self.curvature_filter = 1.0
        self.blur_factor = 0.5
        self.opacity = 1
        self.max_stroke_length = 16
        self.min_stroke_length = 4
        self.grid_size = 1

class Expressionist(Style):
    def __init__(self):
        self.brush_radii = [8, 4, 2]
        self.approximation_threshold = 50
        self.curvature_filter = 0.5
        self.blur_factor = 0.5
        self.opacity = 0.7
        self.max_stroke_length = 16
        self.min_stroke_length = 10
        self.grid_size = 1

class ColoristWash(Style):
    def __init__(self):
        self.brush_radii = [8, 4, 2]
        self.approximation_threshold = 200
        self.curvature_filter = 1
        self.blur_factor = 0.5
        self.opacity = 0.5
        self.max_stroke_length = 16
        self.min_stroke_length = 4
        self.grid_size = 1

class Pointillist(Style):
    def __init__(self):
        self.brush_radii = [4, 2]
        self.approximation_threshold = 100
        self.curvature_filter = 1
        self.blur_factor = 0.5
        self.opacity = 1
        self.max_stroke_length = 0 
        self.min_stroke_length = 0
        self.grid_size = 0.5

class MyStyle(Style):
    def __init__(self):
        self.brush_radii = [8, 4]
        self.approximation_threshold = 100
        self.curvature_filter = 1.0
        self.blur_factor = 0.5
        self.opacity = 1
        self.max_stroke_length = 16
        self.min_stroke_length = 4
        self.grid_size = 1
