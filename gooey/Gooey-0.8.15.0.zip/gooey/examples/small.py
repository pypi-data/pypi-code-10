import sys
from gooey import Gooey, GooeyParser

@Gooey
def main():
  desc = "Example application to show Gooey's various widgets"
  file_help_msg = "Name of the file you want to process"
  my_cool_parser = GooeyParser(description=desc)
  my_cool_parser.add_argument("-w", "--writelog", default="No, NOT whatevs", help="write log to some file or something", nargs=3)
  args = my_cool_parser.parse_args()

if __name__ == '__main__':
  print sys.argv
  main()
