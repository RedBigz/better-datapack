import argparse
import fnmatch
import os
import shutil
import uuid

__app_name__ = "BetterDataPack"
__version__ = "0.0.1"
__entry__ = "cli.py"

BTRGLOB = "*.btr.mcfunction"

def main():
    parser = argparse.ArgumentParser("bdp")

    parser.add_argument("datapack", help="The datapack folder you wish to compile. Must contain *.btr.mcfunction files.")
    parser.add_argument("--output", "-o", default="dist", help="The output datapack folder.")

    args = parser.parse_args()

    indir: os.PathLike = args.datapack
    outdir: os.PathLike = args.output

    if os.path.exists(outdir): shutil.rmtree(outdir)
    os.makedirs(outdir, exist_ok=True)

    id = str(uuid.uuid4())

    idpath = os.path.join(outdir, "data", id, "functions")

    os.makedirs(idpath, exist_ok=True)

    for root, dirs, files in os.walk(indir):
        for file in files:
            path = os.path.join(root, file)
            if fnmatch.fnmatch(file, BTRGLOB):
                with open(path, "r") as mcf:
                    INDQ = False # in double quotes
                    INSQ = False # in single quotes

                    FUNCS = []
                    FUNCSCOPE = -1

                    FINAL = ""
                    
                    contents = mcf.read()

                    for i, c in enumerate(contents):
                        NF = False

                        match c:
                            case "'": INSQ = not INSQ
                            case "\"": INDQ = not INDQ

                            case "{":
                                if i > 0 and not INSQ and not INDQ:
                                    if contents[i - 1] == "$":
                                        FUNCSCOPE += 1
                                        FUNCS.append("")
                                        NF = True
                            
                            case "}":
                                if not INSQ and not INDQ:
                                    if contents[i + 1] == "$":
                                        fsid = str(uuid.uuid4())
                                        fsp = os.path.join(idpath, fsid + ".mcfunction")
                                        with open(fsp, "w+") as fspo:
                                            fspo.write(FUNCS[FUNCSCOPE])
                                        
                                        if FUNCSCOPE >= 0: FUNCSCOPE -= 1

                                        fcall = f"function {id}:{fsid}"

                                        if FUNCSCOPE == -1:
                                            FINAL += fcall
                                        else:
                                            FUNCS[FUNCSCOPE] += fcall
                            
                        if not NF:
                            if c == "$" and i > 0 and not INSQ and not INDQ and contents[i - 1] == "}": continue
                            if c == "}" and not INSQ and not INDQ and contents[i + 1] == "$": continue
                            if c == "$" and not INSQ and not INDQ and contents[i + 1] == "{": continue

                            if FUNCSCOPE == -1:
                                FINAL += c
                            else:
                                FUNCS[FUNCSCOPE] += c
                    
                    fp = path.replace(".btr.mc", ".mc").replace(os.path.join(indir, "data"), os.path.join(outdir, "data"))
                    os.makedirs(os.path.dirname(fp), exist_ok=True)
                    with open(fp, "w+") as nf:
                        nf.write(FINAL)
            else:
                dpath = path.replace(indir, outdir, 1)
                os.makedirs(os.path.dirname(dpath), exist_ok=True)
                shutil.copy(path, dpath)