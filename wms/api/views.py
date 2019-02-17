from django.http import JsonResponse

from rest_framework import viewsets
from rest_framework.permissions import AllowAny
import json

from .models import SKU, Storage, Order, OrderLine
from .serializers import SKUSerializer, StorageSerializer, \
    OrderSerializer, OrderLineSerializer
from .helpers import error_response, is_ascii
from .find_picks import find_picks

# Viewsets (for Django REST framework)


class SKUViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows SKUs to be viewed or edited.
    """
    permission_classes = (AllowAny,)
    queryset = SKU.objects.get_queryset().order_by('id')
    serializer_class = SKUSerializer


class StorageViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Storages to be viewed or edited.
    """
    permission_classes = (AllowAny,)
    queryset = Storage.objects.get_queryset().order_by('id')
    serializer_class = StorageSerializer


class OrderViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Orders to be viewed or edited.
    """
    permission_classes = (AllowAny,)
    queryset = Order.objects.get_queryset().order_by('id')
    serializer_class = OrderSerializer

    def get_queryset(self):
        """
        Filter by `customer_name` against a `q` query parameter.
        """
        queryset = Order.objects.get_queryset().order_by('id')
        customer_name = self.request.query_params.get('q', None)
        if customer_name is not None:
            if not is_ascii(customer_name):
                queryset = queryset.filter(
                    customer_name__icontains=customer_name)
            else:
                queryset = queryset.filter(
                    customer_name_ascii__icontains=customer_name)
        return queryset


class OrderLineViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows OrderLines to be viewed or edited.
    """
    permission_classes = (AllowAny,)
    queryset = OrderLine.objects.get_queryset().order_by('id')
    serializer_class = OrderLineSerializer

# Fulfillment

def fulfil_order(request):
    """
    API endpoint returns instruction for fulfilling an order
    as an ordered list of picks.
    """
    try:
        # validate request method
        if request.method != 'POST':
            return error_response(
                400, 1, "This endpoint only accepts POST requests. \
                    Received a %s request." % request.method)

        # validate json format
        try:
            params = json.loads(str(request.body, encoding='utf-8'))
        except json.decoder.JSONDecodeError:
            return error_response(
                400, 2, "Request body must be valid json.")

        # validate request has required line parameter
        if 'lines' not in params:
            return error_response(
                400, 3, "Request missing required parameter: lines.")
        else:
            order_lines = params.get('lines')

        # validate lines is not empty
        if len(order_lines) == 0:
            return error_response(
                400, 4, "Parameter lines was empty. \
                    At least one order line required.")

        # validate lines is list
        if not isinstance(order_lines, list):
            return error_response(
                400, 5, "Parameter lines must be a list. %s found."
                % type(order_lines))

        # validate each line
        for line in order_lines:

            # validate line is a dict
            if not isinstance(line, dict):
                return error_response(
                    400, 6, "Parameter lines must be a list of dictionaries. \
                        %s found in list." % type(order_lines))

            for field in ['sku', 'quantity']:
                # validate line has required fields
                if field not in line:
                    return error_response(
                        400, 7, "Required field missing for a member \
                            of lines: %s" % field)

            for field in ['sku', 'quantity']:
                # check line values are integers
                try:
                    int(line[field])
                except ValueError:
                    return error_response(400, 8,
                        "Field %s must be a valid id (int). %s found."
                            % (field, type(line[field])))

            for field in ['sku', 'quantity']:
                # check line values are positive integers
                if int(line[field]) < 0:
                    return error_response(400, 9,
                        "Field %s must be a valid id (positive int). \
                            %s found." % (field, line[field]))

            # validate the referenced SKUs exist
            sku_id = int(line['sku'])
            try:
                sku = SKU.objects.get(id=sku_id)
            except SKU.DoesNotExist:
                return error_response(400, 10, 
                    "Referenced SKU with id %s does not exist" % sku_id)
    except Exception as e:
        return error_response(500, 98, "Internal server error: %s" % e)

    # Generate picks
    try:
        success, picks = find_picks(order_lines)
        if not success:
            return error_response(
                    400, 11, "Order cannot be fulfilled.")
        else:
            return JsonResponse({'success': True, 'picks': picks}, status=200)
    except Exception as e:
        return error_response(500, 99, "Internal server error: %s" % e)

    return JsonResponse(picks, status_code=200)
