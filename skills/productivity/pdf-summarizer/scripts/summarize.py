import argparse
import sys

try:
    import pypdf
except ImportError:
    print("Error: 'pypdf' package is not installed. Please run: pip install pypdf")
    sys.exit(1)

def summarize_pdf(file_path: str):
    try:
        reader = pypdf.PdfReader(file_path)
        text = ""
        for page in reader.pages[:5]:
            extracted = page.extract_text()
            text += (extracted or "") + "\n"
        print(text[:3000])
    except Exception as e:
        print(f"Error reading PDF: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", required=True, help="Path to PDF file")
    args = parser.parse_args()
    summarize_pdf(args.file)
