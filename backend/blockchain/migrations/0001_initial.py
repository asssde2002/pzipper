# Generated by Django 5.1.6 on 2025-02-18 11:29

import backend.storage_backends
import blockchain.models
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SmartContract',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contract_file', models.FileField(storage=backend.storage_backends.ContractStorage, upload_to=blockchain.models.contract_upload_to)),
                ('contract_name', models.TextField(db_index=True, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='SmartContractDeployment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(db_index=True, max_length=42, unique=True)),
                ('transaction_hash', models.CharField(db_index=True, max_length=66, unique=True)),
                ('deployed_at', models.DateTimeField(auto_now_add=True)),
                ('smart_contract', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blockchain.smartcontract')),
            ],
        ),
    ]
