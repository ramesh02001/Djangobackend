# Generated by Django 5.1.3 on 2024-11-24 15:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0008_alter_subject_faculty'),
    ]

    operations = [
        migrations.RenameField(
            model_name='subject',
            old_name='faculty',
            new_name='faculty_id',
        ),
    ]
