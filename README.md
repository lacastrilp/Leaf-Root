# Leaf & Root - Guía de Instalación

**LEAF & ROOT** es una tienda online enfocada en productos de origen vegetal, con un enfoque en opciones veganas y vegetarianas. La plataforma busca fomentar un estilo de vida saludable, ético y sostenible, ofreciendo a los usuarios la posibilidad de identificar de forma clara si cada producto es vegano o vegetariano, y brindando información transparente sobre sus beneficios nutricionales y ambientales.

El proyecto consiste en diseñar, desarrollar y lanzar una plataforma digital de comercio electrónico, que permita a los consumidores acceder fácilmente a productos de origen vegetal, conocer sus características y comprar de manera segura.

---

## Requisitos Previos

Antes de comenzar, asegúrate de tener instalado lo siguiente:

- **Python 3.8 o superior**  
  Descarga desde el sitio oficial:  
  [https://www.python.org/downloads/](https://www.python.org/downloads/)
  
  Para verificar tu instalación, ejecuta en la terminal:
  ```bash
  python --version
  pip --version
  ```
  
  Si `python` no funciona, prueba con `python3` en sistemas Linux/Mac.

## 🚀 Pasos de Instalación

### 1. Descargar el Proyecto

- Clona el repositorio
  ```bash
  git clone https://github.com/lacastrilp/Leaf-Root
  ```

---

### 2. Ingresar a el Directorio del Proyecto

- Navega a la carpeta clonada `Leaf-Root`.

Abre una terminal y navega a la carpeta del proyecto:

```bash
cd Leaf-Root
```
---

### 3. Instalar Dependencias

```bash
pip install -r requirements.txt
```

**Nota**: Si encuentras problemas de permisos o el comando no funciona, intenta:
- En Windows/Mac: `python -m pip install -r requirements.txt`
- En Linux/Mac: `pip3 install -r requirements.txt` o `sudo pip install -r requirements.txt`

### 5. Navegar al Directorio de la Aplicación

El archivo `manage.py` se encuentra en el subdirectorio `leaf_and_root`:

```bash
cd leaf_and_root
```

### 6. Configurar la Base de Datos (Primera vez)

Si es la primera vez que ejecutas el proyecto, necesitas configurar la base de datos:

```bash
python manage.py migrate
```

### 7. Ejecutar el Servidor

```bash
python manage.py runserver
```

### 8. Abrir la Aplicación Web

Abre tu navegador y ve a:

```
http://localhost:8000/
```

Ahora deberías ver la página principal de **Leaf & Root**. 🎉

---
