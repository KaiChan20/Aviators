import glob, os
import PyPDF2
import fitz


path = r"C:\Users\lexua\OneDrive\Desktop\Work\DAEN 690\Aviators\Data\tcds"



def get_text_percentage(file_name: str) -> float:
    """
    Calculate the percentage of document that is covered by (searchable) text.

    If the returned percentage of text is very low, the document is
    most likely a scanned PDF
    """
    total_page_area = 0.0
    total_text_area = 0.0

    doc = fitz.open(file_name)

    for page_num, page in enumerate(doc):
        total_page_area = total_page_area + abs(page.rect)
        text_area = 0.0
        for b in page.get_text_blocks():
            r = fitz.Rect(b[:4])  # rectangle where block text appears
            text_area = text_area + abs(r)
        total_text_area = total_text_area + text_area
    doc.close()
    return total_text_area / total_page_area


if __name__ == "__main__":
    os.chdir(path)
    pdfs = []
    for file in glob.glob("*.pdf"):
        text_perc = get_text_percentage(file)
        print(text_perc)
        if text_perc < 0.5:
            print("fully scanned PDF - no relevant text")
        else:
            print("not fully scanned PDF - text is present")
            pdfs.append(file)
        
    print(pdfs)

