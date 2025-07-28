    import sys
    import os

    # Añade la ruta a la carpeta de tu proyecto al path de Python
    # Asegúrate de que esta ruta sea la correcta para tu proyecto
    project_home = '/home/tu_nombre_de_usuario/web-interactivo' # ¡AJUSTA ESTA RUTA!
    if project_home not in sys.path:
        sys.path.insert(0, project_home)

    # Activa tu entorno virtual
    # Asegúrate de que esta ruta sea la correcta para tu entorno virtual
    activate_this = '/home/tu_nombre_de_usuario/.virtualenvs/myflaskenv/bin/activate_this.py' # ¡AJUSTA ESTA RUTA!
    with open(activate_this) as f:
        exec(f.read(), dict(__file__=activate_this))

    # Importa tu aplicación Flask desde run_server.py
    # Asegúrate de que 'app' es el nombre de tu objeto Flask en run_server.py
    from run_server import app as application # 'application' es el nombre que PythonAnywhere espera

    # Opcional: si tienes archivos estáticos que quieres servir directamente
    # desde PythonAnywhere (aunque tu Flask ya los sirve), puedes configurarlo aquí.
    # Pero para tu caso, con Flask sirviendo static_folder, no es estrictamente necesario.
    