from django.db.models import Sum
from django.shortcuts import get_object_or_404
from .models import Product, Review, Wishlist
from carrito.models import ItemCart
from users.models import Customer

# ==========================
# Lógica de Productos
# ==========================
def get_top_selling_products(limit=3):
    """
    Calcula y retorna los productos más vendidos.
    """
    top_products = (
        ItemCart.objects.values('product')
        .annotate(total_quantity=Sum('quantity'))
        .order_by('-total_quantity')[:limit]
    )
    product_ids = [item['product'] for item in top_products]
    return Product.objects.filter(id_product__in=product_ids)

# ==========================
# Reseñas
# ==========================
def add_review(product_id, customer_id, comment, rating):
    """Permite a un cliente enviar una reseña para un producto."""
    product = get_object_or_404(Product, id_product=product_id)
    customer = get_object_or_404(Customer, id_customer=customer_id)
    return Review.objects.create(
        product=product,
        customer=customer,
        comment=comment,
        rating=rating,
        approved=False
    )
def moderate_review(review_id, approved):
    """Modera una reseña, aprobándola o rechazándola."""
    review = get_object_or_404(Review, id_review=review_id)
    review.approved = approved
    review.save()
    return review


# ==========================
# Wishlist
# ==========================
def add_product_to_wishlist(customer_id, product_id):
    """Agrega un producto a la lista de deseos."""
    customer = get_object_or_404(Customer, id_customer=customer_id)
    product = get_object_or_404(Product, id_product=product_id)
    return Wishlist.objects.create(customer=customer, product=product)


def remove_product_from_wishlist(wishlist_id):
    """Elimina una entrada de la lista de deseos."""
    wishlist = get_object_or_404(Wishlist, id_wishlist=wishlist_id)
    wishlist.delete()


# ==========================
# Sistema de Recomendaciones Personalizado
# ==========================
def get_personalized_recommendations(customer=None, session_recently_viewed=None, limit=8):
    """
    Genera recomendaciones personalizadas para un usuario basándose en:
    1. Productos que ha comprado previamente (similares usando embeddings)
    2. Productos en su wishlist (similares usando embeddings)
    3. Productos vistos recientemente (similares usando embeddings)
    4. Productos populares/mejor valorados como fallback
    
    Args:
        customer: instancia de Customer (puede ser None para usuarios no autenticados)
        session_recently_viewed: lista de IDs de productos vistos en sesión
        limit: número máximo de recomendaciones a devolver
        
    Returns:
        QuerySet de productos recomendados
    """
    import os
    from django.db.models import Count, Avg, Q
    from collections import defaultdict
    
    recommended_ids = []
    score_map = defaultdict(float)
    
    # FUENTE 1: Productos comprados previamente
    if customer:
        try:
            from ordenes.models import OrderItem
            purchased_product_ids = list(
                OrderItem.objects.filter(
                    order__customer=customer,
                    order__status__in=["Pagado", "Entregado", "Cancelada"]
                ).values_list('product_id', flat=True).distinct()
            )
            
            # Buscar productos similares usando embeddings
            if purchased_product_ids:
                similar_to_purchased = _get_similar_products_batch(
                    purchased_product_ids, 
                    exclude_ids=purchased_product_ids,
                    top_k=3
                )
                for pid, score in similar_to_purchased:
                    score_map[pid] += score * 3.0  # peso alto para compras
                    
        except Exception:
            pass  # Si falla, continuar con otras fuentes
    
    # FUENTE 2: Productos en wishlist
    if customer:
        try:
            wishlist_product_ids = list(
                Wishlist.objects.filter(customer=customer).values_list('product_id', flat=True)
            )
            
            if wishlist_product_ids:
                similar_to_wishlist = _get_similar_products_batch(
                    wishlist_product_ids,
                    exclude_ids=wishlist_product_ids,
                    top_k=3
                )
                for pid, score in similar_to_wishlist:
                    score_map[pid] += score * 2.0  # peso medio-alto para wishlist
                    
        except Exception:
            pass
    
    # FUENTE 3: Productos vistos recientemente
    if session_recently_viewed:
        try:
            similar_to_viewed = _get_similar_products_batch(
                session_recently_viewed,
                exclude_ids=session_recently_viewed,
                top_k=3
            )
            for pid, score in similar_to_viewed:
                score_map[pid] += score * 1.5  # peso medio para vistos
                
        except Exception:
            pass
    
    # Ordenar por score y tomar los top N
    if score_map:
        recommended_ids = sorted(score_map.items(), key=lambda x: x[1], reverse=True)
        recommended_ids = [pid for pid, _ in recommended_ids[:limit]]
    
    # FALLBACK: Si no hay suficientes recomendaciones, agregar productos populares
    if len(recommended_ids) < limit:
        # Productos más populares (con mejor rating y más reviews)
        popular_products = Product.objects.filter(
            stock__gt=0
        ).exclude(
            id_product__in=recommended_ids
        ).annotate(
            review_count=Count('review', filter=Q(review__approved=True)),
            avg_rating=Avg('review__rating', filter=Q(review__approved=True))
        ).order_by('-review_count', '-avg_rating', '-id_product')[:limit - len(recommended_ids)]
        
        recommended_ids.extend(popular_products.values_list('id_product', flat=True))
    
    # Construir queryset preservando el orden
    if recommended_ids:
        from django.db.models import Case, When
        preserved_order = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(recommended_ids)])
        return Product.objects.filter(
            id_product__in=recommended_ids,
            stock__gt=0
        ).annotate(_order=preserved_order).order_by('_order')
    
    # Si todo falla, devolver productos recientes con stock
    return Product.objects.filter(stock__gt=0).order_by('-id_product')[:limit]


