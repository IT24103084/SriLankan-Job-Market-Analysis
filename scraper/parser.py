def extract_between(lines, label):
    """
    Returns the value that appears after a label.
    Example:
    Company:
    ABC Company
    """

    for i, line in enumerate(lines):
        if line.strip() == label:
            if i + 1 < len(lines):
                return lines[i + 1].strip()

    return None