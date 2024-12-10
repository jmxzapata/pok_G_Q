# Instrucciones de Ejecución

Para ejecutar la aplicación, sigue estos pasos:

1. **Clonar el Repositorio**:
    Clona el repositorio en tu máquina local usando el siguiente comando:
    ```sh
    git clone https://github.com/jmxzapata/pok_G_Q.git
    ```

2. **Navegar al Directorio del Proyecto**:
    Cambia tu directorio actual al directorio del proyecto:
    ```sh
    cd pok_G_Q
    ```

3. **Configurar Variables de Entorno**:
    Crea una carpeta `.env` en la raíz del directorio del proyecto. Luego activa el entorno para instalar las dependencias.

    ```sh
    python -m venv .env
    .env\Scripts\activate (CMD)
    ```

4. **Instalar Dependencias**:
    Instala las dependencias necesarias usando el gestor de paquetes `pip`, ejecuta:
    ```sh
    pip install -r requirements.txt
    ```

5. **Ejecutar la Aplicación**:

    ```sh
    python .\run.py
    ```
    Esto iniciará la aplicación en `http://127.0.0.1:5000`.

6. **Inicio de sesión y Registro de usuario**:
    Ya en `http://127.0.0.1:5000`, puedes registrarte o iniciar sesión con un usuario ya registrado.
    Al iniciar sesión, el paso 1 corresponde a ingresar el nombre de usuario. Seguido de esto, en el paso 2, se debe ingresar la contraseña para generar y completar la prueba automática de conocimiento cero.
