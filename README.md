# TikTok Story Generator

## Overview
TikTok Story Generator is a Python application that automatically generates engaging TikTok-ready videos from text stories. It uses AI to transform written stories into complete video packages, including audio narration, visual elements, and properly formatted content optimized for TikTok's platform.

## Features
- Converts text stories into TikTok-friendly videos
- Generates AI-powered story summaries and titles
- Creates text-to-speech narration
- Automatically adds visual elements to the video
- Provides downloadable outputs (video, audio, and image)

## How It Works
1. **Text Processing**: The app takes a user's story and uses AI to:
   - Generate a catchy, 4-word maximum title
   - Create an engaging 3-phrase summary

2. **Audio Generation**: Converts the story into speech using TikTok-style voices

3. **Visual Generation**: 
   - Uses a template image
   - Overlays the title and summary
   - Adjusts text size and positioning for optimal viewing

4. **Video Creation**:
   - Combines the template video with the generated audio
   - Overlays the processed image
   - Ensures proper timing and synchronization

## Requirements
- Python 3.8 or higher
- Groq API key
- Required Python packages:
  ```
  streamlit
  moviepy
  Pillow
  langchain-groq
  requests
  ```

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/tiktok-story-generator.git
   cd tiktok-story-generator
   ```

2. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your Groq API key:
   - Create a file named `.env` in the project root
   - Add your API key: `GROQ_API_KEY=your_api_key_here`

## Usage
1. Run the Streamlit app:
   ```bash
   streamlit run main.py
   ```

2. Open your web browser to the provided URL (typically `http://localhost:8501`)

3. Enter your story in the text area

4. Click "Generate Content" and wait for processing

5. Download your generated content:
   - Video file (ready for TikTok)
   - Audio file (narration)
   - Image file (visual element)

## Project Structure
```
tiktok-story-generator/
├── main.py              # Main Streamlit application
├── config.py            # Configuration settings
├── LLM.py              # AI processing logic
├── text_to_speech.py    # Audio generation
├── tools.py             # Image processing utilities
├── template.png         # Base image template
├── test2.mp4            # Video template
└── requirements.txt     # Project dependencies
```

## Technical Details

### AI Processing (LLM.py)
Uses the Groq API through LangChain to generate:
- Engaging titles (4 words max)
- Compelling summaries (3 phrases)
- Content appropriate for TikTok's platform

### Audio Processing (text_to_speech.py)
- Converts text to speech using TikTok-style voices
- Handles long text by splitting into manageable chunks
- Ensures audio quality and timing

### Image Processing (tools.py)
- Manages text overlay on template images
- Handles font sizing and text wrapping
- Ensures visual appeal and readability

### Video Creation (main.py)
- Synchronizes audio with video template
- Overlays processed images
- Ensures final video meets TikTok's requirements

## Limitations
- Maximum story length is determined by TikTok's video length limits
- Audio generation may take time for longer stories
- Internet connection required for AI processing

## Troubleshooting
- **Error: API key not found** - Ensure your Groq API key is correctly set up
- **Video generation fails** - Check that all template files are present
- **Text-to-speech fails** - Ensure internet connection and valid API key

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.


## Acknowledgments
- Groq for providing the AI backend
- Streamlit for the web interface framework
- The open-source community for various tools and libraries

