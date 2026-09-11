from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0006_alter_usuario_sucursal'),
    ]

    operations = [
        migrations.RenameField(
            model_name='usuario',
            old_name='first_name',
            new_name='nombre',
        ),
        migrations.RenameField(
            model_name='usuario',
            old_name='last_name',
            new_name='apellido',
        ),
        migrations.AddField(
            model_name='usuario',
            name='telefono',
            field=models.CharField(max_length=20, blank=True),
        ),
        migrations.AddField(
            model_name='usuario',
            name='intentos_fallidos',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='usuario',
            name='fecha_bloqueo',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='usuario',
            name='fecha_baja',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='email',
            field=models.EmailField(max_length=150, unique=True),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='estado',
            field=models.CharField(
                choices=[
                    ('activo', 'Activo'),
                    ('inactivo', 'Inactivo'),
                ],
                default='activo',
                max_length=10,
            ),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='rol',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                to='usuario.rol',
            ),
        ),
    ]