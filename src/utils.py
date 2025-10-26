import cv2
import time


def resize_keep_aspect(image, width=None, height=None):
      (h, w) = image.shape[:2]
      if width is None and height is None:
        return image
      if width is None:
        r = height / float(h)
        dim = (int(w * r), height)
      else:
         r = width / float(w)
         dim = (width, int(h * r))
      return cv2.resize(image, dim, interpolation=cv2.INTER_AREA)




def draw_text(img, text, org, font_scale=0.6, thickness=2, color=(0,0,255)):
cv2.putText(img, text, org, cv2.FONT_HERSHEY_SIMPLEX, font_scale, color, thickness, cv2.LINE_AA)




def ensure_positive_rect(x, y, w, h, max_w, max_h):
  x = max(0, int(x))
  y = max(0, int(y))
  w = max(0, int(w))
  h = max(0, int(h))
  if x + w > max_w:
     w = max_w - x
  if y + h > max_h:
     h = max_h - y
  return x, y, w, h