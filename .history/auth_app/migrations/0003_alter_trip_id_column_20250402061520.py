from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('auth_app', '0001_initial'),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
                -- Drop the existing primary key constraint
                ALTER TABLE auth_app_trip DROP PRIMARY KEY;
                -- Rename the column `trip_id` to `id` and preserve auto-increment property
                ALTER TABLE auth_app_trip CHANGE COLUMN `trip_id` `id` BIGINT NOT NULL AUTO_INCREMENT;
                -- Re-add the primary key constraint on the new column
                ALTER TABLE auth_app_trip ADD PRIMARY KEY (`trip_id`);
            """,
            reverse_sql="""
                -- Reverse: drop the primary key constraint on trip_id
                ALTER TABLE auth_app_trip DROP PRIMARY KEY;
                -- Rename the column `trip_id` back to `id`
                ALTER TABLE auth_app_trip CHANGE COLUMN `trip_id` `id` BIGINT NOT NULL AUTO_INCREMENT;
                -- Re-add the primary key constraint on `id`
                ALTER TABLE auth_app_trip ADD PRIMARY KEY (`id`);
            """
        ),
    ]
