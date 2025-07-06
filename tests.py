import unittest
from functions.run_python_file import run_python_file

def main():
    results = run_python_file("calculator", "main.py")
    print(results)
    results = run_python_file("calculator", "tests.py")
    print(results)
    results = run_python_file("calculator", "../main.py")
    print(results)
    results = run_python_file("calculator", "nonexistent.py")
    print(results)

if __name__ == "__main__":
    main()
