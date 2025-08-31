from sqlalchemy.exc import IntegrityError
import re

class IntegrityErrorHandler:
    @staticmethod
    def parse_fk_violation_error(orig_exc) -> str:
        detail_message = str(orig_exc)
        pattern = r'DETAIL:\s+Key\s+\((\w+)\)=\((.+?)\)\s+is not present in table\s+"?(\w+)"?'
        match = re.search(pattern, detail_message)
        if match:
            field, value, table = match.groups()
            return (
                f"В таблице {table} не найдено поле {field} со "
                f"значением {value}"
            )
        return detail_message

    @classmethod
    def handle_integrity_error(cls, error: IntegrityError) -> str:
        if error.orig.sqlstate == '23503':  # Код для ForeignKeyViolation:
            return cls.parse_fk_violation_error(error.orig)

        return str(error.orig) if error.orig else str(error)
