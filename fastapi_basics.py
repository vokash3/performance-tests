import uvicorn
from fastapi import FastAPI, Query, Path, Body, APIRouter, HTTPException, Depends, status
from pydantic import BaseModel

# Создание экземпляра FastAPI с указанием заголовка приложения
app = FastAPI(title="basics")

# Создание маршрутизатора с префиксом /api/v1 и тегом "Basics" для группировки эндпоинтов в документации
router = APIRouter(prefix="/api/v1", tags=["Basics"])


# Модель Pydantic для представления данных пользователя
class User(BaseModel):
    username: str  # Имя пользователя (обязательное поле)
    email: str     # Email пользователя (обязательное поле)
    age: int       # Возраст пользователя (обязательное поле)


# Модель Pydantic для ответа после создания пользователя
class UserResponse(BaseModel):
    username: str           # Имя пользователя
    email: str              # Email пользователя
    message: str            # Сообщение об успешном создании


# Зависимость: функция-фабрика, возвращающая callable для проверки минимального возраста
# Принимает параметр min_age (по умолчанию 18), возвращает внутреннюю функцию checker
def validate_min_age(min_age: int = 18):
    """
    Внешняя функция для настройки минимального возраста.
    Возвращает внутреннюю функцию, которая будет использоваться как зависимость в FastAPI.

    :param min_age: Минимальный возраст, необходимый для прохождения валидации
    :return: Функция валидации пользователя
    """
    def checker(user: User):
        """
        Внутренняя функция — непосредственно проверяет возраст пользователя.
        Вызывается при внедрении зависимости в эндпоинт.

        :param user: Объект пользователя (из тела запроса)
        :raises HTTPException: Если возраст меньше min_age
        :return: Объект пользователя, если валидация пройдена
        """
        if user.age < min_age:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"User must be at least {min_age} years old"
            )
        return user

    return checker


@router.get("/basics/{item_id}")
async def get_basics(
        name: str = Query("Alise", description="Имя пользователя"),
        item_id: int = Path(..., description="Идентификатор элемента")
):
    """
    GET-эндпоинт для получения базового сообщения.
    
    Принимает имя через query-параметр и ID элемента через путь.
    
    :param name: Имя пользователя (по умолчанию 'Alise')
    :param item_id: Уникальный идентификатор элемента (обязательный путь)
    :return: JSON с приветствием и описанием элемента
    """
    return {
        "message": f"Hello, {name}!",
        "description": f"Item number {item_id}"
    }


@router.post("/basics/users", response_model=UserResponse)
async def create_user(user: User = Body(..., description="Данные нового пользователя")):
    """
    POST-эндпоинт для создания нового пользователя.
    
    Принимает данные пользователя в формате JSON и возвращает подтверждение.

    :param user: Объект пользователя, переданный в теле запроса
    :return: Объект UserResponse с данными и сообщением об успехе
    """
    return UserResponse(
        username=user.username,
        email=user.email,
        message="User created successfully!"
    )


# Эндпоинт использует Depends для валидации возраста
@router.post("/basics/register", summary="Регистрация пользователя с проверкой возраста")
async def register_user(
        user: User = Depends(validate_min_age(min_age=21))  # внедряем зависимость
):
    """
    POST-эндпоинт для регистрации пользователя с проверкой возраста (минимум 21 год).
    
    Использует внедрённую зависимость validate_min_age с порогом 21 год.
    Если возраст меньше — выбрасывается HTTP 400.

    :param user: Объект пользователя, прошедший валидацию через Depends
    :return: Сообщение об успешной регистрации и данные пользователя
    """
    return {
        "message": f"User {user.username} registered successfully",
        "email": user.email,
        "age": user.age
    }


# Подключение маршрутизатора к основному приложению
app.include_router(router)

# Запуск приложения через Uvicorn при прямом запуске скрипта
if __name__ == "__main__":
    uvicorn.run(
        "fastapi_basics:app",      # Путь к приложению
        host="127.0.0.1",          # Хост для прослушивания
        port=8000,                 # Порт сервера
        reload=True,               # Включить авто-перезагрузку при изменении кода
        log_level="info"           # Уровень логирования
    )