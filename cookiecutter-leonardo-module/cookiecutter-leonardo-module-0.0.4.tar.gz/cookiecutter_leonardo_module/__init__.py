
import sys
import os


def main():
    from cookiecutter.cli import main
    template_path = os.path.dirname(os.path.realpath(__file__))
    sys.argv.append(template_path)
    main()


if __name__ == "__main__":
    main()
