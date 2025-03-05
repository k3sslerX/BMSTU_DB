## Redis

1. Установить Redis
```
brew install redis
```
2. Запустить Redis
```
brew services start redis
```
3. Остановить Redis
```
brew services stop redis
```
4. Redis - клиент

Чтобы убедиться, что Redis работает, можно запустить Redis-клиент.

```
redis-cli
```

Можно проверить работу с помощью команды `ping`.

#### Сценарий

```
k3ssler@MacBook---Roman lab5 % redis-cli
127.0.0.1:6379> ping
PONG
```
