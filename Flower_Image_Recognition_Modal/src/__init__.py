# makes src a Python package

# ============================================================
# __init__.py — Makes src/ a Python package
#
# WHY THIS FILE EXISTS:
# When you write "from src.config import ..." in other files,
# Python needs to know that src/ is a package (importable module)
# and not just a random folder.
# This file tells Python exactly that.
# Having it empty would also work, but we add version info
# for professionalism.
# ============================================================

__version__ = "1.0.0"
__author__  = "Flower Recognition Project"