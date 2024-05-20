from rest_framework import serializers

class HTMLSerializer(serializers.Serializer):
    html_file = serializers.FileField()
    page_size = serializers.ChoiceField(choices=['A4', 'A5'])

    def validate(self, data):
        # Perform validation for page_size
        page_size = data.get('page_size')

        # Check if page_size is one of the allowed choices
        if page_size not in ['A4', 'A5']:
            raise serializers.ValidationError("Invalid page size. Must be either 'A4' or 'A5'.")
        
        return data