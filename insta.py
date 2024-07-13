from website import create_app


app = create_app()

# Configuración básica de CORS


if __name__ == '__main__':
    app.run(debug = True)