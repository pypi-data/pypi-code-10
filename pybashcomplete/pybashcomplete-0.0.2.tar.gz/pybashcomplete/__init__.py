''' pybashcomplete

Bash completion utility for python scripts
'''


def main():
    from .parser import main as main_func
    main_func()

if __name__ == '__main__':
    main()
