import streamlit as st
from pathlib import Path
from moviepy.editor import VideoFileClip, AudioFileClip, ImageClip, CompositeVideoClip, concatenate_videoclips
import time
from tools import MediaProcessor
from text_to_speech import TextToSpeech
from LLM import StoryProcessor

class TikTokGenerator:
    def __init__(self):
        self.base_path = Path(__file__).parent
        self.paths = {
            'audio': self.base_path / 'output.mp3',
            'image': self.base_path / 'E-template.png',
            'video': self.base_path / 'output_video.mp4',
            'video_template': self.base_path / 'test2.mp4'
        }
        self.story_processor = StoryProcessor()
        self.media_processor = MediaProcessor()
        self.tts_processor = TextToSpeech()

    def process_video(self) -> bool:
        try:
            with VideoFileClip(str(self.paths['video_template'])) as video, \
                 AudioFileClip(str(self.paths['audio'])) as audio, \
                 ImageClip(str(self.paths['image'])) as img_clip:
                
                loop_count = int(audio.duration / video.duration) + 1
                extended_video = concatenate_videoclips([video] * loop_count)
                final_video = extended_video.subclip(0, audio.duration)
                
                img_clip = img_clip.set_duration(audio.duration).set_position('center')
                video_with_image = CompositeVideoClip([final_video, img_clip])
                final_clip = video_with_image.set_audio(audio)
                
                final_clip.write_videofile(str(self.paths['video']), codec='libx264')
                
            return True
        except Exception as e:
            st.error(f"Error processing video: {str(e)}")
            return False

def initialize_session_state():
    if 'generation_complete' not in st.session_state:
        st.session_state.generation_complete = False
    if 'last_story' not in st.session_state:
        st.session_state.last_story = ""
    if 'story_summary' not in st.session_state:
        st.session_state.story_summary = ""
    if 'story_title' not in st.session_state:
        st.session_state.story_title = ""
    if 'available_downloads' not in st.session_state:
        st.session_state.available_downloads = set()

def create_download_buttons(generator):
    """Create download buttons for available files"""
    st.subheader("Download Generated Content")
    
    # Check which files are available
    available_files = {
        file_type: path for file_type, path in generator.paths.items() 
        if path.exists() and file_type != 'video_template'
    }
    
    if not available_files:
        st.warning("No files are available for download yet.")
        return

    # Create columns dynamically based on number of available files
    columns = st.columns(len(available_files))
    
    for i, (file_type, file_path) in enumerate(available_files.items()):
        with columns[i]:
            try:
                with open(file_path, "rb") as file:
                    file_bytes = file.read()
                    mime_type = f"{'video' if 'video' in file_type else 'audio' if file_type == 'audio' else 'image'}/{file_path.suffix[1:]}"
                    st.download_button(
                        label=f"Download {file_type.capitalize()}",
                        data=file_bytes,
                        file_name=file_path.name,
                        mime=mime_type,
                        key=f"download_{file_type}"
                    )
            except Exception as e:
                st.error(f"Error preparing download for {file_type}: {str(e)}")

def main():
    st.title("TikTok Story Generator")
    
    initialize_session_state()
    generator = TikTokGenerator()

    # Create two columns
    col1, col2 = st.columns([2, 1])
    
    with col1:
        user_story = st.text_area("Paste your story here", height=200)
    
    story_changed = user_story != st.session_state.last_story
    
    with col2:
        generate_button = st.button("Generate Content", key="generate_button")
        
    if generate_button or (story_changed and user_story.strip()):
        if not user_story.strip():
            st.error("Please input a story before generating.")
            return

        st.session_state.last_story = user_story
        st.session_state.generation_complete = False
        st.session_state.available_downloads = set()
        
        progress_placeholder = st.empty()
        status_placeholder = st.empty()
        
        try:
            with progress_placeholder.container():
                progress_bar = st.progress(0)
                
                # Generate title and summary
                status_placeholder.text("Generating story elements...")
                progress_bar.progress(10)
                st.session_state.story_title = generator.story_processor.get_story_title(user_story)
                st.session_state.story_summary = generator.story_processor.get_story_summary(user_story)
                progress_bar.progress(20)
                
                # Generate audio
                status_placeholder.text("Generating audio...")
                audio_success = generator.tts_processor.generate_audio(user_story)
                if audio_success:
                    st.session_state.available_downloads.add('audio')
                progress_bar.progress(40)
                
                # Generate image
                status_placeholder.text("Generating image...")
                image_success = generator.media_processor.add_text_to_image(user_story)
                if image_success:
                    st.session_state.available_downloads.add('image')
                progress_bar.progress(60)
                
                # Generate video
                status_placeholder.text("Generating video...")
                video_success = generator.process_video()
                if video_success:
                    st.session_state.available_downloads.add('video')
                progress_bar.progress(100)
                
                status_placeholder.empty()
                
                if st.session_state.available_downloads:
                    st.session_state.generation_complete = True
                    st.success(f"Generated: {', '.join(st.session_state.available_downloads)}")
                else:
                    st.error("Failed to generate any content.")
                
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
        finally:
            progress_placeholder.empty()

    # Display summary and download buttons
    if st.session_state.generation_complete:
        with st.expander("Generated Content", expanded=True):
            st.subheader(st.session_state.story_title)
            st.write(st.session_state.story_summary)
        
        create_download_buttons(generator)

if __name__ == "__main__":
    main()