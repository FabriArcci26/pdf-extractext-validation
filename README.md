# pdf-extractext-validation

Microservicio FastAPI del sistema **PDF ExtractExt** que valida PDFs en memoria
antes de que ingresen al pipeline de extracción. Verifica dos reglas de negocio
del dominio compartido:

- **Formato**: el archivo debe comenzar con el magic number `%PDF-`.
- **Tamaño**: el archivo no debe exceder `MAX_PDF_SIZE_BYTES` (10 MB por default).

Las reglas de negocio no viven en este repo: se obtienen del paquete compartido
[`pdf-extractext-shared`](https://github.com/videlalauti/pdf-extractext-shared),
pinneado por tag (`v1.0.0`) en `requirements.txt`.

## Endpoints

| Método | Ruta        | Descripción |
| ------ | ----------- | ----------- |
| GET    | `/health`   | Healthcheck del servicio. |
| POST   | `/validate` | Acepta un `multipart/form-data` con el campo `file` y responde `{"valid": bool, "error": str \| null}`. |

### Ejemplo

```bash
curl -F "file=@documento.pdf" http://localhost:8000/validate
```

## Cómo correr

### Local (venv)

```bash
python -m venv .venv
pip install -r requirements-dev.txt
uvicorn main:app --host 0.0.0.0 --port 8000
```

Requiere Python 3.14 (igual que la imagen del `Dockerfile`).

### Docker

```bash
docker build -t pdf-extractext-validation .
docker run -p 8000:8000 pdf-extractext-validation
```

La imagen base pita la misma versión de Python por digest (`python:3.14-slim-bookworm@sha256:...`)
para mantener paridad dev/prod y builds reproducibles.

## Variables de entorno

Actualmente el servicio no requiere variables de entorno. El módulo
`pydantic-settings` ya está declarado como dependencia para la configuración
que se agrega en la tarea VB; cuando exista, las variables se documentarán aquí.

## Desarrollar

```bash
pip install -r requirements-dev.txt
ruff check .          # lint
pytest tests/ -v      # tests
```

El CI (`.github/workflows/ci.yml`) corre ambos en cada push y pull request.