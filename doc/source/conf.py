"""Sphinx documentation configuration file."""

# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

from datetime import datetime
import os
import warnings

from ansys_sphinx_theme import ansys_favicon, get_version_match, pyansys_logo_black
import requests
from sphinx_gallery.sorting import FileNameSortKey

import ansys.mechanical.core as pymechanical
from ansys.mechanical.core.embedding.initializer import (
    SUPPORTED_MECHANICAL_EMBEDDING_VERSIONS_WINDOWS,
)

# necessary when building the sphinx gallery
pymechanical.BUILDING_GALLERY = True

# suppress annoying matplotlib bug
warnings.filterwarnings(
    "ignore",
    category=UserWarning,
    message="Matplotlib is currently using agg, which is a non-GUI backend, "
    "so cannot show the figure.",
)


# -- Project information -----------------------------------------------------

project = "ansys.mechanical.core"
copyright = f"(c) {datetime.now().year} ANSYS, Inc. All rights reserved"
author = "ANSYS Inc."
release = version = pymechanical.__version__
cname = os.getenv("DOCUMENTATION_CNAME", default="mechanical.docs.pyansys.com")
switcher_version = get_version_match(version)


def intersphinx_pymechanical(switcher_version: str):
    """Auxiliary method to build the intersphinx mapping for PyMechanical.

    Notes
    -----
    If the objects.inv file is not found whenever it is a release, the method
    will default to the "dev" version. If the objects.inv file is not found
    for the "dev" version, the method will return an empty string.

    Parameters
    ----------
    switcher_version : str
        Version of the PyMechanical package.

    Returns
    -------
    str
        The intersphinx mapping for PyMechanical.
    """
    prefix = "https://mechanical.docs.pyansys.com/version"

    # Check if the object.inv file exists
    response = requests.get(f"{prefix}/{switcher_version}/objects.inv")

    if response.status_code == 404:
        if switcher_version == "dev":
            return ""
        else:
            return intersphinx_pymechanical("dev")
    else:
        return f"{prefix}/{switcher_version}"


# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
# -- General configuration ---------------------------------------------------
# Sphinx extensions
extensions = [
    "ansys_sphinx_theme.extension.autoapi",
    "jupyter_sphinx",
    "notfound.extension",
    "numpydoc",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.coverage",
    "sphinx.ext.doctest",
    "sphinx.ext.extlinks",
    "sphinx.ext.intersphinx",
    "sphinx_autodoc_typehints",
    "sphinx_copybutton",
    "sphinx_design",
    "sphinx_gallery.gen_gallery",
    "sphinxemoji.sphinxemoji",
]

# Intersphinx mapping
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "scipy": ("https://docs.scipy.org/doc/scipy/", None),
    "numpy": ("https://numpy.org/devdocs", None),
    "matplotlib": ("https://matplotlib.org/stable", None),
    "grpc": ("https://grpc.github.io/grpc/python/", None),
    "pypim": ("https://pypim.docs.pyansys.com/version/dev/", None),
}

# Conditional intersphinx mapping
if intersphinx_pymechanical(switcher_version):
    intersphinx_mapping["ansys.mechanical.core"] = (
        intersphinx_pymechanical(switcher_version),
        None,
    )

suppress_warnings = ["label.*", "autoapi.python_import_resolution", "design.grid", "config.cache"]
# supress_warnings = ["ref.option"]


# numpydoc configuration
numpydoc_use_plots = True
numpydoc_show_class_members = False
numpydoc_xref_param_type = True
numpydoc_validate = True
numpydoc_validation_checks = {
    "GL06",  # Found unknown section
    "GL07",  # Sections are in the wrong order.
    # "GL08",  # The object does not have a docstring
    "GL09",  # Deprecation warning should precede extended summary
    "GL10",  # reST directives {directives} must be followed by two colons
    "SS01",  # No summary found
    "SS02",  # Summary does not start with a capital letter
    # "SS03", # Summary does not end with a period
    "SS04",  # Summary contains heading whitespaces
    # "SS05", # Summary must start with infinitive verb, not third person
    "RT02",  # The first line of the Returns section should contain only the
    # type, unless multiple values are being returned"
}

numpydoc_validation_exclude = {  # set of regex
    # grpc files
    r"\.*pb2\.*",
}

# Favicon
html_favicon = ansys_favicon

# notfound.extension
notfound_template = "404.rst"
notfound_urls_prefix = "/../"

# static path
html_static_path = ["_static"]
templates_path = ["_templates"]
# The suffix(es) of source filenames.
source_suffix = ".rst"

# The master toctree document.
master_doc = "index"

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = "en"

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = [
    "_build",
    "Thumbs.db",
    ".DS_Store",
    "links.rst",
]

# make rst_epilog a variable, so you can add other epilog parts to it
rst_epilog = ""
# Read link all targets from file
with open("links.rst") as f:
    rst_epilog += f.read()

current_mechanical_version = next(iter(SUPPORTED_MECHANICAL_EMBEDDING_VERSIONS_WINDOWS.keys()))
rst_epilog = rst_epilog.replace("%%VERSION%%", f"v{current_mechanical_version}")
# The name of the Pygments (syntax highlighting) style to use.
pygments_style = "sphinx"

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = False

