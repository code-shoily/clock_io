import pytz
from django import forms
from django.utils.timezone import now, datetime
from psycopg2.extras import DateTimeTZRange

from .range_helpers import to_object

from .models import Event


class EventForm(forms.ModelForm):
    date = forms.DateField()
    time_from = forms.TimeField()
    time_to = forms.TimeField(required=False)
    remarks = forms.CharField(widget=forms.TextInput(), required=False)

    def save(self, commit=True, *args, **kwargs):
        event = super().save(commit=False)

        date = self.cleaned_data.get('date')
        time_from = self.cleaned_data.get('time_from')
        time_to = self.cleaned_data.get('time_to')

        event.time_range = DateTimeTZRange(
            lower=to_object(date, time_from),
            upper=to_object(date, time_to) if time_to else None
        )

        if commit:
            event.save()

        return event

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get('date')
        time_from = cleaned_data.get('time_from')
        time_to = cleaned_data.get('time_to')
        current_time = now()

        # General error/tweaked data protection
        try:
            start_time = to_object(date, time_from)
            end_time = to_object(date, time_to) if time_to else None
        except Exception:
            raise forms.ValidationError("Invalid date/time format")

        # Throw error if open-ended range is provided for a past date
        if start_time.date() != current_time.date() and not end_time:
            raise forms.ValidationError(
                'End time must be provided if filling up past attendances')

        if end_time:
            # No future time can be set
            if start_time > now() or end_time > current_time:
                raise forms.ValidationError("Time cannot be set to a future time")

            # Invalid time-range
            if time_from >= time_to:
                raise forms.ValidationError("Invalid time range")

        return super().clean()

    class Meta:
        model = Event
        exclude = ['created_at', 'updated_at', 'user', 'time_range']
        fields = ['date', 'time_from', 'time_to', 'remarks']
