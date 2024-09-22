```
└── 📁Serverless
    └── README.md                       Contiene la documentacion del proyecto
    └── 📁.github
        └── 📁workflows
            └── 📁CI_CD
                └── CI_CD.yml           Define el flujo de trabajo para la integración continua (CI) y despliegue continuo (CD) en GitHub Actions.
    └── 📁auth_service
        └── 📁app
            └── 📁auth
                └── __init__.py
                └── jwt_handler.py      Maneja la creación y decodificación de JWT.
            └── 📁routes
                └── __init__.py
                └── auth.py             Define las rutas para la autenticación (login y generación de JWT).
            └── 📁schemas
                └── __init__.py
                └── auth.py             Define los esquemas para la autenticación.
            └── 📁services
                └── __init__.py
                └── auth_service.py     Contiene la lógica para autenticar usuarios y generar JWT.
            └── 📁utils
                └── __init__.py
                └── database.py         Configura la conexión a la base de datos y el acceso a la sesión.
                └── security.py         Maneja el hashing y verificación de contraseñas.
            └── __init__.py
            └── main.py                 Configura y arranca la aplicación FastAPI para el servicio de autenticación.
            └── models.py               Define los modelos de base de datos para el servicio de autenticación.
        └── lambda_function.py          Configura el adaptador Mangum para AWS Lambda.
        └── requirements.txt            Lista las dependencias del servicio de usuarios.
    └── 📁user_service
        └── 📁app
            └── 📁auth
                └── __init__.py
                └── jwt_handler.py
            └── 📁routes
                └── __init__.py
                └── user.py
            └── 📁schemas
                └── __init__.py
                └── user.py
            └── 📁services
                └── __init__.py
                └── user_service.py
            └── 📁utils
                └── __init__.py
                └── database.py
                └── security.py
            └── __init__.py
            └── main.py
            └── models.py
        └── lambda_function.py
        └── requirements.txt
```
