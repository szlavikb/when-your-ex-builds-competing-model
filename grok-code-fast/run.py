"""
Entry point for the F1 News Dashboard application.
"""
from app import create_app
from config import get_config


def main():
    """Main entry point for the application."""
    config_class = get_config()
    app = create_app(config_class)

    print("Starting F1 News Dashboard...")
    print(f"Debug mode: {app.config['DEBUG']}")
    print("Access the application at: http://127.0.0.1:5000")

    app.run(
        host='127.0.0.1',
        port=5000,
        debug=app.config['DEBUG']
    )


if __name__ == '__main__':
    main()
