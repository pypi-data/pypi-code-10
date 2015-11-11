#=============================================================================
# number formatting function by AS to remove trailing zeros
#=============================================================================
import decimal

def format_number_AS(in_num):

    try:
        dec = decimal.Decimal(in_num)
    except:
        print 'neither integer nor float: what do you want to format? '
        print 'you entered',in_num, type(in_num)
        return num
        #return 'bad programmer: BAD! enter a number only'

#    if len(str(num)) < 4:
#        return str(num)
    
    num             = float(in_num)
    outstr          = str(num)
    int_part        = int(num)
    dec_part        = num - float(int_part)
    nmax            = 6

    if dec_part == 0.0:
        return str(int_part)
    else:
#find how many digits exist in integer part
#        print 'original number', num
#        print 'integer part', int_part
#        print 'decimal part ',dec_part
        int_str  = str(int_part)

        if dec_part < 0.0 and int_part == 0:
            int_str = '-0'

        dec_part = round(dec_part,nmax)
#        print 'integer string',int_str
        fl_part  = str(dec_part).split('.')
        if len(fl_part) > 1:
            fl_part = fl_part[1]
        else:
            fl_part = fl_part[0]
        nint     = len(int_str)
#        print 'floating point string',fl_part
#have at most six characters in xlabel
        if nint >= nmax:
            return int_str
#            print 'returning integer string'
        else:
            for i in xrange(len(fl_part),5):
                fl_part = fl_part + '0'
            out_str = int_str + '.' + fl_part[0:nmax-1-nint]
            out_str = out_str.rstrip('0')
            out_str = out_str.rstrip('.')
        
    return outstr
