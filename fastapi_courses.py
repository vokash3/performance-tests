import uvicorn
from fastapi import FastAPI, APIRouter, HTTPException, status
from pydantic import BaseModel, RootModel

app = FastAPI(title="Courses API")

courses_router = APIRouter(
    prefix="/api/v1/courses",
    tags=["courses-service"],
)


class CourseIn(BaseModel):
    """
    Модель входных данных для создания или обновления курса.

    Атрибуты:
        title (str): Название курса.
        max_score (int): Максимальный балл, который можно получить в курсе.
        min_score (int): Минимальный проходной балл.
        description (str): Описание курса.
    """
    title: str
    max_score: int
    min_score: int
    description: str


class CourseOut(CourseIn):
    """
    Модель выходных данных курса, включает идентификатор.

    Наследуется от CourseIn и добавляет поле id.

    Атрибуты:
        id (int): Уникальный идентификатор курса.
    """
    id: int


class CoursesStore(RootModel):
    """
    Хранилище курсов, реализующее базовые операции CRUD.

    Использует список объектов CourseOut в качестве корневой модели.
    Предоставляет методы для поиска, создания, обновления и удаления курсов.
    """
    root: list[CourseOut]

    def find(self, course_id: int) -> CourseOut | None:
        """
        Находит курс по его идентификатору.

        Аргументы:
            course_id (int): ID курса.

        Возвращает:
            CourseOut | None: Найденный курс или None, если не найден.
        """
        return next(
            filter(lambda course: course.id == course_id, self.root),
            None,
        )

    def create(self, course_in: CourseIn) -> CourseOut:
        """
        Создаёт новый курс с автоматически присваиваемым ID.

        Аргументы:
            course_in (CourseIn): Данные для создания курса.

        Возвращает:
            CourseOut: Созданный курс с присвоенным ID.
        """
        course = CourseOut(
            id=len(self.root) + 1,
            **course_in.model_dump(),
        )
        self.root.append(course)
        return course

    def update(self, course_id: int, course_in: CourseIn) -> CourseOut:
        """
        Обновляет существующий курс по ID.

        Аргументы:
            course_id (int): ID курса для обновления.
            course_in (CourseIn): Новые данные курса.

        Возвращает:
            CourseOut: Обновлённый курс.

        Исключения:
            StopIteration: Если курс с таким ID не найден.
        """
        index = next(
            index
            for index, course in enumerate(self.root)
            if course.id == course_id
        )

        updated = CourseOut(
            id=course_id,
            **course_in.model_dump(),
        )

        self.root[index] = updated
        return updated

    def delete(self, course_id: int) -> None:
        """
        Удаляет курс по его ID.

        Аргументы:
            course_id (int): ID курса для удаления.

        Примечание:
            Если курс не найден — ничего не происходит.
        """
        self.root = [
            course
            for course in self.root
            if course.id != course_id
        ]


# Инициализация хранилища пустым списком курсов
store = CoursesStore(root=[])


@courses_router.get("/{course_id}", response_model=CourseOut)
async def get_course(course_id: int):
    """
    Получить курс по ID.

    Параметры:
        course_id (int): Идентификатор курса.

    Возвращает:
        CourseOut: Данные курса.

    Ответы:
        200: Курс найден.
        404: Курс не найден.
    """
    if not (course := store.find(course_id)):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Course with id {course_id} not found",
        )

    return course


@courses_router.get("", response_model=list[CourseOut])
async def get_courses():
    """
    Получить список всех курсов.

    Возвращает:
        list[CourseOut]: Список всех курсов.

    Ответы:
        200: Успешное получение списка.
    """
    return store.root


@courses_router.post(
    "",
    response_model=CourseOut,
    status_code=status.HTTP_201_CREATED,
)
async def create_course(course: CourseIn):
    """
    Создать новый курс.

    Тело запроса:
        CourseIn: Данные нового курса.

    Возвращает:
        CourseOut: Созданный курс с присвоенным ID.

    Ответы:
        201: Курс успешно создан.
    """
    return store.create(course)


@courses_router.put("/{course_id}", response_model=CourseOut)
async def update_course(course_id: int, course: CourseIn):
    """
    Обновить курс по ID.

    Параметры:
        course_id (int): Идентификатор курса.

    Тело запроса:
        CourseIn: Новые данные курса.

    Возвращает:
        CourseOut: Обновлённый курс.

    Ответы:
        200: Курс успешно обновлён.
        404: Курс не найден.
    """
    if not store.find(course_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Course with id {course_id} not found",
        )

    return store.update(course_id, course)


@courses_router.delete(
    "/{course_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_course(course_id: int):
    """
    Удалить курс по ID.

    Параметры:
        course_id (int): Идентификатор курса.

    Ответы:
        204: Курс успешно удалён.
        404: Курс не найден.
    """
    if not store.find(course_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Course with id {course_id} not found",
        )

    store.delete(course_id)


# Подключение маршрутов к приложению
app.include_router(courses_router)

# Запуск приложения через Uvicorn при прямом запуске скрипта
if __name__ == "__main__":
    uvicorn.run(
        "fastapi_courses:app",  # Путь к приложению
        host="127.0.0.1",  # Хост для прослушивания
        port=8000,  # Порт сервера
        reload=True,  # Включить авто-перезагрузку при изменении кода
        log_level="info"  # Уровень логирования
    )
