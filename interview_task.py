file_path = "release_notes.txt"
unique_element = "Issue"
second_element = "Title"


def findMissingNotes(filename):
    flag = False
    file = open(filename, 'r')
    lines = file.readlines()
    missing_notes = []
    current_note = None
    for line in lines:
        if "Owner" in line and flag:
            flag = False
            owner = line.split(":")[1].strip()
            if owner not in ["chdauto", "syspdbuild", "syspdbuild2"]:
                missing_notes.append((current_note, owner))
            else:
                if missing_notes:
                    missing_notes.pop()
        if "[ NOTE_MISSING ]" in line:
            current_note = line.split("#")[1].strip()
            flag = True
    return missing_notes


def findUniqeIssues(filename):
    issues = set()
    cur_title = ""
    file = open(filename, 'r')
    lines = file.readlines()
    for line in lines:
        if second_element in line:
            cur_title = line.split(":")[1].strip()
        if unique_element in line:
            if line.split(":")[1].strip() not in issues:
                issues.add((line.split(":")[1].strip(), cur_title))

    return issues


def printSummary(issues, missing_notes):
    for issue in issues:
        print("[" + issue[0] + "]", issue[1])
    print("")
    print("Commits with missing git notes:")
    for note in missing_notes:
        print("[ NOTE_MISSING ] Commit #" + note[0])
        print("@" + note[1] + ", Please add git notes to this commit!")


issues = findUniqeIssues(file_path)
missing_notes = findMissingNotes(file_path)
printSummary(issues, missing_notes)
