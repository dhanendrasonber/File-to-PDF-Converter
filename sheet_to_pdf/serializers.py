from rest_framework import serializers

class ExcelSerializer(serializers.Serializer):
    excel_file = serializers.FileField()
    page_size = serializers.ChoiceField(choices=['A3','A4', 'A5','A6'])

    def validate(self, data):
        # Perform validation for page_size
        page_size = data.get('page_size')

        # Check if page_size is one of the allowed choices
        if page_size not in ['A3','A4', 'A5','A6']:
            raise serializers.ValidationError("Invalid page size. Must be either 'A4' or 'A5'.")
        
        return data
    
    