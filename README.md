# Leaf & Root - Guía de Instalación

¡Saludos! 😊

**LEAF & ROOT** es una tienda online enfocada en productos de origen vegetal, con un enfoque en opciones veganas y vegetarianas. La plataforma busca fomentar un estilo de vida saludable, ético y sostenible, ofreciendo a los usuarios la posibilidad de identificar de forma clara si cada producto es vegano o vegetariano, y brindando información transparente sobre sus beneficios nutricionales y ambientales.

El proyecto consiste en diseñar, desarrollar y lanzar una plataforma digital de comercio electrónico, que permita a los consumidores acceder fácilmente a productos de origen vegetal, conocer sus características y comprar de manera segura.

---

## 📋 Requisitos Previos

Antes de comenzar, asegúrate de tener instalado lo siguiente:

- **Python 3.8 o superior**  
  Descarga desde el sitio oficial:  
  [https://www.python.org/downloads/](https://www.python.org/downloads/)

## 🚀 Pasos de Instalación

### 1. Descargar el Proyecto

- Ve al [repositorio de Leaf & Root en GitHub](https://github.com/lacastrilp/Leaf-Root).
- Haz clic en el botón verde **"Code"** y selecciona **"Download ZIP"**.
- Extrae el contenido.

---

### 2. Configurar el Directorio del Proyecto

- Extrae la carpeta `Leaf-Root` en una ubicación de tu preferencia (por ejemplo, en tu escritorio o carpeta de documentos).
- Navega a la carpeta extraída `Leaf-Root`.
- Copia su ruta completa:
  - **Windows**: Haz clic en la barra de direcciones del Explorador de archivos y presiona `CTRL + C`.
  - **Mac**: Haz clic en la barra de direcciones del Finder y presiona `CMD + C`.
  - **Linux**: Puedes copiar la ruta desde la barra de direcciones o usar `pwd` en la terminal.

### 3. Abrir la Línea de Comandos

Abre una terminal y navega a la carpeta del proyecto:

```bash
cd <RUTA_COPIADA>
```

Ejemplo (Windows):

```bash
cd C:\Users\usuario\Desktop\Leaf-Root
```

Ejemplo (Linux/Mac):

```bash
cd ~/Desktop/Leaf-Root
```

---

### 4. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 5. Navegar al Directorio de la Aplicación

El archivo `manage.py` se encuentra en el subdirectorio `leaf_and_root`:

```bash
cd leaf_and_root
```

### 6. Ejecutar el Servidor

```bash
python manage.py runserver
```

### 7. Abrir la Aplicación Web

Abre tu navegador y ve a:

```
http://localhost:8000/
```

Ahora deberías ver la página principal de **Leaf & Root**. 🎉

---
