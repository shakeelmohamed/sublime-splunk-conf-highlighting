import os

import sublime
import sublime_plugin

""" TODO:
 * make this madness work on windows dynamically (http://blogs.technet.com/b/heyscriptingguy/archive/2014/09/15/powertip-use-powershell-to-find-path-for-processes.aspx)
 * Test on Sublime Text 2
 * Test on Windows
 * Test on Linux
 * Parse the btool output, and highlight those lines - also potentially open files
 * Investigate file_regex
 * Investigate line_regex
 * Investigate using a setting for SPLUNK_HOME
 * Hide the excessive output (finished, shell_cmd, dir, path)
 * Handle cases where splunkd is in the path multiple times
 * Add a debug command, same thing but with --debug
"""

def get_splunk_path(platform):
    if platform == "windows":
        ret = "C:\\\\Program%20Files\\Splunk\\Splunk.exe"
    else:
        """ Super hack:
        * Find running process
        * Regex search results for "bin.splunkd" (ie: bin/splunkd)
        * Trim the first result (should be this script)
        * Take the 11th column of text, the path name
        * Remove "splunkd"
        * Append "splunk"
        """
        ret = '$(ps aux | grep "bin.splunkd" | head -1 | awk \'{print $11}\' | sed -e \'s/splunkd//\')splunk'
    return ret


class BtoolCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        filepath = self.view.file_name()
        packages = sublime.packages_path()

        args = {
            "shell_cmd": '%s cmd btool check' % get_splunk_path(sublime.platform())
            # ,
            # "file_regex": r"JSHint: (.+)\]",
            # "line_regex": r"(\d+),(\d+): (.*)$"
        }
        self.view.window().run_command('exec', args)