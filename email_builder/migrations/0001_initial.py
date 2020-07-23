# Generated by Django 2.2.10 on 2020-07-23 15:34

from django.db import migrations, models
import django_extensions.db.fields.json
import email_builder.utils

from email_builder import utils
from django.utils.translation import ugettext, ugettext_lazy as _

email_code_choices = [(x, _(y)) for x, y in utils.get_email_code_choices()]
language_choices = [(x, _(y)) for x, y in utils.get_email_languages()]
base_raw_template_choices = [(x, _(y)) for x, y in utils.get_base_templates()]
base_html_template_choices = [(x, _(y)) for x, y in utils.get_base_html_templates()]


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EmailBuilder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(choices=email_code_choices, help_text='Select your logic between the available ones. For each key, a different context will be available in the emails created through this template', max_length=255, verbose_name='Name')),
                ('description', models.TextField(blank=True, help_text='Description of this template.', verbose_name='Description')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('subject', models.CharField(max_length=255, validators=[email_builder.utils.validate_template_syntax], verbose_name='Subject')),
                ('content', models.TextField(blank=True, default='', validators=[email_builder.utils.validate_template_syntax], verbose_name='Content')),
                ('html_content', models.TextField(blank=True, default='', validators=[email_builder.utils.validate_template_syntax], verbose_name='HTML content')),
                ('extends_template', models.CharField(blank=True, choices=base_raw_template_choices, default='', max_length=255)),
                ('extends_html_template', models.CharField(blank=True, choices=base_html_template_choices, default='', max_length=255)),
                ('body_content', models.TextField(blank=True, default='', verbose_name='Content')),
                ('body_html_content', models.TextField(blank=True, default='', verbose_name='Html Content')),
                ('libs_loaded', django_extensions.db.fields.json.JSONField(blank=True, default='[]', verbose_name='Loaded Libs')),
                ('language', models.CharField(choices=language_choices, default='en-us', help_text='Render template in alternative language', max_length=12, verbose_name='Language')),
            ],
            options={
                'verbose_name': 'Email Template',
                'verbose_name_plural': 'Email Templates',
                'unique_together': {('code', 'language')},
            },
        ),
    ]
