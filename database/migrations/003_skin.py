"""Peewee migrations -- 003_skin.py.

Some examples (model - class or model name)::

    > Model = migrator.orm['table_name']            # Return model in current state by name
    > Model = migrator.ModelClass                   # Return model in current state by name

    > migrator.sql(sql)                             # Run custom SQL
    > migrator.python(func, *args, **kwargs)        # Run python code
    > migrator.create_model(Model)                  # Create a model (could be used as decorator)
    > migrator.remove_model(model, cascade=True)    # Remove a model
    > migrator.add_fields(model, **fields)          # Add fields to a model
    > migrator.change_fields(model, **fields)       # Change fields
    > migrator.remove_fields(model, *field_names, cascade=True)
    > migrator.rename_field(model, old_field_name, new_field_name)
    > migrator.rename_table(model, new_table_name)
    > migrator.add_index(model, *col_names, unique=False)
    > migrator.drop_index(model, *col_names)
    > migrator.add_not_null(model, *field_names)
    > migrator.drop_not_null(model, *field_names)
    > migrator.add_default(model, field_name, default)

"""

import peewee as pw
from peewee_migrate import Migrator
from decimal import ROUND_HALF_EVEN

try:
    import playhouse.postgres_ext as pw_pext
except ImportError:
    pass

SQL = pw.SQL


def migrate(migrator: Migrator, database: pw.Database, *, fake=False):
    """Write your migrations here."""

    @migrator.create_model
    class Skin(pw.Model):
        skin_id = pw.AutoField()
        created_at = pw.DateTimeField()
        updated_at = pw.DateTimeField()
        name = pw.CharField(constraints=[SQL("DEFAULT ''")], default='', max_length=255)
        type = pw.CharField(constraints=[SQL("DEFAULT 'steve'")], default='steve', max_length=255)
        hash = pw.CharField(
            constraints=[SQL("DEFAULT '9b155b4668427669ca9ed3828024531bc52fca1dcf8fbde8ccac3d9d9b53e3cf'")],
            default='9b155b4668427669ca9ed3828024531bc52fca1dcf8fbde8ccac3d9d9b53e3cf', max_length=255)
        likes = pw.IntegerField(constraints=[SQL("DEFAULT 0")], default=0)
        uploader = pw.ForeignKeyField(column_name='uploader_id', field='skin_id', model='self')
        public = pw.BooleanField(constraints=[SQL("DEFAULT True")], default=True)

        class Meta:
            table_name = "skins"


def rollback(migrator: Migrator, database: pw.Database, *, fake=False):
    """Write your rollback migrations here."""

    migrator.remove_model('skins')
