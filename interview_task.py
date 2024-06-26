def find_missing_elements(missing_element, filename):
    # Initialize variables
    # flag to keep track if we should process owner information
    flag = False
    file = open(filename, 'r')
    lines = file.readlines()
    missing_elements = []
    # current_note to keep track of the current note we've processed
    current_note = None

    # Iterate over each line in the file
    for line in lines:
        if "Owner" in line and flag:
            # Process owner information
            flag = False
            owner = line.split(":")[1].strip()
            # Check if owner is not in the exclusion list
            if owner not in ["chdauto", "syspdbuild", "syspdbuild2"]:
                missing_elements.append((current_note, owner))
            else:
                # Remove the note if the owner is in the exclusion list
                if missing_elements:
                    missing_elements.pop()
        if missing_element in line:
            # Process missing_element information
            current_note = line.split("#")[1].strip()
            flag = True
    return missing_elements


def find_unique_elements(unique_element, second_element, filename):
    # Initialize variables
    elements = set()
    cur_element = ""
    file = open(filename, 'r')
    lines = file.readlines()

    # Iterate over each line in the file
    for line in lines:
        if second_element in line:
            # Process second_element information
            cur_element = line.split(":")[1].strip()
        if unique_element in line:
            # Process unique_element information
            if line.split(":")[1].strip() not in elements:
                elements.add((line.split(":")[1].strip(), cur_element))

    return elements


def print_summary(unique_elements, missing_elements):
    # Print unique elements
    for element in unique_elements:
        print("[" + element[0] + "]", element[1])
    # Print commits with missing git notes
    print("\nCommits with missing git notes:")
    for element in missing_elements:
        print("[ NOTE_MISSING ] Commit #" + element[0])
        print("@" + element[1] + ", Please add git notes to this commit!")


# running it all
file_path = "release_notes.txt"
unq_element = "Issue"
scnd_element = "Title"
miss_element = "[ NOTE_MISSING ]"
issues = find_unique_elements(unq_element, scnd_element, file_path)
missing_notes = find_missing_elements(miss_element,
                                      file_path)
print_summary(issues, missing_notes)
