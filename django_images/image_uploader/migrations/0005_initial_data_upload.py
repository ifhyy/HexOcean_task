from django.db import migrations


def create_initial_data(apps, schema_editor):
    AccountTier = apps.get_model('image_uploader', 'AccountTier')
    if not AccountTier.objects.exists():
        initial_data = [
            AccountTier(name='Basic',
                        thumbnail_sizes='200',
                        originally_uploaded_image=False,
                        generate_exp_links=False),
            AccountTier(name='Premium',
                        thumbnail_sizes='200,400',
                        originally_uploaded_image=True,
                        generate_exp_links=False),
            AccountTier(name='Enterprise',
                        thumbnail_sizes='200,400',
                        originally_uploaded_image=True,
                        generate_exp_links=True),
        ]
        AccountTier.objects.bulk_create(initial_data)


class Migration(migrations.Migration):
    dependencies = [
        ('image_uploader', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_initial_data),
    ]
