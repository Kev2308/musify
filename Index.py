import streamlit as st
import subprocess
from pathlib import Path
import os
import io
import whisper

def delete_files_in_folder(folder_path):
    if not os.path.exists(folder_path):
        print(f"The folder '{folder_path}' does not exist.")
        return

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        if os.path.isfile(file_path):
            try:
                os.remove(file_path)
                print(f"Deleted: {file_path}")
            except Exception as e:
                print(f"Error deleting {file_path}: {e}")
def cleartmp():
    delete_files_in_folder("tmp\midi")
    delete_files_in_folder("tmp\seperated")
    delete_files_in_folder("tmp\music")




def separator(input_arg):
    subprocess.run(["python", "inference.py", "--input", input_arg])
def midi():
    subprocess.run(["basic-pitch", "tmp\midi", "tmp\seperated\Instruments.wav"])
def midi_ns():
    subprocess.run(["basic-pitch", "tmp\midi", f"tmp\music\{uploaded_file.name}"])
def save_uploadedfile(uploadedfile):
     with open(os.path.join("tmp\music",uploadedfile.name),"wb") as f:
         f.write(uploadedfile.getbuffer())
     return st.success("Uploaded File:{} Successfully".format(uploadedfile.name))

st.title("Musify")
if st.button("ClearTemp"):
    cleartmp()
uploaded_file = st.file_uploader("Choose a music file", type=["wav","flac","mp3"],accept_multiple_files=False)
if uploaded_file is not None:
    st.audio(uploaded_file.read(), format="audio/wav")
    #audio_details = {"FileName":uploaded_file.name,"FileType":uploaded_file.type}
    save_uploadedfile(uploaded_file)
    if st.button("Seperate audio and vocals"):
        separator(f"tmp\music\{uploaded_file.name}")
        Instruments = open('tmp\seperated\Instruments.wav', 'rb')
        audio_bytes0 = Instruments.read()
        st.audio(audio_bytes0, format='audio/wav')
        Vocals = open('tmp\seperated\Vocals.wav', 'rb')
        audio_bytes1 = Vocals.read()
        st.audio(audio_bytes1, format='audio/wav')
        if st.button("create midi file from seperated file"):
            #separator(f"tmp\music\{uploaded_file.name}")
            try:
                midi()
            except:
                st.text("warning vocals havent been seperated")
            midi_file_path = "tmp\midi\Generated_midi.mid"
            with open(midi_file_path, "rb") as file:
                midi_content = file.read()
            
            if st.download_button(
            label="Download MIDI File",
            data=io.BytesIO(midi_content).getvalue(),
            file_name=f"{midi_file_path.split('/')[-1]}",
            key="download_button1"
        ):
                st.write('Downloaded the midi file')
                with open(midi_file_path, "rb") as file:
                    midi_content = file.read()

    if st.button("create midi file "):
        #separator(f"tmp\music\{uploaded_file.name}")
        st.text("warning vocals havent been seperated")
        midi_ns()
        midi_file_path = "tmp\midi\Generated_midi.mid"
        with open(midi_file_path, "rb") as file:
            midi_content = file.read()
        
        if st.download_button(
        label="Download MIDI File",
        data=io.BytesIO(midi_content).getvalue(),
        file_name=f"{midi_file_path.split('/')[-1]}",
        key="download_button0"
    ):
            st.write('Downloaded the midi file')
            

    # Read MIDI file content
            with open(midi_file_path, "rb") as file:
                midi_content = file.read()

    # Create a download button for the MIDI file
    
    if st.button("generate lyrics file"):
        model = whisper.load_model("base")
        try:
            result = model.transcribe("tmp\seperated\Vocals.wav")
        except:
            st.write("seperated file not available using original file")
            result = model.transcribe(f"tmp\music\{uploaded_file.name}")
        st.text_area("Lyrics",result["text"])
    
