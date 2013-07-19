# -*- coding: utf-8 -*-
import re
import sys
import os
from pyparsing import *


def pdf2raw(bretz_text):
    """Remove unnecessary characters that resulted from copying
    and pasting from the Bretz's book into a text file. This will
    remove all newlines, leaving one long concatenated string.

    Note: after this, the user must go into the resulting test and
    break up the cave entries to one per line."""
    # Read in file.
    raw_text = open(bretz_text, 'rb').read()

    # Remove page number annotations and unnecessary newlines.
    ## Each page is separated by the following sequence:
    ##  |428
    ##  |_
    ##  |Page 428
    ##  |428 Missouri Geological Survey and Water Resources
    ##
    ## or
    ##
    ##  |427
    ##  |_
    ##  |Page 427
    ##  |Caves of Missouri 427
    ##
    ##  These need to be removed. The following regex will do so.
    regex = "\d+\s+_\s+Page \d+\s+(?:\d+ Missouri Geological Survey and Water Resources|Caves of Missouri \d+)* *(\w+|\s+)"
    p = re.compile(regex)
    raw_text = "".join(filter(None, p.split(raw_text)))

    # Remove unnecessary newlines.
    raw_text = " ".join(raw_text.split('\n'))
    raw_text = "".join(raw_text.split('\r'))
    
    return re.sub('l/', '1/', re.sub(b'¼', b'1/4', raw_text))


if __name__ == "__main__":
    f = sys.argv[1]
    raw = bretz2text(f)
    
    o = os.path.join(os.path.dirname(f), "Cleaned " + os.path.basename(f))
    with open(o, 'wb') as output_file:
      output_file.write(raw)
