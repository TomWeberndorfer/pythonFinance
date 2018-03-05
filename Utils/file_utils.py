import re
import pandas as pd


def replace_in_file(file, pattern, subst):
    """
    Replaces a pattern in a file with another substitute.
    :param file: file path + name
    :param pattern: pattern to replace
    :param subst: substitute
    :return: nothing
    """

    # Read contents from file as a single string
    file_handle = open(file, 'r')
    file_string = file_handle.read()
    file_handle.close()

    # Use RE package to allow for replacement (also allowing for (multiline) REGEX)
    file_string = (re.sub(pattern, subst, file_string))

    # Write contents to file.
    # Using mode 'w' truncates the file.
    file_handle = open(file, 'w')
    file_handle.write(file_string)
    file_handle.close()


def get_hash_from_file(file, url):
    """
    reads the hash from the hashfile, due to given url (dict style with url and hash)
    :param file: hash file path + name
    :param url: url for hash
    :return: returns the hash id
    """
    
    data = pd.read_csv(file)
    test = data.set_index('url').T.to_dict('list')
    last_id = str(test[url][0])
    return last_id
