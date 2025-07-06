import unittest
from functions.get_files_info import get_files_info

def main():
    results = get_files_info("calculator", ".")
    print(f"Result for current directory:\n{results}")
    results = get_files_info("calculator", "pkg")
    print(f"Result for 'pkg' directory:\n{results}")
    results = get_files_info("calculator", "/bin")
    print(f"Result for '/bin' directory:\n{results}")
    results = get_files_info("calculator", "../")
    print(f"Result for '../' directory:\n{results}")

if __name__ == "__main__":
    main()
