# run.py

from app import create_app
from flask import render_template

# Create Flask app instance from factory
app = create_app()



if __name__ == '__main__':
    app.run(debug=True)