# Copy button customization ---------------------------------------------------
# exclude traditional Python prompts from the copied code
copybutton_prompt_text = r">>> ?|\.\.\. "
copybutton_prompt_is_regexp = True

# -- Sphinx Gallery Options ---------------------------------------------------
sphinx_gallery_conf = {
    # convert rst to md for ipynb
    "pypandoc": True,
    # path to your examples scripts
    "examples_dirs": ["../../examples/"],
    # path where to save gallery generated examples
    "gallery_dirs": ["examples/gallery_examples"],
    # Pattern to search for example files
    "filename_pattern": r"\.py",
    # Remove the "Download all examples" button from the top level gallery
    "download_all_examples": False,
    # Sort gallery example by file name instead of number of lines (default)
    "within_subsection_order": FileNameSortKey,
    # directory where function granular galleries are stored
    "backreferences_dir": None,
    # Modules for which function level galleries are created.  In
    "doc_module": "ansys-mechanical-core",
    "image_scrapers": ("matplotlib"),
    "ignore_pattern": "flycheck*",
    "thumbnail_size": (350, 350),
}

# -- Options for HTML output -------------------------------------------------
html_short_title = html_title = "PyMechanical"
html_theme = "ansys_sphinx_theme"
html_logo = pyansys_logo_black
html_context = {
    "github_user": "pyansys",
    "github_repo": "pymechanical",
    "github_version": "main",
    "doc_path": "doc/source",
}
html_theme_options = {
    "switcher": {
        "json_url": f"https://{cname}/versions.json",
        "version_match": get_version_match(version),
    },
    "check_switcher": False,
    "github_url": "https://github.com/ansys/pymechanical",
    "show_prev_next": False,
    "show_breadcrumbs": True,
    "collapse_navigation": True,
    "use_edit_page_button": True,
    "header_links_before_dropdown": 4,  # number of links before the dropdown menu
    "additional_breadcrumbs": [
        ("PyAnsys", "https://docs.pyansys.com/"),
    ],
    "icon_links": [
        {
            "name": "Support",
            "url": "https://github.com/ansys/pymechanical/discussions",
            "icon": "fa fa-comment fa-fw",
        },
    ],
    "use_meilisearch": {
        "api_key": os.getenv("MEILISEARCH_PUBLIC_API_KEY", ""),
        "index_uids": {
            f"pymechanical-v{get_version_match(version).replace('.', '-')}": "PyMechanical",
        },
    },
    "cheatsheet": {
        "url": "https://cheatsheets.docs.pyansys.com/pymechanical_cheat_sheet.pdf",
        "title": "PyMechanical cheat sheet",
        "thumbnail": "https://cheatsheets.docs.pyansys.com/pymechanical_cheat_sheet.png",
        "needs_download": True,
    },
    "ansys_sphinx_theme_autoapi": {"project": project, "templates": "_templates/autoapi"},
    "navigation_depth": 10,
}

# -- Options for HTMLHelp output ---------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = "pymechanicaldoc"


# -- Options for LaTeX output ------------------------------------------------
latex_elements = {}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (
        master_doc,
        f"pymechanical-Documentation-{version}.tex",
        "ansys.mechanical.core Documentation",
        author,
        "manual",
    ),
]


# -- Options for manual page output ------------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (master_doc, "ansys.mechanical.core", "ansys.mechanical.core Documentation", [author], 1)
]


# -- Options for Texinfo output ----------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (
        master_doc,
        "ansys.mechanical.core",
        "ansys.mechanical.core Documentation",
        author,
        "ansys.mechanical.core",
        "Pythonic interface to Mechanical using gRPC",
        "Engineering Software",
    ),
]


# -- Options for Epub output -------------------------------------------------

# Bibliographic Dublin Core info.
epub_title = project

# The unique identifier of the text. This can be a ISBN number
# or the project homepage.
#
# epub_identifier = ''

# A unique identification for the text.
#
# epub_uid = ''

# A list of files that should not be packed into the epub file.
epub_exclude_files = ["search.html"]

# -- Linkcheck config --------------------------------------------------------

linkcheck_ignore = [
    "https://github.com/ansys/pymechanical/pkgs/container/.*",
    "gallery_examples/embedding_n_remote/embedding_remote.html",
    "https://ansyshelp.ansys.com/*",
    "https://ansysaccount.b2clogin.com/*",
    "https://answers.microsoft.com/en-us/windows/forum/all/*",
    "https://download.ansys.com/*",
    "https://support.ansys.com/*",
    "https://discuss.ansys.com/*",
    "../api/*",  # Remove this after release 0.10.12
    "path.html",
]

linkcheck_anchors = False

# If we are on a release, we have to ignore the "release" URLs, since it is not
# available until the release is published.
switcher_version = get_version_match(version)
if switcher_version != "dev":
    linkcheck_ignore.append(
        f"https://github.com/ansys/pymechanical/releases/tag/v{pymechanical.__version__}"
    )
