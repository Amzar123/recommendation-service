from src.app import create_app
from gunicorn.app.base import BaseApplication

# Create an application instance using the factory function
app = create_app()

class GunicornApp(BaseApplication):
    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super().__init__()

    def load_config(self):
        for key, value in self.options.items():
            self.cfg.set(key, value)

    def load(self):
        return self.application

if __name__ == '__main__':
    # Configure Gunicorn options
    options = {
        'bind': '127.0.0.1:8000',  # Change this to your desired host and port
        'workers': 4,  # Adjust the number of workers based on your needs
    }

    # Create and run the Gunicorn application
    GunicornApp(app, options).run()
