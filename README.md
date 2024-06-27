# LITE_Gallery
# Тестовое задание

Задание желательно выполнить за максимум 3-4 вечера.

Процессинг изображений:

1. Разработать api-интерфейс для высоконагруженной загрузки изображений.

Описание:

У вас есть поток загрузки фотографий. Примерно 130 000 штук за сутки, в среднем по 4 мб.

Придумать архитектуру и реализовать минимальный функционал по обработке фотографий.

Версии фоток:

    Original
    thumb: 150x120, to_fit
    big_thumb: 700x700, to_fit
    big_1920, 1920x1080, to_fit
    d2500: 2500x2500, to_fit

to_fit - значит ресайзится по длинной стороне.

Технические ограниения:

    Python, Web API
    Можно использовать любую базу данных
    Можно использовать любой S3 сервис, но лучше иметь в виду, что будем держать свой.

Минимальный функционал:

    АПИ для загрузки с клиента. Запрос на загрузку, получение ссылки куда грузить файл.
    Использование внешнего хранилища, s3
    Использование docker-compose
    Организация процессинга
    Использовать веб сокеты для оповещения о готовности фотки.
    Покрыть тестами, чтобы все проходило(И сокеты и API)

Дополнительно, написать предложение:

    по масштабируемому процессингу - как организовать?
    как сделать надежное свое s3 хранилище?
    если будет желание, сделать минимальную веб версию для тестов

API примерное
POST /images/
REQUEST
```json
{
	filename: 'hello.jpg', // имя файла для загрузки
	project_id: 111, // проект, в который грузится фотка
}
```
RESPONSE
```json
{
   upload_link: '....',
   params: {} // Возможно параметры для POST запроса
}
```
GET /projects/{id}/images
RESPONSE
```json
{
	images: [
		{
			image_id: '',
			state: 'init', // uploaded, processing, done, error
			project_id: '',
			versions: {
				original: '',
				thumb: '',
				big_thumb: '',
				big_1920: '',
				d2500: ''
			}
		}
	]
}
```
Websockets
Когда фотка обработана, нужно получать событие по проекту. Клиент подписывается на проект, используя project_id, 
в момент, когда фотка обрабатывается, отправляется событие с обновлением статуса.
=============================================================================================

# LITE_Gallery
# Test Assignment

The assignment should ideally be completed within a maximum of 3-4 evenings.

## Image Processing:

### 1. Develop an API interface for high-load image uploading.

### Description:

You have a photo upload stream. Approximately 130,000 photos per day, averaging 4 MB each.

### Requirements:

Design the architecture and implement the minimum functionality for image processing.

### Versions of photos:

- Original
- thumb: 150x120, to_fit
- big_thumb: 700x700, to_fit
- big_1920: 1920x1080, to_fit
- d2500: 2500x2500, to_fit

to_fit - means resizing based on the longer side.

### Technical Constraints:

- Python, Web API
- Any database can be used
- Any S3 service can be used, but keep in mind we will be maintaining our own.

### Minimum Functionality:

- API for uploading from the client. A request for uploading, obtaining a link where to upload the file.
- Using external storage, S3
- Using docker-compose
- Organizing processing
- Using web sockets for notifying when a photo is ready.
- Cover with tests to ensure everything works (both sockets and API).

### Additionally, provide a proposal:

- For scalable processing - how to organize it?
- How to create a reliable own S3 storage?
- If desired, create a minimal web version for testing

### Sample API

#### POST /images/
##### REQUEST

REQUEST
```json
{
	filename: 'hello.jpg', // имя файла для загрузки
	project_id: 111, // проект, в который грузится фотка
}
```
RESPONSE
```json
{
   upload_link: '....',
   params: {} // Возможно параметры для POST запроса
}
```
GET /projects/{id}/images
RESPONSE
```json
{
	images: [
		{
			image_id: '',
			state: 'init', // uploaded, processing, done, error
			project_id: '',
			versions: {
				original: '',
				thumb: '',
				big_thumb: '',
				big_1920: '',
				d2500: ''
			}
		}
	]
}
```
Websockets

When a photo is processed, an event needs to be received by the project. The client subscribes to the project using
project_id, and when the photo is processed, an event is sent with the status update.
