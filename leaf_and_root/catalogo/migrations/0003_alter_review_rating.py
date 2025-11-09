from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('catalogo', '0002_product_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='rating',
            field=models.DecimalField(
                max_digits=2,
                decimal_places=1,
                validators=[
                    django.core.validators.MinValueValidator(0.5),
                    django.core.validators.MaxValueValidator(5.0)
                ],
            ),
        ),
    ]
