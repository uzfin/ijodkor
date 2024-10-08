# Generated by Django 4.2.1 on 2024-08-12 05:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0003_customuser_phone_number_alter_comp_rassom_situation_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Artists',
            new_name='Talant',
        ),
        migrations.AlterField(
            model_name='comp_rassom',
            name='situation',
            field=models.CharField(choices=[('Active', 'Active'), ('Inactive', 'Inactive')], default='Inactive', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='comp_sher',
            name='situation',
            field=models.CharField(choices=[('Active', 'Active'), ('Inactive', 'Inactive')], default='Active', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='comp_song',
            name='situation',
            field=models.CharField(choices=[('Active', 'Active'), ('Inactive', 'Inactive')], default='Inactive', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='comp_video',
            name='situation',
            field=models.CharField(choices=[('Active', 'Active'), ('Inactive', 'Inactive')], default='Inactive', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='counter',
            name='competition',
            field=models.CharField(choices=[('Painting', 'Painting'), ('Video', 'Video'), ('Writer', 'Writer'), ('Music', 'Music')], default='Music', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='rassom',
            name='situation',
            field=models.CharField(choices=[('Active', 'Active'), ('Inactive', 'Inactive')], default='Inactive', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='sher',
            name='situation',
            field=models.CharField(choices=[('Active', 'Active'), ('Inactive', 'Inactive')], default='Active', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='song',
            name='situation',
            field=models.CharField(choices=[('Active', 'Active'), ('Inactive', 'Inactive')], default='Inactive', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='videos',
            name='situation',
            field=models.CharField(choices=[('Active', 'Active'), ('Inactive', 'Inactive')], default='Inactive', max_length=50, null=True),
        ),
    ]
