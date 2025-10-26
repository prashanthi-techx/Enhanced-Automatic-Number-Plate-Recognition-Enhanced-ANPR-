import pytesseract
import cv2


# If Tesseract is not in PATH on Windows, uncomment and set the path:
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'




def ocr_plate(plate_image, psm=8, whitelist=None):
       """Run Tesseract OCR on the provided plate image and return cleaned text."""
       config = f'--psm {psm} -c tessedit_char_whitelist={whitelist}' if whitelist else f'--psm {psm}'
       text = pytesseract.image_to_string(plate_image, config=config)
       # Basic cleaning
       text = text.strip()
       text = ''.join(ch for ch in text if ch.isalnum())
       return text




if __name__ == '__main__':
# quick test (optional)
img = cv2.imread('data/sample_plate.jpg')
if img is not None:
    print(ocr_plate(img))