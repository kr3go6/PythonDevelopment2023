import shlex, cmd
from cowsay import list_cows, COW_PEN, Option, make_bubble, cowsay, cowthink, THOUGHT_OPTIONS

class CowLine(cmd.Cmd):
    prompt = ">>>"

    def do_list_cows(self, args):
        """Lists all cow file names in the given directory"""

        parsed = shlex.split(args)
        print(list_cows(parsed[0] if len(parsed) == 1 else COW_PEN))

    def do_make_bubble(self, args):
        """
        Wraps text is wrap_text is true, then pads text and sets inside a bubble.
        This is the text that appears above the cows
        Usage: make_bubble 'text' ["cowsay"/"cowthink" (OPTIONAL)]
        """

        parsed = shlex.split(args)
        brackets = THOUGHT_OPTIONS[parsed[1]] if (len(parsed) > 1) else THOUGHT_OPTIONS["cowsay"]

        print(make_bubble(parsed[0], brackets=brackets))

    def do_cowsay(self, args):
        """
        Similar to the cowsay command. Parameters are listed with their
        corresponding options in the cowsay command. Returns the resulting cowsay
        string
        """

        parsed = shlex.split(args)

        cow = parsed[parsed.index("-c") + 1] if "-c" in parsed else "default"
        eyes = parsed[parsed.index("-e") + 1] if "-e" in parsed else 'oo'
        tongue = parsed[parsed.index("-T") + 1] if "-T" in parsed else ''

        print(cowsay(parsed[0], cow=cow, eyes=eyes, tongue=tongue))

    def do_cowthink(self, args):
        """
        Similar to the cowthink command. Parameters are listed with their
        corresponding options in the cowthink command. Returns the resulting
        cowthink string
        """

        parsed = shlex.split(args)

        cow = parsed[parsed.index("-c") + 1] if "-c" in parsed else "default"
        eyes = parsed[parsed.index("-") + 1] if "-e" in parsed else 'oo'
        tongue = parsed[parsed.index("-T") + 1] if "-T" in parsed else ''

        print(cowsay(parsed[0], cow=cow, eyes=eyes, tongue=tongue))

    def complete_cowsay(self, prefix, line, start, end):
        hints = ["taxi", "skeleton", "00", "XX", "P", "W"]

        return list(filter(lambda x: x.startswith(prefix), hints))

    def complete_cowthink(self, prefix, line, start, end):
        hints = ["taxi", "skeleton", "00", "XX", "P", "W"]

        return list(filter(lambda x: x.startswith(prefix), hints))
        
    def complete_make_bubble(self, prefix, line, start, end):
        hints = ["cowsay", "cowthink"]
        return list(filter(lambda x: x.startswith(prefix), hints))

if __name__ == "__main__":
    CowLine().cmdloop()