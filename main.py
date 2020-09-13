import random
import argparse
import cairo
import numpy as np 
from tqdm import tqdm
from scipy import ndimage
from PIL import Image, ImageFilter
from style import *
from utils import *

STYLES = {
    'impressionist' : Impressionist(),
    'expressionist' : Expressionist(),
    'coloristwash' : ColoristWash(),
    'pointillist' : Pointillist(),
    'mystyle': MyStyle()
}

class Painter:
    def __init__(self, output_path, style):
        self.output_path = output_path
        self.style = style

    def paint(self, src_img):
        self.canvas = cairo.ImageSurface(cairo.FORMAT_RGB24, \
            src_img.width, src_img.height)
        self.context = cairo.Context(self.canvas)
        self.context.scale(src_img.width, src_img.height)
        self.context.set_line_cap(cairo.LINE_CAP_ROUND) # Ends of a stroke are circles

        for radius in self.style.brush_radii: 
            gaussian_filter = ImageFilter.GaussianBlur(radius * self.style.blur_factor)
            ref_img = src_img.filter(gaussian_filter)        
            self.paint_layer(ref_img, radius)
            self.canvas.write_to_png(self.output_path)

        return self.canvas

    def paint_layer(self, ref_img, radius):
        strokes = []

        canvas_np = surface_to_np(self.canvas)
        ref_img_np = PIL_to_np(ref_img)
        diff = img_diff(canvas_np, ref_img_np)

        self.gradient_x, self.gradient_y = get_gradient(ref_img)

        width, height = self.canvas.get_width(), self.canvas.get_height()
        step_size = int(self.style.grid_size * radius)
        for x in range(0, width, step_size):
            for y in range(0, height, step_size):
                M = diff[x - int(step_size / 2):x + int(step_size / 2),
                        y - int(step_size / 2):y + int(step_size / 2)]
                area_error = np.sum(M) / (step_size ** 2)
                if area_error > self.style.approximation_threshold:
                    x_1, y_1 = np.unravel_index(np.argmax(M), M.shape)
                    x_1, y_1 = x - int(step_size / 2) + x_1, y - int(step_size / 2) + y_1
                    x_1, y_1 = min(width - 1, max(0, x_1)), min(height - 1, max(0, y_1)) 
                    stroke = self.make_spline_stroke(x_1, y_1, radius, ref_img_np, canvas_np)
                    strokes.append(stroke)

        # Paint all strokes on the canvas in random order
        random.shuffle(strokes)
        print("Painting with stroke size {}...".format(radius))

        for stroke in tqdm(strokes):
            self.context.set_line_width(max(self.context.device_to_user_distance(2 * radius, 2 * radius)))
            self.context.set_source_rgba(stroke['stroke_color'][0] / 255,  
                                        stroke['stroke_color'][1] / 255,
                                        stroke['stroke_color'][2] / 255,
                                        self.style.opacity)

            width, height = self.canvas.get_width(), self.canvas.get_height()
            self.context.move_to(stroke['control_points'][0][0] / width, stroke['control_points'][0][1] / height)
            for idx in range(1, len(stroke['control_points'])):
                self.context.line_to(stroke['control_points'][idx][0] / width, stroke['control_points'][idx][1] / height)
                self.context.move_to(stroke['control_points'][idx][0] / width, stroke['control_points'][idx][1] / height)

            self.context.close_path()
            self.context.stroke()
        
        return 

    def make_spline_stroke(self, x_0, y_0, radius, ref_img_np, canvas_np):
        stroke = {}
        stroke['stroke_color'] = ref_img_np[x_0, y_0]
        stroke['control_points'] = []
        stroke['control_points'].append((x_0, y_0))

        x, y = x_0, y_0
        last_dx, last_dy = 0, 0
        for length in range(1, self.style.max_stroke_length):
            if length > self.style.min_stroke_length and \
                np.linalg.norm(ref_img_np[x, y] - canvas_np[x, y]) < \
                np.linalg.norm(ref_img_np[x, y] - ref_img_np[x_0, y_0]):
                return stroke 

            # Detect vanishing gradient
            gx, gy = self.gradient_x[x, y], self.gradient_y[x, y]
            if gx * gx + gy * gy == 0:
                return stroke

            # Get unit vector of gradient
            normal_x, normal_y = -gy, gx

            # Reverse direction if necessary 
            if last_dx * normal_x + last_dy * normal_y < 0:
                normal_x, normal_y = -normal_x, -normal_y

            normal_x = self.style.curvature_filter * normal_x + \
                        (1 - self.style.curvature_filter) * last_dx
            normal_y = self.style.curvature_filter * normal_y + \
                        (1 - self.style.curvature_filter) * last_dy
            normal_x_norm = normal_x / np.sqrt((normal_x ** 2 + normal_y ** 2))
            normal_y_norm = normal_y / np.sqrt((normal_x ** 2 + normal_y ** 2))
            x, y = int(round(x + radius * normal_x_norm)), int(round(y + radius * normal_y_norm))
            
            # Check if (x, y) is a valid point
            if not (0 <= x < self.canvas.get_width() and 0 <= y < self.canvas.get_height()):
                return stroke
            last_dx, last_dy = normal_x, normal_y

            # Add the point (x, y) to strokes
            stroke['control_points'].append((x, y))

        return stroke


if __name__ == '__main__':
    # Argument parsing 
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', '-i', help = 'Path of input image') 
    parser.add_argument('--output', '-o', help = 'Directory of output images')
    parser.add_argument('--style', '-s', default = 'impressionist', help = 'Painter style')
    args = parser.parse_args()

    if args.input is None:
        print('Error: Source image is not given.')
        exit(0)
    
    if args.output is None:
        print('Error: Output path is not given.')
        exit(0)

    if args.style not in STYLES:
        print('Error: Specified style is not found.')
        exit(0)

    # Read source image 
    src_img = Image.open(args.input).convert('RGB')

    # Painting
    style = STYLES[args.style]
    painter = Painter(args.output, style)
    painter.paint(src_img)
