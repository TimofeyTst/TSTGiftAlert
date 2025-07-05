from yoyo import step

__depends__ = {"0001_create_gifts_table"}

steps = [
    step(
        """
        CREATE OR REPLACE FUNCTION update_updated_at_column()
        RETURNS TRIGGER AS $$
        BEGIN
            NEW.updated_at = CURRENT_TIMESTAMP;
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;

        CREATE TRIGGER trigger_gifts_updated_at
            BEFORE UPDATE ON gifts
            FOR EACH ROW
            EXECUTE PROCEDURE update_updated_at_column();
        """,
        """
        DROP TRIGGER IF EXISTS trigger_gifts_updated_at ON gifts;
        DROP FUNCTION IF EXISTS update_updated_at_column();
        """,
    )
] 