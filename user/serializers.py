from rest_framework_gis.serializers import GeoFeatureModelSerializer
from .models import Address
# Create your views here.


class AddressSerializers(GeoFeatureModelSerializer):

    class Meta:
        model = Address
        geo_field = "location"
        fields = '__all__'
