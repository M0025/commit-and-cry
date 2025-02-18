"""
Determine whether to update the model:
If only the model version has changed:
    If version increased: Return TRUE
    If version decreased: Return FALSE
If other changes exist: Return TRUE
"""

import argparse

def parse_diff_file(diff_file_path):
    changes = []
    with open(diff_file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            if line.startswith('-') and not line.startswith('---'):
                changes.append(line.strip())
            elif line.startswith('+') and not line.startswith('+++'):
                changes.append(line.strip())
    return changes

def compare_versions(old_version, new_version):
    old_parts = list(map(int, old_version.split('.')))
    new_parts = list(map(int, new_version.split('.')))
    return new_parts > old_parts

def main():
    parser = argparse.ArgumentParser(description='Process diff file.')
    parser.add_argument('diff_file_path', type=str, help='Path to the diff file')
    args = parser.parse_args()

    diff_file_path = args.diff_file_path
    changes = parse_diff_file(diff_file_path)

    if not changes:
        print("No changes detected")
        return False

    old_version = None
    new_version = None
    only_model_version_changed = True

    for change in changes:
        if change.startswith('-model_version:'):
            old_version = change.split(':')[1].strip()
        elif change.startswith('+model_version:'):
            new_version = change.split(':')[1].strip()
        else:
            only_model_version_changed = False

    if only_model_version_changed:
        if old_version and new_version:
            print(f"Version change: {old_version} -> {new_version}")
            return compare_versions(old_version, new_version)
        else:
            print("Incomplete version information")
            return False
    else:
        print("Other changes detected in config file")
        return True

if __name__ == "__main__":
    result = main()
    print(result)