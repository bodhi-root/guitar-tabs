# File: build.py
# Build script for producing the static website.  This includes some generic
# builder code (copied from a separate project) as well as some custom
# extensions.  It finishes by executing the build script.

### Site Builder ##############################################################

import os
import frontmatter
import markdown
import glob
from jinja2 import Environment, FileSystemLoader


class Collection(object):
    """Represents a collection of file objects that can be transformed and manipulated.
    The data is stored in a dict named 'files' with keys representing paths to the
    files and values equal to the frontmatter.Post object parsed by frontmatter.
    Common transformations are available as class-level methods, but custom transformations
    can also be made easily.
    """

    def __init__(self):
        self.files = {}

    def load_file(self, path, base_path=None):
        """Loads a single file from the given 'path'.  'path' should be a relative path.
        This exact string will be used as the key for the file in our collection.  'base_path'
        can be used to specify a directory other than the working directory from which files
        can be loaded."""
        file_path = path
        if base_path is not None:
            file_path = os.path.join(base_path, file_path)
        with open(file_path) as fp:
            file = frontmatter.load(fp)

        self.files[path] = file

    def load_files(self, pattern="**/*.md", recursive=True, base_path=None):
        """Loads all files that match the given glob pattern.  This essentially runs
        glob.glob(pattern, recursive=recursive) from either the working directory or
        the directory specified by 'base_path'.  All matching files will be loaded using
        their paths as keys.  Paths are standardized so that forward slashes are used
        instead of backslashes.
        """
        # NOTE: glob.glob(..., root_dir=) is only available in Python 3.10.  We hack
        #       around this by joining the glob_pattern to the base_path and then stripping
        #       the base_path off of the results.
        glob_pattern = pattern
        if base_path is not None:
            glob_pattern = os.path.join(base_path, glob_pattern)

        paths = glob.glob(glob_pattern, recursive=recursive)
        for path in paths:
            rel_path = path
            if base_path is not None:
                rel_path = path[len(base_path):]
                rel_path = rel_path.replace('\\', '/')
                if rel_path[0] == '/':
                    rel_path = rel_path[1:]

            self.load_file(rel_path, base_path)

    def write(self, output_dir):
        """Writes all files to the specified directory.  The current set of keys will be
        used as the file names.  Each item's 'content' value will be used as the content
        of the file."""
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        for key, item in self.files.items():
            rel_dir, file_name = os.path.split(key)
            full_dir = os.path.join(output_dir, rel_dir)
            if not os.path.exists(full_dir):
                os.makedirs(full_dir)

            full_path = os.path.join(full_dir, file_name)
            with open(full_path, "w") as fp:
                fp.write(item.content)

    def remove_spaces(self, replace_with='-'):
        """Removes all spaces from path names, replacing them with the specified character"""
        new_files = {}
        for key, item in self.files.items():
            key = key.replace(' ', replace_with)
            new_files[key] = item
        self.files = new_files
        return self

    def markdown_to_html(self, file_extensions=[".md", ".markdown"], markdown_extensions=["extra"]):
        """Converts markdown content to HTML.  This will apply to any file keys ending with the
        given extensions (default=".md" and ".markdown").  The file extension will be replaced
        with ".html".  We call markdown.markdown(content, extensions=markdown_extensions) to perform
        the conversion.  The list of extensions lets us extend the capabilities of the markdown
        process as specified here: https://python-markdown.github.io/extensions/.
        """
        new_files = {}

        for key, item in self.files.items():

            is_markdown = False
            for file_ext in file_extensions:
                if key.endswith(file_ext):
                    is_markdown = True
                    end_index = len(key) - len(file_ext)
                    new_key = key[0:end_index] + ".html"
                    item.content = markdown.markdown(item.content, extensions=markdown_extensions)
                    new_files[new_key] = item
                    break

            if not is_markdown:
                new_files[key] = item

        self.files = new_files
        return self

    def apply_templates(self, jinja_env, default_template=None, globals={}):
        """Applies Jinja2 templates to our content.  A Jinja2.Environment provides the
        context for loading templates by name.  Each file object specifies the template
        it wants to use via the 'template' property.  A default_template can be specified
        for when this is missing.  Without a default, the file will be left alone.  The
        template is loaded, and then we call render().  The variables passed to render()
        include any global properties (as specified by 'global'), extended with properties
        from file's front-matter, and lastly a property named 'content' containing the
        file's content.
        """

        for key, item in self.files.items():
            template_name = item.get("template", default_template)
            if template_name is None:
                continue

            template = jinja_env.get_template(template_name)

            values = dict(globals)
            values.update({key: item[key] for key in item.keys()})
            values["content"] = item.content

            item.content = template.render(**values)


### Custom Functions ##########################################################

import json


def create_index(files):
    song_data_list = []
    for key, item in files.files.items():
        song_data = {
            "link": key
        }
        for var in ["title", "artist", "tuning", "rating", "difficulty"]:
            song_data[var] = item.get(var, None)

        song_data_list.append(song_data)

    metadata = {
        "title": "Song Index",
        "template": "song_index.html",
        "songData": json.dumps(song_data_list)
    }

    index_page = frontmatter.Post("This page does not have content", **metadata)
    files.files["index.html"] = index_page


### Script ####################################################################

import shutil

SRC_DIR = "src"
DST_DIR = "build"

if not os.path.exists(SRC_DIR):
    raise Exception(f"Source directory not found: {SRC_DIR}")
if os.path.exists(DST_DIR):
    shutil.rmtree(DST_DIR)

jinja_env = Environment(
    loader=FileSystemLoader("templates"),
    autoescape=True
)

global_vars = {
    "siteTitle": "Dan's Guitar Tabs"
}

files = Collection()
files.load_files("songs/*.md", base_path=SRC_DIR)
files.files.pop("songs/_template.md")
files.remove_spaces()
files.markdown_to_html()

create_index(files)

files.apply_templates(jinja_env, default_template="song.html", globals=global_vars)
files.write(DST_DIR)

# copy assets:
shutil.copytree("public", DST_DIR, dirs_exist_ok=True)
