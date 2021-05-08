# Import vispupu objects
from .regview import *  

# Capture the original matplotlib rcParams
import matplotlib as mpl
_orig_rc_params = mpl.rcParams.copy()

# Define the vispupu version
__version__ = "0.0.1"