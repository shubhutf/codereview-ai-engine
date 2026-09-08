def parse_patch(patch: str):
    lines = patch.split("\n")
    new_line = 0
    result = []

    for line in lines:
        if line.startswith("@@"):
            import re
            match = re.search(r"\+(\d+)", line)
            if match:
                new_line = int(match.group(1))
        elif line.startswith("+") and not line.startswith("+++"):
            result.append({
                "line": new_line,
                "content": line[1:]
            })
            new_line += 1
        elif line.startswith(" "):
            new_line += 1
        elif line.startswith("-"):
            continue

    return result

def process_pr_files(files):
    all_lines = []

    for file in files:
        patch = file.get("patch")
        if not patch:
            continue

        parsed_lines = parse_patch(patch)

        for item in parsed_lines:
            all_lines.append({
                "file": file["filename"],
                "line": item["line"],
                "content": item["content"]
            })

    return all_lines