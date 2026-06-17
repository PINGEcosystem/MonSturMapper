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

# Set GHOSTVISION utils dir
USER_DIR = os.path.expanduser('~')
MM_UTILS_DIR = os.path.join(USER_DIR, '.monsturmapper')
if not os.path.exists(MM_UTILS_DIR):
    os.makedirs(MM_UTILS_DIR)

# Default function to run

# print("Parameters passed to MonSturMapper:")
# print(sys.argv[2])
# sys.exit()

if len(sys.argv) == 1:
    to_do = 'gui'
else:
    to_do = sys.argv[1:]


#=======================================================================
def main(process):
    '''
    '''

    from monsturmapper.version import __version__
    print("\n\nMonSturMapper v{}".format(__version__))

    # Launch GUI
    if process[0] == 'gui':
        print('\n\nLaunching MonSturMapper gui...\n\n')

        # from monsturmapper.gui_main import gui

    elif process[0] == 'gui_batch':
        print('\n\nLaunching MonSturMapper batch gui...\n\n')
        
        # from monsturmapper.gui_main import gui_batch

        # gui_batch()

    elif process[0] == 'mask_shadows':

        print('\n\nRemoving transect shadows...\n\n')

        try:
            transect_path = to_do[1]
        except:
            print('\n\nNo transect path provided for shadow removal.\n\n')
            sys.exit(1)

        from monsturmapper.test_utilities import remove_transect_shadows


        remove_transect_shadows(transect_path)

    else:
        print('\n\nUnknown process: {}'.format(process))

        print('Valid options are: "gui" or "gui_batch"')

        sys.exit(1)

    return

#=======================================================================
if __name__ == "__main__":
    main(to_do)

