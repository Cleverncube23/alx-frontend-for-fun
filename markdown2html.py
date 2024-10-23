#!/usr/bin/python3
"""
Markdown to HTML converter with heading support
"""

import sys

def parse_heading(line):
    """
    Parses a Markdown heading line and converts it to an HTML heading.
    """
    heading_level = line.count('#')
    if 1 <= heading_level <= 6:
        heading_content = line[heading_level:].strip()
        return f"<h{heading_level}>{heading_content}</h{heading_level}>"
    return None

def convert_markdown_to_html(input_file, output_file):
    """
    Converts a Markdown file to HTML file with heading support.
    """
    try:
        with open(input_file, 'r') as md_file:
            lines = md_file.readlines()
            html_lines = []
            for line in lines:
                if line.startswith('#'):
                    html_line = parse_heading(line)
                    if html_line:
                        html_lines.append(html_line)
                    else:
                        html_lines.append(line.strip())
                else:
                    html_lines.append(line.strip())

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
