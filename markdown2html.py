#!/usr/bin/python3
"""
Markdown to HTML converter with heading, list, paragraph, bold, and emphasis support
"""

import sys
import hashlib

def parse_heading(line):
    """
    Parses a Markdown heading line and converts it to an HTML heading.
    """
    heading_level = line.count('#')
    if 1 <= heading_level <= 6:
        heading_content = line[heading_level:].strip()
        return f"<h{heading_level}>{heading_content}</h{heading_level}>"
    return None

def parse_list(lines):
    """
    Parses Markdown list lines and converts them to HTML list.
    """
    html_list = ["<ul>"]
    for line in lines:
        list_item = parse_inline_formatting(line[1:].strip())  # Remove the '-' and any leading/trailing whitespace
        html_list.append(f"<li>{list_item}</li>")
    html_list.append("</ul>")
    return "\n".join(html_list)

def parse_paragraph(lines):
    """
    Parses Markdown paragraph lines and converts them to HTML paragraph.
    """
    html_paragraph = ["<p>"]
    for line in lines:
        if line:
            html_paragraph.append(parse_inline_formatting(line))
        else:
            html_paragraph.append("<br/>")
    html_paragraph.append("</p>")
    return "\n".join(html_paragraph)

def parse_inline_formatting(text):
    """
    Parses inline formatting for bold, emphasis, MD5, and character removal.
    """
    # Bold
    text = text.replace("**", "<b>").replace("**", "</b>")
    
    # Emphasis
    text = text.replace("__", "<em>").replace("__", "</em>")
    
    # MD5
    while '[[' in text and ']]' in text:
        start_idx = text.find('[[')
        end_idx = text.find(']]')
        content = text[start_idx + 2:end_idx]
        md5_hash = hashlib.md5(content.encode()).hexdigest()
        text = text[:start_idx] + md5_hash + text[end_idx + 2:]
    
    # Remove 'c'
    while '((' in text and '))' in text:
        start_idx = text.find('[[')
        end_idx = text.find(']]')
        content = text[start_idx + 2:end_idx]
        content = content.replace('c', '').replace('C', '')
        text = text[:start_idx] + content + text[end_idx + 2:]
    
    return text

def convert_markdown_to_html(input_file, output_file):
    """
    Converts a Markdown file to HTML file with heading, list, paragraph, bold, and emphasis support.
    """
    try:
        with open(input_file, 'r') as md_file:
            lines = md_file.readlines()
            html_lines = []
            inside_list = False
            inside_paragraph = False
            list_lines = []
            paragraph_lines = []

            for line in lines:
                stripped_line = line.strip()

                if stripped_line.startswith('#'):
                    if inside_list:
                        html_lines.append(parse_list(list_lines))
                        list_lines = []
                        inside_list = False
                    if inside_paragraph:
                        html_lines.append(parse_paragraph(paragraph_lines))
                        paragraph_lines = []
                        inside_paragraph = False
                    html_line = parse_heading(stripped_line)
                    if html_line:
                        html_lines.append(html_line)
                elif stripped_line.startswith('-'):
                    if not inside_list:
                        if inside_paragraph:
                            html_lines.append(parse_paragraph(paragraph_lines))
                            paragraph_lines = []
                            inside_paragraph = False
                        inside_list = True
                    list_lines.append(stripped_line)
                elif stripped_line == '':
                    if inside_paragraph:
                        html_lines.append(parse_paragraph(paragraph_lines))
                        paragraph_lines = []
                        inside_paragraph = False
                else:
                    if inside_list:
                        html_lines.append(parse_list(list_lines))
                        list_lines = []
                        inside_list = False
                    inside_paragraph = True
                    paragraph_lines.append(stripped_line)
            
            if inside_list:
                html_lines.append(parse_list(list_lines))
            if inside_paragraph:
                html_lines.append(parse_paragraph(paragraph_lines))

            html_content = "\n".join(html_lines)
            with open(output_file, 'w') as html_file:
                html_file.write(html_content)
    except FileNotFoundError:
        print(f"Missing {input_file}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: ./markdown2html.py README.md README.html", file=sys.stderr)
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    convert_markdown_to_html(input_file, output_file)
    sys.exit(0)
