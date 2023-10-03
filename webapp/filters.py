from django_filters import FilterSet, ModelChoiceFilter

from webapp.models import Response, Message


class ResponseFilter(FilterSet):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(ResponseFilter, self).__init__(*args, **kwargs)
        self.filters['message'].queryset = Message.objects.filter(messageAuthor_id=self.user.id)

    message = ModelChoiceFilter(queryset=Message.objects.all())
    class Meta:
        model = Response
        fields = ['message']
