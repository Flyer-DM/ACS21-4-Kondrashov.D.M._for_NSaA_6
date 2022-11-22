Лабораторная работа "Алгоритмы асимметричного шифрования"


Алгоритм Диффи-Хеллмана:
![image](https://user-images.githubusercontent.com/113033685/203364932-31fdf0a3-2d4b-49cd-bdf0-76c7736ba4a8.png)

Основной Алгоритм:

1.При запуске клиент и сервер генерируют каждый свою пару ключей (открытй сервер генерирует случайным образом, клиент - вводит с клавиатуры, закрытый ключи оба берут из разных файлов):
![image](https://user-images.githubusercontent.com/113033685/203365063-d22286d7-4e34-428a-b631-8b20d5175f73.png)

![image](https://user-images.githubusercontent.com/113033685/203365105-9ce32685-37f5-4f17-9404-928f2fb60093.png)
![image](https://user-images.githubusercontent.com/113033685/203365114-a201304c-e745-4572-950b-900e0702d6e0.png)

2.При подключении клиента отправляет серверу свой открытый ключ:
![image](https://user-images.githubusercontent.com/113033685/203365244-f00050d7-7049-4f80-8be0-97440614f6e8.png)

3.В ответ сервер посылает клиенту свой открытый ключ (после прохождения проверки клиентского ключа на разрешённость):
![image](https://user-images.githubusercontent.com/113033685/203365305-2c957d90-cc26-48d2-9948-9742c07f4567.png)

![image](https://user-images.githubusercontent.com/113033685/203365331-79c6367f-b1cf-4395-9716-983543f6cd86.png)

Далее клиент и сервер формируют каждый свой частичный ключ на основе трёх имеющихся (для клиента - свой открытый, серверный открытый и свой закрытый; для сервера - свой открытый, клиентский открытый и свой закрытый) и обмениваются ими. После чего на их основе получается одно и то же число - полный ключ, по которому они далее могут расшифровывать входящие сообщения и шифровать исходящие:

![image](https://user-images.githubusercontent.com/113033685/203365491-fd4c25a0-7d31-4319-9b20-bd1e74d1f49f.png)

![image](https://user-images.githubusercontent.com/113033685/203365504-e2008d55-bc47-4476-aff2-faa70cf56fe7.png)

4.Когда клиент отправляет сообщение на сервер, он шифрует его:
![image](https://user-images.githubusercontent.com/113033685/203365540-86428de1-5121-4ef3-92a9-59780b1e28bd.png)
![image](https://user-images.githubusercontent.com/113033685/203365560-7c1b77fe-7b3e-4806-912b-c5f8c64f12b3.png)

5.Сервер при получении дешифрует:

![image](https://user-images.githubusercontent.com/113033685/203365654-49a8b1f6-2e86-4ce6-a4a2-9b56d59bb3ed.png)



Все разрешённые ключи хранятся в отдельном файле, по которому сервер проверяется, можно ли подключить клиента или нет:
![image](https://user-images.githubusercontent.com/113033685/203365770-e3fd42a5-7ae5-44b7-8c00-c69e430972c2.png)

Успешное подключение:

![image](https://user-images.githubusercontent.com/113033685/203365869-aa373bb5-a326-4929-8580-c8a78a18adf0.png)

Отказ в доступе:
![image](https://user-images.githubusercontent.com/113033685/203365905-13cf950a-5b7f-4cdf-a5e4-e592d251d177.png)



Шифрование происходит по одному порту (обычно 1025), а общение по указанному клиентом:

Переподключение на порт 4095:
![image](https://user-images.githubusercontent.com/113033685/203366050-8b3c5a36-6e4f-455f-9dd7-3d4dce6a53cf.png)

Неудачное переподключение на несуществующий порт:
![image](https://user-images.githubusercontent.com/113033685/203366207-69d97fe9-9709-4612-a921-71178be19eae.png)

