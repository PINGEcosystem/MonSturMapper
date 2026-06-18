'''
Copyright (c) 2025 Cameron S. Bodine
'''

#########
# Imports
import os, sys

# Add 'rockmapper' to the path, may not need after pypi package...
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PACKAGE_DIR = os.path.dirname(SCRIPT_DIR)
sys.path.append(PACKAGE_DIR)

# Set MONSTURMAPPER utils dir
USER_DIR = os.path.expanduser('~')
MM_UTILS_DIR = os.path.join(USER_DIR, '.monsturmapper')
if not os.path.exists(MM_UTILS_DIR):
    os.makedirs(MM_UTILS_DIR)

# Default function to run
if len(sys.argv) == 1:
    to_do = 'gui'
else:
    to_do = sys.argv[1]

#=======================================================================
def main(process):
    '''
    '''

    from monsturmapper.version import __version__
    print("\n\nMonSturMapper v{}".format(__version__))

    # Launch GUI
    if process == 'gui':
        print('\n\nLaunching MonSturMapper gui...\n\n')

        from monsturmapper.gui_main import gui

    return

#=======================================================================
if __name__ == "__main__":
    main(to_do)

