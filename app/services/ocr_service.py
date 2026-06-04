import easyocr
import numpy as np
import cv2

class OCRService:
    def __init__(self):
        # โหลดโมเดลในหน่วยความจำ
        self.reader = easyocr.Reader(['th', 'en'], gpu=False)

    async def extract_text_from_bytes(self, file_bytes: bytes) -> str:
        nparr = np.frombuffer(file_bytes, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        ocr_result = self.reader.readtext(image, detail=0)
        return " ".join(ocr_result)

ocr_service = OCRService()