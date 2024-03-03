import django_filters
from .models import EbookModel

class BookFilter(django_filters.FilterSet):
	author = django_filters.CharFilter(lookup_expr="icontains")
	title = django_filters.CharFilter(lookup_expr="icontains")

	class Meta:
		model = EbookModel
		fields = ['title', 'author', 'institute']