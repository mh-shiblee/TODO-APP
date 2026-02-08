from app import create_app

app = create_app()

if __name__ == '__main__':
    print("Starting Todo App...")
    print("Open your browser: http://127.0.0.1:5000")
    print("-" * 40)
    app.run(debug=True)