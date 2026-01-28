# Импортируем gRPC-билдер
from seeds.builder import build_grpc_seeds_builder

# Импортируем функции для сохранения и загрузки данных
from seeds.dumps import save_seeds_result, load_seeds_result

# Импортируем схемы плана сидинга (описывают структуру данных)
from seeds.schema.plan import SeedsPlan, SeedUsersPlan, SeedCardsPlan, SeedAccountsPlan, SeedOperationsPlan

# Шаг 1. Создаём билдер, который будет генерировать данные через gRPC
builder = build_grpc_seeds_builder()

# Шаг 2. Определяем план сидинга:
# - Создать 10 пользователей
# - У каждого пользователя:
#   - 1 аккаунт с 1 кредитной картой и 1 дебетовой картой
#   - У каждого аккаунта:
#       - 1 физическая карта (SeedCardsPlan):
#           - 1 операция пополнения (SeedOperationsPlan)
#           - 1 операция покупки (SeedOperationsPlan)
#           - 1 операция перевода (SeedOperationsPlan)
#           - 1 операция снятия наличных (SeedOperationsPlan)
#       - 1 виртуальная карта (SeedCardsPlan):
#           - 1 операция пополнения (SeedOperationsPlan)
#           - 1 операция покупки (SeedOperationsPlan)
#           - 1 операция перевода (SeedOperationsPlan)
#           - 1 операция снятия наличных (SeedOperationsPlan)
result = builder.build(
    SeedsPlan(
        users=SeedUsersPlan(
            count=10,
            debit_card_accounts=SeedAccountsPlan(
                count=1,
                physical_cards=SeedCardsPlan(count=1),
                virtual_cards=SeedCardsPlan(count=1),
                top_up_operations=SeedOperationsPlan(count=1),
                purchase_operations=SeedOperationsPlan(count=1),
                transfer_operations=SeedOperationsPlan(count=1),
                cash_withdrawal_operations=SeedOperationsPlan(count=1)
            ),
            credit_card_accounts=SeedAccountsPlan(
                count=1,
                physical_cards=SeedCardsPlan(count=1),
                virtual_cards=SeedCardsPlan(count=1),
                top_up_operations=SeedOperationsPlan(count=1),
                purchase_operations=SeedOperationsPlan(count=1),
                transfer_operations=SeedOperationsPlan(count=1),
                cash_withdrawal_operations=SeedOperationsPlan(count=1),
            )
        ),
    )
)

# Шаг 3. Сохраняем результат сидинга в файл, привязанный к сценарию
save_seeds_result(result=result, scenario="test-scenario-11-2")

# Шаг 4. Загружаем данные из файла и выводим в консоль
print(load_seeds_result(scenario="test-scenario-11-2"))
