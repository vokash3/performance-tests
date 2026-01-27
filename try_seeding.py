# Импортируем gRPC-билдер
from seeds.builder import build_grpc_seeds_builder

# Импортируем функции для сохранения и загрузки данных
from seeds.dumps import save_seeds_result, load_seeds_result

# Импортируем схемы плана сидинга (описывают структуру данных)
from seeds.schema.plan import SeedsPlan, SeedUsersPlan, SeedCardsPlan, SeedAccountsPlan


# Шаг 1. Создаём билдер, который будет генерировать данные через gRPC
builder = build_grpc_seeds_builder()

# Шаг 2. Определяем план сидинга:
# - Создать 500 пользователей
# - У каждого пользователя:
#   - 1 аккаунт с кредитной картой
#   - У каждого аккаунта:
#       - 1 физическая карта
result = builder.build(
    SeedsPlan(
        users=SeedUsersPlan(
            count=500,
            credit_card_accounts=SeedAccountsPlan(
                count=1,
                physical_cards=SeedCardsPlan(count=1)
            )
        ),
    )
)

# Шаг 3. Сохраняем результат сидинга в файл, привязанный к сценарию "test-scenario"
save_seeds_result(result=result, scenario="test-scenario")

# Шаг 4. Загружаем данные из файла и выводим в консоль
print(load_seeds_result(scenario="test-scenario"))

