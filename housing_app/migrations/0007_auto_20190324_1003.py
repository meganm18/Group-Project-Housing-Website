# Generated by Django 2.1.7 on 2019-03-24 14:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('housing_app', '0006_profile_avatar'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avatar', models.ImageField(default='static/images/blank_profile.png', max_length=500, upload_to='')),
                ('bio', models.TextField(blank=True, max_length=500)),
            ],
        ),
        migrations.RemoveField(
            model_name='profile',
            name='favorites',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='user',
        ),
        migrations.AddField(
            model_name='apartment',
            name='bathrooms',
            field=models.CharField(default='--', max_length=100),
        ),
        migrations.AddField(
            model_name='apartment',
            name='distance',
            field=models.CharField(default='--', max_length=100),
        ),
        migrations.AddField(
            model_name='apartment',
            name='number',
            field=models.CharField(default='--', max_length=100),
        ),
        migrations.AlterField(
            model_name='apartment',
            name='bedrooms',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='apartment',
            name='company',
            field=models.CharField(max_length=150),
        ),
        migrations.AlterField(
            model_name='apartment',
            name='name',
            field=models.CharField(max_length=150),
        ),
        migrations.AlterField(
            model_name='apartment',
            name='price',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='apartment',
            name='size',
            field=models.CharField(max_length=100),
        ),
        migrations.DeleteModel(
            name='Profile',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='compare',
            field=models.ManyToManyField(blank=True, related_name='compare', to='housing_app.Apartment'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='favorites',
            field=models.ManyToManyField(blank=True, related_name='favorites', to='housing_app.Apartment'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]