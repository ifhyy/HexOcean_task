from django.db import migrations


def create_initial_data(apps, schema_editor):
    AccountTier = apps.get_model('image_uploader', 'AccountTier')
    CustomUser = apps.get_model('image_uploader', 'CustomUser')
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
        admin = CustomUser.objects.create_superuser(username='admin', password='1q2w3e', account_tier=initial_data[0])
        admin.save()


class Migration(migrations.Migration):
    dependencies = [
        ('image_uploader', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_initial_data),
    ]
