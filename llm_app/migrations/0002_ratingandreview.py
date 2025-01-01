# Generated by Django 4.2.17 on 2025-01-01 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('llm_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RatingAndReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hotel_id', models.IntegerField(unique=True)),
                ('rating', models.FloatField()),
                ('review', models.TextField()),
            ],
            options={
                'verbose_name': 'Rating and Review',
                'verbose_name_plural': 'Ratings and Reviews',
                'db_table': 'property_ratingandreview',
            },
        ),
    ]