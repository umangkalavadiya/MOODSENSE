# Generated by Django 4.2.3 on 2023-07-24 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0018_alter_profile_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='role',
            field=models.CharField(blank=True, choices=[('Faculty', 'Faculty'), ('Admin', 'Admin'), ('FeedbackbackOfficer', 'FeedbackbackOfficer')], default='Select your role', max_length=50, null=True),
        ),
    ]
