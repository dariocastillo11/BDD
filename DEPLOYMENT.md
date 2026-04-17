# Instrucciones para desplegar en Replit

## Paso 1: Crear repositorio GitHub

1. Ve a https://github.com/new
2. Nombre: `quiz-bases-datos`
3. Descripción: "Quiz interactivo de Bases de Datos"
4. Elige "Public"
5. Click "Create repository"

## Paso 2: Subir archivos a GitHub

```bash
cd /home/dario/Escritorio/bddquest
git init
git add .
git commit -m "Initial commit: Quiz de Bases de Datos"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/quiz-bases-datos.git
git push -u origin main
```

## Paso 3: Desplegar en Replit

1. Ve a https://replit.com y crea cuenta (es gratis)
2. Click en "+ Create Replit"
3. Selecciona "Import from GitHub"
4. Pega: `https://github.com/TU_USUARIO/quiz-bases-datos`
5. Click "Import"
6. Espera a que cargue (1-2 minutos)
7. Click en el botón "Run" (play)
8. Abre el link público en la esquina superior derecha

¡Listo! Tu quiz estará disponible en internet para compartir con todos.

## Compartir

Tu link será algo como:
```
https://quiz-bases-datos.TU_USUARIO.repl.co
```

Comparte este link a todos tus amigos y compañeros.
