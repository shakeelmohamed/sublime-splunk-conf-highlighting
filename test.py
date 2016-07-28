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
            self.test_conf_lines = f.readlines()

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
        # TODO: handle the case of begin/end regex
        expected_keys = [
            "match",
            "name",
            "comment"
        ]
        expected_match_counts = {
            "invalid.illegal": 1,
            "comment.line": 3,
            "entity.name.function": 1,
            "support.function": 1,
            "keyword.operator": 1
        }

        patterns = self.json_obj["patterns"]

        # make sure test code isn't very broken
        # TODO: make this stricter
        self.assertEqual(len(expected_match_counts), len(patterns))

        for p in patterns:
            for item in expected_keys:
                self.assertIn(item, p)

            matches = 0
            for line in self.test_conf_lines:
                match = re.search(p["match"], line)
                if match is not None:
                    matches += 1
            self.assertEqual(matches, expected_match_counts[p["name"]], p["comment"] + " failed")

if __name__ == '__main__':
    unittest.main()