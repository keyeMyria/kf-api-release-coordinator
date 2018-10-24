# Generated by Django 2.0.8 on 2018-10-18 17:43

import coordinator.api.models.release_note
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_longer_varchar'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReleaseNote',
            fields=[
                ('kf_id', models.CharField(default=coordinator.api.models.release_note.release_note_id, max_length=11, primary_key=True, serialize=False)),
                ('uuid', models.UUIDField(default=uuid.uuid4, help_text='UUID used internally')),
                ('author', models.CharField(default='admin', help_text='The user who created the note', max_length=100)),
                ('description', models.CharField(help_text='The content of the note', max_length=5000)),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Time the note was created')),
            ],
        ),
        migrations.AlterField(
            model_name='release',
            name='tags',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=50), blank=True, default=list, help_text='Tags to group the release by', size=None),
        ),
        migrations.AddField(
            model_name='releasenote',
            name='release',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notes', to='api.Release'),
        ),
        migrations.AddField(
            model_name='releasenote',
            name='study',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='notes', to='api.Study'),
        ),
    ]
