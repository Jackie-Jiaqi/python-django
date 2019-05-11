def validate_csv_extension(value):
    import os
    from django.core.exceptions import ValidationError
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = '.csv'
    if not ext.lower() in valid_extensions:
        raise ValidationError("Unsupported File Format! Please upload a .csv file!")


def validate_json_extension(value):
    import os
    from django.core.exceptions import ValidationError
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = '.json'
    if not ext.lower() in valid_extensions:
        raise ValidationError("Unsupported File Format! Please upload a .json file!")


def validate_excel_extension(value):
    import os
    from django.core.exceptions import ValidationError
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.xlsx', '.xls']
    if not ext.lower() in valid_extensions:
        raise ValidationError("Unsupported File Format! Please upload a .xlsx or .xls file!")

