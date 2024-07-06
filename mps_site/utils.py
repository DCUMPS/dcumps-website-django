import markdown
from markdown.extensions import Extension
from markdown.treeprocessors import Treeprocessor

class ImageDimensionsTreeprocessor(Treeprocessor):
    def run(self, root):
        for img in root.iter('img'):
            alt_text = img.get('alt', '')
            parts = alt_text.split('|')
            if len(parts) == 2:
                try:
                    width = int(parts[0])
                    height = int(parts[1])
                    img.set('width', str(width))
                    img.set('height', str(height))
                except ValueError:
                    pass  # Handle invalid width/height gracefully
        return root

class ImageDimensionsExtension(Extension):
    def extendMarkdown(self, md):
        md.treeprocessors.register(ImageDimensionsTreeprocessor(md), 'image_dimensions', 15)

def render_markdown(text):
    md = markdown.Markdown(extensions=['fenced_code', ImageDimensionsExtension()])
    return md.convert(text)

