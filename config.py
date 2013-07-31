# -*- coding: utf-8 -*-

# Copyright (C) 2013 Leandro
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os

############################# Directorios #############################

ROOT_DIR_PATH = os.path.abspath(os.path.dirname(__file__))
ECREATOR_DIR_PATH = os.path.join(ROOT_DIR_PATH, "ecreator")
GUI_DIR_PATH = os.path.join(ROOT_DIR_PATH, "gui")
RESOURCES_DIR_PATH = os.path.join(GUI_DIR_PATH, "resources")
FILES_DIR_PATH = os.path.join(ECREATOR_DIR_PATH, "files")
EPUBBASE_FILES_DIR_PATH = os.path.join(FILES_DIR_PATH, "epubbase_files")
STYLESHEETS_DIR_PATH = os.path.join(ROOT_DIR_PATH, FILES_DIR_PATH, "stylesheets")
TRANSLATIONS_DIR_PATH = os.path.join(RESOURCES_DIR_PATH, "translations")

############################# Archivos #############################

DOCX_TO_EPUB_STYLESHEET_PATH = os.path.join(STYLESHEETS_DIR_PATH, "docx_to_epub.xslt")