import os
import sys
import subprocess

def find_first_subdirectory(path):
    # List all directories in the given path and return the first one found
    for folder_name in os.listdir(path):
        folder_path = os.path.join(path, folder_name)
        if os.path.isdir(folder_path):
            return folder_path
    return None

def process_audio_files(base_path, output_base_path):
    # Construct the path to the songs directory
    bin_dir = os.path.join(base_path, 'bin')
    songs_dir = os.path.join(bin_dir, 'assets', 'songs')

    # If the 'bin' directory does not exist, find the first subdirectory in the base path
    if not os.path.isdir(bin_dir):
        print(f"'bin' directory does not exist in {base_path}.")
        songs_dir = find_first_subdirectory(base_path)
        if songs_dir is None:
            print("No subdirectory found in the base path.")
            return
        songs_dir = os.path.join(songs_dir, 'assets', 'songs')  # Adjust path if necessary

    # Ensure the songs directory exists
    if not os.path.isdir(songs_dir):
        print(f"Songs directory {songs_dir} does not exist.")
        return

    # Create a directory for the output files named after the base folder
    base_folder_name = os.path.basename(os.path.normpath(base_path))
    output_folder = os.path.join(output_base_path, base_folder_name)
    os.makedirs(output_folder, exist_ok=True)

    # Iterate through each folder in the songs directory
    for folder_name in os.listdir(songs_dir):
        folder_path = os.path.join(songs_dir, folder_name)
        if os.path.isdir(folder_path):
            voices_file = os.path.join(folder_path, 'Voices.ogg')
            inst_file = os.path.join(folder_path, 'Inst.ogg')
            output_file = os.path.join(output_folder, f'{folder_name}.flac')

            # Check if both input files exist
            if os.path.isfile(voices_file) and os.path.isfile(inst_file):
                # Construct the ffmpeg command
                ffmpeg_command = [
                    'ffmpeg',
                    '-i', voices_file,
                    '-i', inst_file,
                    '-filter_complex', '[0:a][1:a]amerge=inputs=2[a]',
                    '-map', '[a]',
                    '-ar', '48000',
                    '-sample_fmt', 's32',
                    '-ac', '2',
                    output_file
                ]

                # Run the ffmpeg command
                try:
                    subprocess.run(ffmpeg_command, check=True)
                    print(f"Processed {folder_name} into {output_file}")
                except subprocess.CalledProcessError as e:
                    print(f"Error processing {folder_name}: {e}")
            else:
                print(f"Missing input files in {folder_name}")

if __name__ == "__main__":
    # Check if the correct number of arguments is provided
    if len(sys.argv) != 2:
        print("Usage: python script.py <full_base_path>")
        sys.exit(1)

    # Get the base path from command-line arguments
    base_path = sys.argv[1]
    
    # Get the directory where the script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Define the output path as the script directory
    output_base_path = script_dir
    
    process_audio_files(base_path, output_base_path)
