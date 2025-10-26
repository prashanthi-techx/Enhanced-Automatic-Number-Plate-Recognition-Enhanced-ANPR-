import math




def estimate_speed(location1, location2, ppm=8.8, fps=18.0):
"""Estimate speed (km/h) between two rectangle centers.
location = [x, y, w, h] — we use center displacement in pixels.
ppm = pixels per meter (calibration required)
fps = frames per second of the video (or measured)
"""
x1, y1, w1, h1 = location1
x2, y2, w2, h2 = location2
c1x = x1 + w1 / 2.0
c1y = y1 + h1 / 2.0
c2x = x2 + w2 / 2.0
c2y = y2 + h2 / 2.0


d_pixels = math.hypot(c2x - c1x, c2y - c1y)
d_meters = d_pixels / ppm
speed_m_s = d_meters * fps
speed_kmh = speed_m_s * 3.6
return speed_kmh