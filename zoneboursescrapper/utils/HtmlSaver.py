import os


class HtmlSaver:
    def __init__(self, to_dir, company_name):
        self.to_dir = to_dir
        self.company_name = company_name

    def save_html(self, response, page_number):
        file_path = self.to_dir + "/" + self.company_name + "/page" + str(page_number) + ".html"
        directory = os.path.dirname(file_path)
        if not os.path.exists(directory):
            os.makedirs(directory)
        with open(file_path, 'w') as html_file:
            html_file.write(response.text)
