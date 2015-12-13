import argparse,sys
import yaccli.stack

def yac_options(string):
    # options can be most anything. Let the 
    # sub-functions argparse handle validation
    return string

def main():

    parser = argparse.ArgumentParser('Your Atlassian Cloud',add_help=False)
    
    # required args
    parser.add_argument('operation',  
                        help='the yac operation to perform', 
                        choices=['stack','app','db','container'])
    
    parser.add_argument('option', 
                        help='options',
                        nargs='*',
                        type=yac_options)

    # trap -h. let operations handle most of the help
    parser.add_argument('-h', action='store_true')

    args = parser.parse_args()

    # strip operation from args list
    sys.argv = sys.argv[1:]

    if args.operation == 'stack':

        return yaccli.stack.main()

    else:

        return "operation not yet implemented"
        