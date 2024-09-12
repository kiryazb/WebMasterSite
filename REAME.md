## Создание fork, клонирование репозитария, отправка изменений на github и создание pull reqest 

Для создания fork проекта необходимо иметь экканунт github.com и быть залогиненым 

Если локально git не настроен, необходимо выполнить команды из секции "Настройка доступа к git локально" (ниже)

1. Переходим на страницу основного репозитария проекта
```url
https://github.com/vakhnin/WebMasterSite
```

2. Справа сверху нажимаем кнопку "Fork"
3. Снимаем галочку с пункта "Copy the master branch only"
4. Жмем кнопку "Create Fork"
5. Оказываемся на странице Вашего fork проекта
6. Жмем кнопку "Code", копируем https репозитария
7. Далее, локально. Клонируем репозитарий (вставляем ссылку из пункта 6)
```commandline
git clone https://github.com/vakhnin/WebMasterSite.git
```
8. Переходим в папку проекта
```commandline
cd WebMasterSite
```
9. Создаем свою ветку и переключаемся на неё (название ветки логин пользователя на github)
```commandline
git checkout -b <имя пользователя на github>
```
10. Создаем в папке tmp файл (можно пустой) <логин на github>.test
11.  Добавляем измененеия в индекс
```commandline
git add tmp/<имя пользователя на github>.test
```
12. Делаем commit (необходимо будет ввести имя пользователя на github и токен из пункта )
```commandline
git commit -m "Fork test"
```
13. На странице Pull request нажать кнопку "Compare & pull request"
```url
https://github.com/vakhnin/WebMasterSite/pulls
```
14. Нажать кноку "Create pull request"
15. Выслать из адресной строки браузера ссылку на Pull request такого вида
```url
https://github.com/kiryazb/WebMasterSite/pull/1
```


# Настройка доступа к git локально
1. Установка email пользователя git
```commandline
git config --global user.email "<email пользователя>"
```
2. Установка имени пользователя git
```commandline
git config --global user.name "<Имя ползователя>"
```
3. Переходим на страницу генерации токенов
```url
https://github.com/settings/tokens
```
4. Жмем "Generate new token" -> "Generate new token (ckassic)"
5. В разделе "Note" заполняем "WebMasterSite-token"
6. Выбираем "Expiration" -> "No expiration"
7. В секции "Select scopes" ставим галочку "repo"
8. Жмем "Generate token"
9. Копируем и сохраняем токен. Вы не сможете его увидеть, после того, как покинете страницу
