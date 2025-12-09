from pydantic import BaseModel, EmailStr

from helpers.users.FakeUser import FakeUser, FakeUserFactory


class UserSchema(BaseModel):
    """
    Модель данных пользователя
    """
    id: str
    email: EmailStr
    first_name: str
    last_name: str
    middle_name: str
    phone_number: str


class CreateUserRequestSchema(BaseModel):
    """
    Модель запроса нп создание пользователя
    """
    email: EmailStr
    first_name: str
    last_name: str
    middle_name: str
    phone_number: str


class CreateUserResponseSchema(BaseModel):
    """
    Модель ответа на создание пользователя
    """
    user: UserSchema


if __name__ == "__main__":
    """
    Пример использования моделей
    """
    # Пример данных для создания пользователя
    fake_user = FakeUserFactory().create()
    user_data = {
        "email": fake_user.email,
        "first_name": fake_user.firstName,
        "last_name": fake_user.lastName,
        "middle_name": fake_user.middleName,
        "phone_number": fake_user.phoneNumber
    }

    try:
        # Валидация входных данных
        create_request = CreateUserRequestSchema(**user_data)
        print("Валидация CreateUserRequestSchema прошла успешно:")
        print(create_request)

        # Имитация созданного пользователя (с id) – типа пришел ответ от сервера
        user_with_id = UserSchema(id="12345", **user_data)
        response = CreateUserResponseSchema(user=user_with_id)
        print("\nCreateUserResponseSchema успешно сформирован:")
        print(response.model_dump_json(indent=2))

    except Exception as e:
        print("Ошибка валидации:", e)
