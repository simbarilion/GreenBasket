from django.core.exceptions import ValidationError


def validate_image(image):
    if image.size > 2 * 1024 * 1024:
        raise ValidationError("Максимальный размер файла — 2MB")

    if hasattr(image, "content_type") and not image.content_type.startswith("image"):
        raise ValidationError("Файл должен быть изображением")
