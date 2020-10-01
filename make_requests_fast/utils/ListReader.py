class ListReader:
    def __init__(self):
        pass

    @staticmethod
    def read(filename="resources/urls.csv"):
        url_raw_list = []
        with open(file=filename, mode="r") as f:
            url_raw_list = f.readlines()

        urls = []
        for url in url_raw_list:
            urls.append(url.rstrip())

        return urls