import os
from django.core.management.base import BaseCommand, CommandError
from django.urls import reverse
from django.conf import settings
from catalogo.models import Product

# ---------- CONFIG ----------
EMBED_MODEL_NAME = 'all-MiniLM-L6-v2'

# Carpeta donde se guardarán los artefactos (dentro del proyecto)
EMBED_DIR = os.path.join(getattr(settings, "BASE_DIR", "."), 'var', 'embeddings')
EMBED_PATH = os.path.join(EMBED_DIR, 'product_embeddings.npy')
ID_PATH = os.path.join(EMBED_DIR, 'product_ids.joblib')
TOP_K = 5

_model = None  # cache para el modelo


def _get_model():
    """Carga perezosamente el modelo de sentence-transformers y lo cachea."""
    global _model
    if _model is None:
        try:
            from sentence_transformers import SentenceTransformer  # type: ignore
        except ImportError as e:
            raise CommandError(
                "Falta 'sentence-transformers'. Instálalo con: pip install sentence-transformers"
            ) from e
        _model = SentenceTransformer(EMBED_MODEL_NAME)
    return _model


# ---------- GENERADOR DE EMBEDDINGS ----------
def load_or_generate_embeddings(force: bool = False):
    """Carga o genera embeddings para todas las propiedades en la BD.

    Si force=True, vuelve a generarlos aunque existan en disco.
    """
    # Crear carpeta de embeddings si no existe
    os.makedirs(EMBED_DIR, exist_ok=True)

    if (not force) and os.path.exists(EMBED_PATH) and os.path.exists(ID_PATH):
        print("Cargando embeddings desde cache...")
        try:
            import numpy as np  # type: ignore
            import joblib  # type: ignore
        except ImportError as e:
            raise CommandError(
                "Faltan dependencias 'numpy' y/o 'joblib'. Instálalas con: pip install numpy joblib"
            ) from e
        embeddings = np.load(EMBED_PATH)
        product_ids = joblib.load(ID_PATH)
        return product_ids, embeddings

    print("Generando embeddings desde la base de datos...")

    # 1. Obtener todos los productos
    productos = Product.objects.all()
    if not productos.exists():
        raise CommandError("No hay productos en la base de datos.")

    # 2. Crear textos representativos
    corpus = []
    product_ids = []

    for prod in productos:
        text_parts = [
            prod.name or "",
            prod.category or "",
            prod.type or "",
            prod.labels or "",
            prod.nutriscore or "",
            prod.description or "",
            f"stock:{prod.stock}",
            f"precio:{prod.price}",
        ]
        texto_final = " ".join(str(x) for x in text_parts if x)
        corpus.append(texto_final)
        product_ids.append(prod.pk)  # id_product como PK

    # 3. Generar embeddings
    model = _get_model()
    try:
        import numpy as np  # type: ignore
        import joblib  # type: ignore
    except ImportError as e:
        raise CommandError(
            "Faltan dependencias 'numpy' y/o 'joblib'. Instálalas con: pip install numpy joblib"
        ) from e
    embeddings = model.encode(corpus, show_progress_bar=True, convert_to_numpy=True)

    # 4. Guardar resultados
    np.save(EMBED_PATH, embeddings)
    joblib.dump(product_ids, ID_PATH)
    print(f"Embeddings generados y guardados ({len(product_ids)} productos).")

    return product_ids, embeddings


# Cache para embeddings y IDs
_cached_embeddings = None
_cached_ids = None


def _load_embeddings_cache():
    """Carga embeddings y IDs en memoria una sola vez."""
    global _cached_embeddings, _cached_ids
    
    if _cached_embeddings is None or _cached_ids is None:
        try:
            import numpy as np  # type: ignore
            import joblib  # type: ignore
        except ImportError as e:
            raise CommandError(
                "Faltan dependencias: numpy, joblib"
            ) from e
        
        _cached_ids = joblib.load(ID_PATH)
        _cached_embeddings = np.load(EMBED_PATH)
    
    return _cached_ids, _cached_embeddings


# ---------- BÚSQUEDA ----------
def buscar_productos(query_text, top_k=TOP_K):
    """Busca productos similares a una consulta textual."""
    if not os.path.exists(EMBED_PATH) or not os.path.exists(ID_PATH):
        raise CommandError("No hay embeddings. Ejecuta con --build para generarlos.")

    try:
        import numpy as np  # type: ignore
    except ImportError as e:
        raise CommandError("Falta numpy") from e

    # Cargar modelo y embeddings en cache
    model = _get_model()
    product_ids, embeddings = _load_embeddings_cache()

    # Codificar query (rápido)
    query_vec = model.encode([query_text], convert_to_numpy=True)

    # Calcular similitud (muy rápido con NumPy)
    sims = np.dot(embeddings, query_vec.T).flatten()
    top_idx = np.argpartition(-sims, min(top_k, len(sims)-1))[:top_k]
    top_idx = top_idx[np.argsort(-sims[top_idx])]

    resultados = []
    for idx in top_idx:
        prod_id = product_ids[idx]
        try:
            prod = Product.objects.get(pk=prod_id)
            url = reverse('product_detail', kwargs={'product_id': prod.pk})
            resultados.append({
                "id": prod_id,
                "name": prod.name,
                "category": prod.category,
                "price": float(prod.price),
                "url": url,
                "score": round(float(sims[idx]), 3),
            })
        except Product.DoesNotExist:
            continue
    
    return resultados


class Command(BaseCommand):
    help = "Genera y consulta embeddings de productos (Sentence-Transformers)."

    def add_arguments(self, parser):
        parser.add_argument("--build", action="store_true", help="Genera (o recarga) los embeddings")
        parser.add_argument("--force", action="store_true", help="Fuerza regenerar, ignorando cache")
        parser.add_argument("--query", type=str, help="Texto a buscar entre productos")
        parser.add_argument("--top-k", type=int, default=TOP_K, help="Número de resultados a devolver")

    def handle(self, *args, **options):
        do_build = bool(options.get("build"))
        force = bool(options.get("force"))
        query = options.get("query")
        top_k = int(options.get("top_k") or TOP_K)

        if do_build:
            load_or_generate_embeddings(force=force)
            self.stdout.write(self.style.SUCCESS("✅ Embeddings de productos listos."))

        if query:
            if not os.path.exists(EMBED_PATH) or not os.path.exists(ID_PATH):
                self.stdout.write("No hay embeddings en cache; generando primero...")
                load_or_generate_embeddings(force=force)
            results = buscar_productos(query, top_k=top_k)
            self.stdout.write("\nResultados más cercanos:")
            for r in results:
                price_fmt = f"${r['price']:,.2f}"
                self.stdout.write(
                    f"🛒 {r['name']} | {r.get('category') or '-'} | {price_fmt} | score={r['score']} | {r['url']}"
                )

        if not do_build and not query:
            self.stdout.write(
                "Uso: python manage.py embeddings --build | --query 'texto' [--top-k 5] [--force]"
            )