import argparse
import glob
import re
import os

from tqdm import tqdm

def fix_links(file_name, root_path, links):
    root_path_len = len(os.path.normpath(root_path).split(os.sep))
    file_path_len = len(os.path.normpath(file_name).split(os.sep))

    path_len = file_path_len - root_path_len
    if path_len == 1:
        rel_to_root_md = "../"
        rel_to_root_img = "./"
    elif path_len == 2:
        rel_to_root_md = "../../"
        rel_to_root_img = "../"
    else:
        print("ERROR: nested paths over 2 are not supported")
        exit()
    local_links = []
    for i in range(len(links)):
        if links[i].endswith(".png\n"):
            local_links.append(links[i].replace("./", rel_to_root_img))
        else:
            local_links.append(links[i].replace("./", rel_to_root_md))

    input_file = open(file_name, "r", encoding="utf-8")
    file_data = input_file.readlines()
    input_file.close()
    all_links = ""
    data = ""
    # extract links from file
    for line in file_data:
        if re.match(r"\[.+\]: .+\n", line):
            all_links += line
        else:
            data += line

    # remove all links that are part of the link file
    for link in local_links:
        link_id = link.split("]:")[0].replace("[","")
        all_links = re.sub(f"\[{link_id}\]\: .+\n".replace("(","\(").replace(")","\)"), "", all_links)

    data=data.strip()+"\n\n"+all_links
    # add necessary links
    for link in local_links:
        link_id = link.split(":")[0]
        if data.count(link_id):
            data += link

    output_file = open(file_name, "w", encoding="utf-8")
    output_file.write(data)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(prog="Fix links")
    parser.add_argument('-l', default="./links.txt", help='The location of the link file')
    parser.add_argument('-r', default="./docs/", help='The root of the mkdocs')
    parser.add_argument('paths', nargs='+', help='the paths to all files where the link should be fixed')

    args = parser.parse_args()

    links = open(args.l, "r" , encoding="utf-8").readlines()
    for link in links:
        link_id = link.split(":")[0]
        count = 0
        for other in links:
            if other.startswith(link_id):
                count += 1
        if count > 1:
            print(f"ERROR: the link with id {link_id} is duplicated.")
            exit()

    print(f"Found {args.l} file with {len(links)} links")

    for path in args.paths:
        files =  glob.glob(args.r + path)
        tqdm_files = tqdm(files)
        for f in tqdm_files:
            tqdm_files.set_postfix(file=f)
            fix_links(f, args.r, links)
