import unittest
import json
import re


class TestSyntaxPatterns(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        with open("splunk-conf.json", "r") as f:
            # skip the first line, expected to be a comment
            lines = f.readlines()
            self.first_line = lines[0]
            lines = lines[1:]
            self.json_obj = json.loads("".join(lines))

        with open("test.conf", "r") as f:
            self.test_conf_str = f.read()

    def test_form(self):
        expected_keys = [
            "name",
            "scopeName",
            "fileTypes",
            "uuid",
            "patterns"
        ]
        for item in expected_keys:
            self.assertIn(item, self.json_obj)

    def test_patterns(self):
        expected_keys = [
            "match",
            "name",
            "comment"
        ]
        expected_match_counts = {
            "invalid.illegal": 2,
            "comment.line": 8,
            "entity.name.function": 2
        }

        expected_begin_end_counts = {
            "splunk.conf.setting": 11
        }

        patterns = self.json_obj["patterns"]

        # make sure test code isn't very broken
        # TODO: make this stricter
        self.assertEqual(len(expected_match_counts) + len(expected_begin_end_counts), len(patterns))

        for p in patterns:
            if p["name"] == "splunk.conf.setting":
                begin = p["begin"]
                end = p["end"]
                matches = re.findall(begin, self.test_conf_str, re.MULTILINE)
                self.assertEqual(len(matches), expected_begin_end_counts[p["name"]])
            else:
                for item in expected_keys:
                    self.assertIn(item, p)
                matches = re.findall(p["match"], self.test_conf_str, re.MULTILINE)
                self.assertEqual(len(matches), expected_match_counts[p["name"]])

if __name__ == '__main__':
    unittest.main()