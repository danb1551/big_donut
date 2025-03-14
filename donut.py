import os
import time
import math

# Dimensions for the screen buffer
screen_width = 140
screen_height = 45
A, B = 0, 0  # Rotation angles

while True:
    output = [' '] * screen_width * screen_height  # Initialize screen with spaces
    zbuffer = [0] * screen_width * screen_height  # Depth buffer to handle overlap

    # Loop through angles to create the 3D shape of a torus
    for theta in range(0, 628, 10):  # 0 to 2π, step by 10 for the torus circle
        for phi in range(0, 628, 2):  # 0 to 2π, finer steps for a rounder shape
            # Precompute sines and cosines of angles
            sinA = math.sin(A)
            cosA = math.cos(A)
            sinB = math.sin(B)
            cosB = math.cos(B)
            sin_theta = math.sin(theta)
            cos_theta = math.cos(theta)
            sin_phi = math.sin(phi)
            cos_phi = math.cos(phi)

            # 3D coordinates for the donut shape
            circle_x = cos_theta + 2  # Offset from origin
            circle_y = sin_theta

            # Calculate the 3D position after rotating
            x = circle_x * (cosB * cos_phi + sinA * sinB * sin_phi) - circle_y * cosA * sinB
            y = circle_x * (sinB * cos_phi - sinA * cosB * sin_phi) + circle_y * cosA * cosB
            z = 5 + cosA * circle_x * sin_phi + circle_y * sinA  # Distance from viewer
            ooz = 1 / z  # One over z (depth)

            # 2D screen projection coordinates (increased scale factor)
            xp = int(screen_width / 2 + screen_width / 2 * ooz * x)
            yp = int(screen_height / 2 - screen_height / 2 * ooz * y)

            # Calculate luminance index based on the angle
            luminance_index = int(8 * ((cos_phi * cos_theta * sinB - cosA * cos_theta * sin_phi - sinA * sin_theta + cosB * (cosA * sin_theta - cos_theta * sinA * sin_phi))))
            luminance_index = max(0, min(11, luminance_index))  # Ensure it's within range
            luminance_char = '.,-~:;=!*#$@'[luminance_index]

            # Update the output buffer if this point is closer to the screen
            idx = xp + yp * screen_width
            if 0 <= xp < screen_width and 0 <= yp < screen_height:
                if ooz > zbuffer[idx]:
                    zbuffer[idx] = ooz
                    output[idx] = luminance_char

    # Print the frame
    os.system("cls" if os.name == "nt" else "clear")  # Clear screen
    print('\n'.join([''.join(output[i:i + screen_width]) for i in range(0, len(output), screen_width)]))
    A += 0.04  # Rotate around the x-axis
    B += 0.02  # Rotate around the y-axis
    time.sleep(0.03)
