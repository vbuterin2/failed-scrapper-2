import unittest
from zoneboursescrapper.utils.HtmlSaver import HtmlSaver
from requests import get
from pathlib import Path


class MyTestCase(unittest.TestCase):
    def test_something(self):
        html_saver = HtmlSaver("saved_html", "debug")
        html_saver.save_html(get("https://g.co"), 1)
        html_saver.save_html(get("https://g.co"), 2)
        html_saver.save_html(get("https://g.co"), 3)
        html_saver.save_html(get("https://g.co"), 4)

        self.assertTrue(Path("saved_html/debug/page1.html").is_file())
        self.assertTrue(Path("saved_html/debug/page2.html").is_file())
        self.assertTrue(Path("saved_html/debug/page3.html").is_file())
        self.assertTrue(Path("saved_html/debug/page4.html").is_file())


if __name__ == '__main__':
    unittest.main()
