from stroke_dashboard import create_app


app = create_app()
server = app.server


if __name__ == "__main__":
    app.run(debug=True)
