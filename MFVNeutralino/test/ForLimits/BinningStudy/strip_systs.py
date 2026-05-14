# Strip nuisance lines from datacards; write _statonly.txt alongside each.
# Usage:  python strip_systs.py [scheme1 scheme2 ...]  (default: all schemes)
import os, sys, glob

HERE = os.path.dirname(os.path.abspath(__file__))


def strip_one(src_path, dst_path):
    with open(src_path) as f:
        lines = f.readlines()

    out = []
    past_rate = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("rate ") or stripped.startswith("rate\t"):
            out.append(line)
            past_rate = True
            continue
        if past_rate:
            continue  # drop all nuisance lines
        # Fix kmax line to 0 (no nuisances)
        if stripped.startswith("kmax"):
            out.append("kmax 0  number of nuisance parameters\n")
        else:
            out.append(line)

    with open(dst_path, "w") as f:
        f.writelines(out)


def strip_scheme(scheme_dir):
    n = 0
    for ch in ("lep", "bjet"):
        ch_dir = os.path.join(scheme_dir, ch)
        if not os.path.isdir(ch_dir):
            continue
        for fn in glob.glob(os.path.join(ch_dir, "Datacard_*.txt")):
            if fn.endswith("_statonly.txt"):
                continue
            dst = fn.replace(".txt", "_statonly.txt")
            strip_one(fn, dst)
            n += 1
    return n


def main():
    datacards_dir = os.path.join(HERE, "datacards")
    schemes = sys.argv[1:] if len(sys.argv) > 1 else sorted(os.listdir(datacards_dir))
    for name in schemes:
        d = os.path.join(datacards_dir, name)
        if not os.path.isdir(d):
            continue
        n = strip_scheme(d)
        print("%-12s  stripped %d datacards" % (name, n))


if __name__ == "__main__":
    main()