def _get_similar_products_batch(product_ids, exclude_ids=None, top_k=3):
    """
    Helper: Encuentra productos similares a una lista de productos usando embeddings.
    
    Args:
        product_ids: lista de IDs de productos de referencia
        exclude_ids: lista de IDs a excluir de resultados
        top_k: cuántos similares buscar por cada producto
        
    Returns:
        Lista de tuplas (product_id, score) ordenadas por score
    """
    import os
    from collections import defaultdict
    
    try:
        from store.management.commands.embeddings import EMBED_PATH, ID_PATH
        
        # Verificar que existen los embeddings
        if not os.path.exists(EMBED_PATH) or not os.path.exists(ID_PATH):
            return []
        
        import numpy as np
        import joblib
        from sklearn.metrics.pairwise import cosine_similarity
        
        # Cargar embeddings
        all_embeddings = np.load(EMBED_PATH)
        all_product_ids = joblib.load(ID_PATH)
        
        # Crear mapeo de id a índice
        id_to_idx = {pid: idx for idx, pid in enumerate(all_product_ids)}
        
        # Obtener embeddings de productos de referencia
        ref_indices = [id_to_idx[pid] for pid in product_ids if pid in id_to_idx]
        if not ref_indices:
            return []
        
        ref_embeddings = all_embeddings[ref_indices]
        
        # Calcular similitudes
        similarities = cosine_similarity(ref_embeddings, all_embeddings)
        
        # Agregar scores por producto
        score_map = defaultdict(float)
        exclude_set = set(exclude_ids) if exclude_ids else set()
        exclude_set.update(product_ids)  # también excluir los productos de referencia
        
        for sim_row in similarities:
            # Obtener top_k más similares
            top_indices = np.argsort(-sim_row)[:top_k + len(exclude_set)]
            
            for idx in top_indices:
                pid = all_product_ids[idx]
                if pid not in exclude_set:
                    score_map[pid] += sim_row[idx]
        
        # Retornar ordenado por score
        results = sorted(score_map.items(), key=lambda x: x[1], reverse=True)
        return results[:top_k * len(product_ids)]
        
    except Exception:
        return []