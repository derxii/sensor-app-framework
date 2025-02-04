import sys
from frontend.main import main
import traceback


def error_handler(etype, value, tb):
    error_msg = "".join(traceback.format_exception(etype, value, tb))
    print(error_msg)
    sys.exit(1)


if __name__ == "__main__":
    sys.excepthook = error_handler
    main()
