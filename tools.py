from PIL import Image, ImageDraw, ImageFont
from PIL.ImageFont import FreeTypeFont  # Add this import for correct type annotation
from pathlib import Path
from typing import List, Tuple, Dict
from LLM import StoryProcessor

class MediaProcessor:
    def __init__(self):
        self.base_path = Path(__file__).parent
        self.story_processor = StoryProcessor()
        self.fonts: Dict[str, FreeTypeFont] = {
            'regular': ImageFont.truetype("arial.ttf", 18),
            'bold': ImageFont.truetype("arialbd.ttf", 24)
        }

    def clean_string(self, text: str) -> str:
        return text.strip().strip('"\'').replace("\n", "")

    def wrap_text(self, draw: ImageDraw.ImageDraw, text: str, max_width: int, font: FreeTypeFont) -> List[str]:
        lines = []
        words = text.split()
        current_line = ''
        
        for word in words:
            test_line = current_line + word + ' '
            line_width = draw.textbbox((0, 0), test_line, font=font)[2]
            
            if line_width <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line[:-1])
                current_line = word + ' '
        
        if current_line:
            lines.append(current_line[:-1])
        
        return lines

    def resize_image(self, image: Image.Image, new_width: int) -> Tuple[Image.Image, float]:
        original_width, original_height = image.size
        aspect_ratio = original_height / original_width
        new_height = int(new_width * aspect_ratio)
        return image.resize((new_width, new_height)), new_width / original_width

    def add_text_to_image(self, input_text: str) -> bool:
        try:
            template_path = self.base_path / "template.png"
            output_path = self.base_path / "E-template.png"
            
            if not template_path.exists():
                raise FileNotFoundError(f"Template image not found at {template_path}")

            # Get text content
            title = self.clean_string(self.story_processor.get_story_title(input_text))
            summary = self.clean_string(self.story_processor.get_story_summary(input_text))
            print(template_path)
            print(summary)
            print(title)
            # Process image
            with Image.open(template_path) as original_image:
                resized_image, scale_factor = self.resize_image(original_image, 600)
                draw = ImageDraw.Draw(resized_image)

                # Scale fonts
                for name, font in self.fonts.items():
                    self.fonts[name] = ImageFont.truetype(
                        font.path, 
                        int(font.size * scale_factor)
                    )

                # Add text to image
                draw.text((50, 10), "Scary stories", font=self.fonts['regular'], fill="white")
                draw.text((10, 40), title, font=self.fonts['bold'], fill="white")

                # Add wrapped summary
                max_width = resized_image.width - 20
                wrapped_lines = self.wrap_text(draw, summary, max_width, self.fonts['regular'])
                y_offset = 80
                for line in wrapped_lines:
                    draw.text((10, y_offset), line, font=self.fonts['regular'], fill="white")
                    y_offset += self.fonts['bold'].size + 5

                resized_image.save(output_path)
                return True

        except Exception as e:
            print(f"Error processing image: {str(e)}")
            return False