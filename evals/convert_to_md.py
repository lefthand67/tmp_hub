import os
from bs4 import BeautifulSoup

def convert_html_to_md(html_path, md_path):
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    soup = BeautifulSoup(html_content, 'html.parser')

    # Try to find the main content. 
    # Many modern sites use <main> or a specific article tag.
    # If not found, we'll look for common content wrappers.
    main_content = soup.find('main')
    if not main_content:
        main_content = soup.find('article')
    if not main_content:
        # Fallback: search for the body and remove header/footer
        main_content = soup.find('body')
        if main_content:
            for tag in main_content.find_all(['header', 'footer', 'nav']):
                tag.decompose()

    if not main_content:
        print("Could not find main content area.")
        return

    md_output = []

    # Process elements in order
    for element in main_content.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'ul', 'ol', 'img', 'a']):
        if element.name.startswith('h'):
            level = int(element.name[1])
            text = element.get_text().strip()
            md_output.append(f"{'#' * level} {text}\n")
        
        elif element.name == 'p':
            text = element.get_text().strip()
            if text:
                md_output.append(f"{text}\n")
        
        elif element.name == 'ul':
            for li in element.find_all('li'):
                md_output.append(f"- {li.get_text().strip()}")
            md_output.append("")
        
        elif element.name == 'ol':
            for i, li in enumerate(element.find_all('li'), 1):
                md_output.append(f"{i}. {li.get_text().strip()}")
            md_output.append("")
            
        elif element.name == 'img':
            src = element.get('src', '')
            alt = element.get('alt', 'Image')
            # Ensure relative paths are preserved
            md_output.append(f"![{alt}]({src})\n")
            
        elif element.name == 'a' and element.parent.name != 'p':
            # Only handle standalone links; links inside <p> are handled by get_text()
            # For better MD conversion, we should handle links inside <p> too.
            # But for simplicity in this script, we'll handle them separately if they are blocks.
            text = element.get_text().strip()
            href = element.get('href', '')
            md_output.append(f"[{text}]({href})\n")

    # Special handling for paragraphs to preserve links inside them
    # The above loop is a bit too simple. Let's refine the <p> handling.
    
    # Re-do content processing more carefully
    md_output = []
    for element in main_content.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'ul', 'ol', 'img']):
        if element.name.startswith('h'):
            level = int(element.name[1])
            md_output.append(f"{'#' * level} {element.get_text().strip()}\n")
        elif element.name == 'p':
            # Handle links and bold/italic inside paragraph
            p_text = ""
            for child in element.children:
                if child.name == 'a':
                    p_text += f"[{child.get_text().strip()}]({child.get('href', '')})"
                elif child.name == 'strong' or child.name == 'b':
                    p_text += f"**{child.get_text().strip()}**"
                elif child.name == 'em' or child.name == 'i':
                    p_text += f"*{child.get_text().strip()}*"
                else:
                    p_text += child.get_text()
            md_output.append(f"{p_text.strip()}\n")
        elif element.name == 'ul':
            for li in element.find_all('li'):
                li_text = ""
                for child in li.children:
                    if child.name == 'a':
                        li_text += f"[{child.get_text().strip()}]({child.get('href', '')})"
                    else:
                        li_text += child.get_text()
                md_output.append(f"- {li_text.strip()}")
            md_output.append("")
        elif element.name == 'ol':
            for i, li in enumerate(element.find_all('li'), 1):
                li_text = ""
                for child in li.children:
                    if child.name == 'a':
                        li_text += f"[{child.get_text().strip()}]({child.get('href', '')})"
                    else:
                        li_text += child.get_text()
                md_output.append(f"{i}. {li_text.strip()}")
            md_output.append("")
        elif element.name == 'img':
            src = element.get('src', '')
            alt = element.get('alt', 'Image')
            md_output.append(f"![{alt}]({src})\n")

    with open(md_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(md_output))

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 3:
        print("Usage: python3 convert_to_md.py <input_html> <output_md>")
        sys.exit(1)
    convert_html_to_md(sys.argv[1], sys.argv[2])
