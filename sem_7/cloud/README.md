# Как запустить код под MPI на клауде

## _Основные ингридиенты_
* Рабочий `cpp`шний код под mpi c прошлого сема.
* Аккаунт в [Google Cloud Platform](https://cloud.google.com/).

## _Создание виртуалки и запуск кода на ней_
После того как аккаунт создан, необходимо забабахать виртуалку.
1. Переходим на страницу с виртуальными машинами (ВМ):

    ![alt text](https://github.com/andynik/knu_labs/blob/master/sem_7/cloud/images/01.png 'COMPUTE > Compute Engine > VM instances')

2. Выбираем Create instance. Там всё оставляем по дефолту, меняем только:
   * 1 vCPU → 4 vCPU
   * Boot disk: Ubuntu 16.04 LTS
   * ✓ Allow HTTP traffic
   
3. Нажимаем Create. Виртуалка создана!

4. Теперь загружаем на Google Drive свой `cpp`шник, открываем к нему доступ по ссылке и запоминаем его `id`шник.

   ![alt text](https://github.com/andynik/knu_labs/blob/master/sem_7/cloud/images/02.jpg 'id файла')
   
5. После этого возвращаемся на страничку ВМ и нажимаем на SSH в строке с витруалкой.
   Если выдаёт **Warnings**, то
     1. Нажимаем на стрелочку справа от SSH, где выбираем  
        ![alt text](https://github.com/andynik/knu_labs/blob/master/sem_7/cloud/images/03.png)
      
     2. В появившемся окне копируем команду типа такой:
     
        ```
        gcloud compute --project "optimum-reactor-187009" ssh --zone "us central1-a" "ubuntu-xenial-8"
        ```
      
     3. Запускаем на своём компе Google Cloud SDK Shell (см. Примечания) и выполняем её там. Откроется консоль виртуалки.
     
        ![alt text](https://github.com/andynik/knu_labs/blob/master/sem_7/cloud/images/04.png 'PuTTY')
      
      
6. В него мы вводим команду

   ```
   wget --no-check-certificate 'https://docs.google.com/uc export=download&id=FILEID' -O FILENAME
   ```

   где вместо FILEID подставляем id из пункта 4, FILENAME – какое-нибудь слово – имя файла, как он будет сохранён на виртуалке.

7. Теперь поставим на ВМ gcc и mpi-модуль. Делается двумя командами:

   ```
   sudo apt-get install mpich
   sudo apt-get install gcc
   ```

8. Далее файл на диске надо скомпилить и запустить. Для этого вводим команды:

   ```
   mpic++ filename.cpp -o name -std=c++11  
   mpirun -np 2 ./name
   ```

   Где вместо `2` можно поставить какое-нить число от 1 до 8 – кол-во задействованных процессов.
   
9. Если ошибок доселе не было, то можно поиграться, указывая разное кол-во процессов:

   ![alt text](https://github.com/andynik/knu_labs/blob/master/sem_7/cloud/images/05.png 'amma parallel proger')
   
   Виден прирост в скорости при увеличении кол-ва задействованных процессов.  
   Ещё можно посмотреть, как загружается клауд:
   
   ![alt text](https://github.com/andynik/knu_labs/blob/master/sem_7/cloud/images/06.png 'клауд потеет')
   
   И отметить, что подробная конфигурация гугловсих машин, увы, скрыта:
   
   ![alt text](https://github.com/andynik/knu_labs/blob/master/sem_7/cloud/images/07.png)

10. Ах, да! И не забудьте выключить его нахрен. А то придётся заводить новый ак с 300$.
   
   ![alt text](https://github.com/andynik/knu_labs/blob/master/sem_7/cloud/images/08.jpg 'теперь можно пойти спокойно пожрать')

## _Создание ключа на ВМ_

После того как создали и развернули работающий код под MPI на одной ВМ, пришло время создать ещё одну. Но перед этим необходимо сделать пару вещей на текущей ВМ:

1. Нажимаем на SSH в меню виртуальных машин, в консольном окне вводим
   ```
   ssh-keygen -t rsa
   ```
   После чего вводим `passphrase`, повторяем ввод и получаем наш RSA-ключ:
   
   ![alt text](https://github.com/andynik/knu_labs/blob/master/sem_7/cloud/images/09.png)
   
2. После того как пункт 1 выполнен у нас появился файлик с ключём id_rsa.pub. Его необходимо переместить в папку authorized_keys:

   ```
   cd .ssh
   cat id_rsa.pub >> authorized_keys
   cat authorized_keys
   ```
   При этом после выполнения третьей команды в консоле отобразятся все ключи, но интересует пристутсвтие последнего из них:
   
   ![alt text](https://github.com/andynik/knu_labs/blob/master/sem_7/cloud/images/10.png)
   
Теперь можно приступать к созданию копии.

## _Создание копии виртуалки_

1. Для этого в меню выбираем пункт Snapshots

   ![alt text](https://github.com/andynik/knu_labs/blob/master/sem_7/cloud/images/11.png 'COMPUTE > Compute Engine > Snapshots')
   
   Где тыкаем на CREATE SNAPSHOT.
   
2. Тут выбираем в качестве Source disk ВМ, которую ранее создавали и нажимаем create.

   ![alt text](https://github.com/andynik/knu_labs/blob/master/sem_7/cloud/images/12.png)
   
   Процедура создания займёт какое-то время.
   
3. После этого в меню `snapshot`ов появится наш новоиспечённый. Выбираем его и в открытом окне тыкаем на CREATE INSTANCE.

   ![alt text](https://github.com/andynik/knu_labs/blob/master/sem_7/cloud/images/13.png)
   
   Попав окно конфигурации, ничего не меняем кроме кол-ва процессоров: можно выбрать любое, но рекомендуется, чтобы их число в сумме с первой ВМ **не превышало 8**.
   
После того, как настройка новой ВМ закочится, рядом с ней появится привычный символ галочки.

![alt text](https://github.com/andynik/knu_labs/blob/master/sem_7/cloud/images/14.png 'а я создал даже две копии')


# Примечания

Найти Cloud SDK можно [здесь](https://cloud.google.com/sdk/). На винде дальнейшая установка стандартная. Для яблочников с macOS установка описана ниже.

## _Как установить Cloud SDK на MacOS_

1. Открываем консоль, там вводим

   ```
   python -V
   ```

2. Должно вернуть версию Python 2.7.x. Потом пишем

   ```
   curl https://sdk.cloud.google.com | bash
   ```

3. Устанавливаем. И проверяем работоспособность gcloud строчкой

   ```
   /Users/USERNAME/Desktop/google-cloud-sdk/bin/gcloud init
   ```

4. После этого вводим команду из пункта 5-b выше. В ответ на что будет предложено установить пароль (5-значный). Делаем это.

   ![alt text](https://github.com/andynik/knu_labs/blob/master/sem_7/cloud/images/n01.png 'прикольное отображение ключа в консоли')
   
   Затем тут же будет предложено пройти авторизацию, вводим наш пароль из предыдущего пункта, вас перенаправит на страницу гугл-аккаунта, где будет запрошено разрешение на доступ к нему – разрешаем.
   
5. Будет написано, что вы залогинились [ваша почта], и предложено выбрать проект. Выберите тот, в котором создавали ВМ.

   ![alt text](https://github.com/andynik/knu_labs/blob/master/sem_7/cloud/images/n02.png 'Victory!')
   
   Конфигурацию пропускаем. Видим победную строку.  
   Консоль виртуалки при этом откроется в консоле мака (ваше имя будет подсвечено зелёным).
   
   ![alt text](https://github.com/andynik/knu_labs/blob/master/sem_7/cloud/images/n03.png 'наканецта')
   
6. Далее возвращаемся к пункту 6 из основой части гайда.
