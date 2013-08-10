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
import sys


isFrozen = getattr(sys, "frozen", False)

############################# Directorios #############################
ROOT_DIR_PATH = os.path.dirname(sys.executable if isFrozen else __file__)
EPUBBASE_FILES_DIR_PATH = os.path.join(ROOT_DIR_PATH, "" if isFrozen else "ecreator", "files", "epubbase_files")

############################# Archivos #############################
DOCX_TO_EPUB_STYLESHEET_PATH = os.path.join(ROOT_DIR_PATH, "" if isFrozen else "ecreator", "files", "stylesheets",
                                            "docx_to_epub.xslt")
QT_SP_TRANSLATION_PATH = (os.path.join("translations", "qt_es.qm") if isFrozen else
                          os.path.join("gui", "resources", "translations", "qt_es.qm"))