import argparse
import cowsay

MOOSET = "bdgpstwy"

parser = argparse.ArgumentParser()
parser.add_argument("-e", dest="eye_string", default="oo", help="select the appearance of the cow's eyes")
parser.add_argument("-f", dest="cowfile", help="specifies a particular cow picture file (\"cowfile\") to use")
parser.add_argument("-l", action="store_true", default="DONT_LIST_COWS",
                    help="list all cowfiles on the current COWPATH")
parser.add_argument("-n", action="store_true", help="if specified, the given message will not be word-wrapped")
parser.add_argument("-T", dest="tongue_string", default="", type=str, help="configures the tongue")
parser.add_argument("-W", dest="column", default=40, type=int,
                    help="specifies roughly where the message should be wrapped")
parser.add_argument("-b", action="store_true", help="initiates Borg mode")
parser.add_argument("-d", action="store_true", help="causes the cow to appear dead")
parser.add_argument("-g", action="store_true", help="invokes greedy mode")
parser.add_argument("-p", action="store_true", help="causes a state of paranoia to come over the cow")
parser.add_argument("-s", action="store_true", help="makes the cow appear thoroughly stoned")
parser.add_argument("-t", action="store_true", help="yields a tired cow")
parser.add_argument("-w", action="store_true", help="initiates wired mode")
parser.add_argument("-y", action="store_true", help="brings on the cow's youthful appearance")
parser.add_argument("message", default="", type=str, nargs="?", help="what does the cow say")

args = parser.parse_args()

if args.l != "DONT_LIST_COWS":
    print(cowsay.list_cows())
else:
    opts = "".join([opt for opt in MOOSET if args.__dict__[opt]])

    print(cowsay.cowsay(message=args.message,
                        preset=opts,
                        eyes=args.eye_string,
                        tongue=args.tongue_string,
                        width=args.column,
                        wrap_text=args.n,
                        cowfile=args.cowfile))
