def parse_file(missing_element, unique_element, second_element,
               filename):
    # Initialize variables
    # flag to keep track if we should process owner information
    flag = False
    file = open(filename, 'r')
    lines = file.readlines()
    missing_elements = []
    # current_note to keep track of the current note we've processed
    current_note = None
    elements = set()
    cur_element = ""

    # Iterate over each line in the file
    for line in lines:
        # Process second_element information
        if second_element in line:
            cur_element = line.split(":")[1].strip()

        # Process unique_element information
        if unique_element in line:
            if line.split(":")[1].strip() not in elements:
                elements.add((line.split(":")[1].strip(), cur_element))

        # Process owner information
        if "Owner" in line and flag:
            flag = False
            owner = line.split(":")[1].strip()
            if owner not in ["chdauto", "syspdbuild", "syspdbuild2"]:
                missing_elements.append((current_note, owner))
            else:
                if missing_elements:
                    # Remove the note if the owner is in the exclusion list
                    missing_elements.pop()

        # Process missing_element information
        if missing_element in line:
            current_note = line.split("#")[1].strip()
            flag = True

    return missing_elements, elements


def print_summary(unique_elements, missing_elements):
    # Print unique elements
    for element in unique_elements:
        print("[" + element[0] + "]", element[1])

    # Print commits with missing git notes
    print("\nCommits with missing git notes:")
    for element in missing_elements:
        print("[ NOTE_MISSING ] Commit #" + element[0])
        print("@" + element[1] + ", Please add git notes to this commit!")


file_path = "release_notes.txt"
unq_element = "Issue"
scnd_element = "Title"
miss_element = "[ NOTE_MISSING ]"
missing_notes, issues = parse_file(miss_element, unq_element,
                                   scnd_element, file_path)
print_summary(issues, missing_notes)
