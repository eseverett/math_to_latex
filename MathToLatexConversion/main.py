from lib import QT_UI

def run_UI():
    """
    This function initializes the QApplication and the UI window.

    arguments:
    None

    returns:
    None
    """

    app = QT_UI.QApplication([])
    window = QT_UI.UI()
    window.show()
    app.exec()

# This is the main entry point for the application.
def main():
    print("Starting Math to Latex Conversion Application...")
    run_UI()

if __name__ == "__main__":
    main()