import exifread
import os
import json
import datetime

#Metadata extraction

def extract_metadata(file_path):
    try:
        with open(file_path, 'rb') as file:
            tags = exifread.process_file(file)
            metadata = {tag: str(tags[tag]) for tag in tags}
            return metadata
    except Exception as e:
        print(f"Error reading metadata from {file_path}: {e}")
        return {}

#file info test

import os
import datetime

def get_file_info(file_path):
    try:
        stats = os.stat(file_path)
        return {
            "File Size (bytes)": stats.st_size,
            "Creation Time": datetime.datetime.fromtimestamp(stats.st_ctime).isoformat(),
            "Last Modified Time": datetime.datetime.fromtimestamp(stats.st_mtime).isoformat(),
        }
    except Exception as e:
        print(f"Error getting file info for {file_path}: {e}")
        return {"Info": "Error retrieving file details"}


#process files

def process_directory(directory_path):
    all_metadata = {}

    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        
        if os.path.isfile(file_path):
            print(f"Processing file: {filename}")
            
            if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.tiff')):
                metadata = extract_metadata(file_path)
            elif filename.lower().endswith('.pdf'):
                metadata = extract_pdf_metadata(file_path)
            else:
                metadata = get_file_info(file_path)  # Fallback for unsupported files
            
            all_metadata[filename] = metadata
    
    return all_metadata


#save to file


def save_metadata(metadata, output_path="metadata_output.json"):
    try:
        with open(output_path, 'w') as f:
            json.dump(metadata, f, indent=4)
        print(f"Metadata saved to {output_path}")
    except Exception as e:
        print(f"Error saving metadata: {e}")


#Main

if __name__ == "__main__":
    directory_path = input("Enter the directory path to analyze: ")
    metadata = process_directory(directory_path)
    save_metadata(metadata)

