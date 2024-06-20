file_path = "release_notes.txt"

def findMissingElements(missing_element, filename):
    flag = False
    file = open(filename, 'r')
    lines = file.readlines()
    missing_elements = []
    current_note = None
    for line in lines:
        if "Owner" in line and flag:
            flag = False
            owner = line.split(":")[1].strip()
            if owner not in ["chdauto", "syspdbuild", "syspdbuild2"]:
                missing_elements.append((current_note, owner))
            else:
                if missing_elements:
                    missing_elements.pop()
        if missing_element in line:
            current_note = line.split("#")[1].strip()
            flag = True
    return missing_elements


def findUniqeElements(unique_element, second_element, filename):
    elements = set()
    cur_element = ""
    file = open(filename, 'r')
    lines = file.readlines()
    for line in lines:
        if second_element in line:
            cur_element = line.split(":")[1].strip()
        if unique_element in line:
            if line.split(":")[1].strip() not in elements:
                elements.add((line.split(":")[1].strip(), cur_element))

    return elements


def printSummary(unique_elements, missing_elements):
    for element in unique_elements:
        print("[" + element[0] + "]", element[1])
    print("\nCommits with missing git notes:")
    for element in missing_elements:
        print("[ NOTE_MISSING ] Commit #" + element[0])
        print("@" + element[1] + ", Please add git notes to this commit!")


issues = findUniqeElements("Issue", "Title", file_path)
missing_notes = findMissingElements("[ NOTE_MISSING ]", file_path)
printSummary(issues, missing_notes)
