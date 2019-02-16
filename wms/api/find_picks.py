from .models import Storage


def find_picks(order_lines):
    """
    Finds picks for order lines using Storages with least stock first.
    """
    picks = []

    for r in order_lines:
        storages = Storage.objects.filter(
            sku__id=r['sku'], stock__gt=0).order_by('stock')
        remaining_quantity = r['quantity']
        for s in storages:
            if s.stock >= remaining_quantity:
                picks.append({'id': s.id, 'quantity': remaining_quantity})
                remaining_quantity = 0
                break
            else:
                picks.append({'id': s.id, 'quantity': s.stock})
                remaining_quantity -= s.stock
            if remaining_quantity == 0:
                break
        if remaining_quantity > 0:
            return False, []

    return True, picks
