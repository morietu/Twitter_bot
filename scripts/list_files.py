import os

def list_files_recursively(base_dir="."):
    print(f"📂 プロジェクト構成（基準ディレクトリ: {os.path.abspath(base_dir)}）\n")
    for root, dirs, files in os.walk(base_dir):
        level = root.replace(base_dir, '').count(os.sep)
        indent = '  ' * level
        print(f"{indent}{os.path.basename(root)}/")
        for f in files:
            print(f"{indent}  {f}")

if __name__ == "__main__":
    list_files_recursively(".")
