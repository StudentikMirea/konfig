import os
import hashlib
import sys

def calculate_hash(file_path):
    """Вычисляет MD5 хеш-сумму файла."""
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def find_duplicates(root_path):
    """Находит файлы-дубликаты в заданном каталоге и подкаталогах."""
    file_hashes = {}
    duplicates = []

    for dirpath, _, filenames in os.walk(root_path):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            file_hash = calculate_hash(file_path)

            if file_hash in file_hashes:
                duplicates.append((file_path, file_hashes[file_hash]))
            else:
                file_hashes[file_hash] = file_path

    return duplicates

def main():
    if len(sys.argv) != 2:
        print("Usage: python find_duplicates.py <path>")
        return

    root_path = sys.argv[1]
    duplicates = find_duplicates(root_path)

    if duplicates:
        print("Duplicate files found:")
        for duplicate in duplicates:
            print(f"{duplicate[0]} is a duplicate of {duplicate[1]}")
    else:
        print("No duplicate files found.")

if __name__ == "__main__":
    main()
