## Гайд по настройке ETL-процесса на основе nifi-2.2.0

1. Поместите драйвер в папку lib директории nifi
2. Запустите nifi `./bin/nifi.sh start`
3. Используйте команду `./bin/nifi.sh set-single-user-credentials <username> <password>`, чтобы изменить логин и пароль для входа
4. Перезапустите nifi `./bin/nifi.sh restart`
5. Перейдите по адресу `localhost:8443/nifi`
6. Постройте схему процессов (см. папку `nifi settings`)
7. Выставьте настройки всех процессов и сервисов согласно картинкам в папке `nifi settings`
8. Запустите процессы (ПКМ - Run)

## Настройка сервисов

Процессорам ConvertRecord и PutDatabaseRecord необходимо добавить сервисы

- Во вкладке `Properties` процессора `ConvertRecord` в столбце `value`
необходимо нажать на три точки -> `Create new service`.

- Во вкладке `Properties` процессора `PutDatabaseRecord` в строке
`Record Reader` нужно выбрать уже существующий сервис, который создавался для процессора
`ConvertRecord`.

- Для настройки сервисов необходимо нажать на три точки -> `Go to services`

- Настройки выставлять в соответствии с картинками в папке `nifi settings`

## Процессоры
### GetFile

- `Input Directory` - абсолютный путь к папке, в которую сохраняет свои файлы генератор
- `File Filter` - фильтр файлов. Оставить по умолчанию. Если по умолчанию стоит пустая строка, исправить в соответствии с картинкой в папке `nifi settings`

### ConvertRecord

- `Record Reader`, `Record Writer` - про создание сервисов написано выше

### SplitJson

- `JsonPath Expression` - ставим звёздочку

### PutDatabaseRecord

- `Record Reader`, `Database Connection Pulling Service` - про создание сервисов написано выше
- `Database Type` - в нашем случае `PostgreSQL`
- `Statement type` - в соответствии с заданием - `INSERT`
- `Shema name`, `Table name` - схема и таблица, в которую будут добавляться записи

## Сервис DBCPConnectionPool

- `Database connection URL` - jdbc:postgresql://localhost:`ваш порт`/`ваша база данных`
- `Database driver class name` - org.postgresql.Driver
- `Database user`, `Database password` - пользователь БД и его пароль (лучше ставить пользователей по умолчанию, т.е. `postgres`)