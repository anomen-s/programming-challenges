import sys
import re

# chatgpt

def load_words_from_files(file_list):
    word_set = set()
    for file in file_list:
        try:
            with open(file, 'r', encoding='utf-8') as f:
                for line in f:
                    words = re.findall(r'\b[a-zA-Z0-9]{5,7}\b', line)
                    word_set.update(words)
        except FileNotFoundError:
            print(f"Warning: File '{file}' not found.")
    return word_set

def highlight_missing_words(word_list, known_words):
    missing_words = [word for word in word_list if word not in known_words]
    return missing_words

def main():
    if len(sys.argv) < 2:
        print("Usage: python script.py <file1> <file2> ...")
        return
    
    file_list = sys.argv[1:]
    known_words = load_words_from_files(file_list)
    
    print("Enter text to check (Ctrl+C to exit):")
    
    try:
        while True:
            input_text = input()
            input_words = re.findall(r'\b[a-zA-Z0-9]{5,7}\b', input_text)
            
            missing_words = highlight_missing_words(input_words, known_words)
            
            if missing_words:
                #print("Words not found:")
                for word in missing_words:
                    print(f"\033[91m||{word} ||                                  ||tb: ||\033[0m")  # Highlight in red
            else:
                print("All words are found in the given files.")
    except KeyboardInterrupt:
        print("\nExiting...")

if __name__ == "__main__":
    main()
