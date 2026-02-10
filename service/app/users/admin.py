class AdminRules():
    rules: dict = {
        "rules": {
            1: "Все пользователи должны иметь уникальный логин",
            2: "Пароль должен быть минимум 6 символов",
            3: "Доступ к админ-панели только для администраторов"
        }
    }

    @classmethod
    def add_rules(cls, new_rule: str) -> dict:
        """Добавляет правило в правила админа."""

        mx = max(cls.rules["rules"].keys())
        cls.rules["rules"][mx + 1] = new_rule
        return cls.rules
    
    @classmethod
    def del_rules(cls, number_rule: int) -> dict:
        """Удаляет правило из правил админа"""

        del cls.rules["rules"][number_rule]
        return cls.rules

