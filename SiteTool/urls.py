from django.urls import path
from .views import StackView, UrbanView,WikiView


urlpatterns = [
    path('stack', StackView.as_view(), name='stack'),
    path('urban', UrbanView.as_view(), name='urban'),
    path('wiki',WikiView.as_view(), name='wiki'),

]
