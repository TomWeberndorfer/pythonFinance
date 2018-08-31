import hashlib


class NewsUtils:

    @staticmethod
    def generate_hash(url, content):
        """
        Generates a hash for comparison containing url and content
        :param url: page url
        :param content:  content of the page
        :return: id (hash md5)
        """
        hash_id = hashlib.md5(url.encode('utf-8') + str(content).encode('utf-8')).hexdigest()
        return hash_id
