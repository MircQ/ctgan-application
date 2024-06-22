import fitz


class PDFManager:

    @staticmethod
    def create_pdf(text: str, image: bytes) -> bytes:
        """
        
        """

        doc = fitz.open()
        page = doc.new_page(width=1200, height=700)
        text_point = fitz.Point(50, 50)
        image_box = fitz.Rect(250, 175, 950, 525)
        page.insert_text(point=text_point, text=text)
        page.insert_image(rect=image_box, stream=image)

        return doc.write()
