# Как запустить код под MPI на клауде

## _Основные ингридиенты:_
* Рабочий `cpp`шний код под mpi c прошлого сема.
* Аккаунт в [Google Cloud Platform](https://cloud.google.com/).

## _Что дальше?_
После того как аккаунт создан, необходимо забабахать виртуалку.
1. Переходим на страницу с виртуальными машинами (ВМ):

    ![alt text](https://github.com/andynik/knu_labs/blob/master/term_7/cloud/photos/1.png 'COMPUTE > Compute Engine > VM instances')

2. Выбираем Create instance. Там всё оставляем по дефолту, меняем только:

  * 1 vCPU → 4 vCPU

  * Boot disk: Ubuntu 16.04 LTS

  * ✓ Allow HTTP traffic
   
3. Нажимаем Create. Виртуалка создана!

4. Теперь загружаем на Google Drive свой `cpp`шник, открываем к нему доступ по ссылке и запоминаем его `id`шник.

   ![alt text](https://github.com/andynik/knu_labs/blob/master/term_7/cloud/photos/2.jpg 'id файла')
   
5. После этого возвращаемся на страничку ВМ и нажимаем на SSH в строке с витруалкой.
   Если выдаёт **Warnings**, то
     1. Нажимаем на стрелочку справа от SSH, где выбираем  
        ![alt text](https://github.com/andynik/knu_labs/blob/master/term_7/cloud/photos/3.png)
      
     2. В появившемся окне копируем команду типа такой:
     
        `gcloud compute --project "optimum-reactor-187009" ssh --zone "us central1-a" "ubuntu-xenial-8"`
      
     3. Запускаем на своём компе Google Cloud SDK Shell (см. Примечания) и выполняем её там. Откроется консоль виртуалки.
     
        ![alt text](https://github.com/andynik/knu_labs/blob/master/term_7/cloud/photos/4.png 'PuTTY')
      
      
6. В него мы вводим команду

   `wget --no-check-certificate 'https://docs.google.com/uc export=download&id=FILEID' -O FILENAME`

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

   ![alt text](https://github.com/andynik/knu_labs/blob/master/term_7/cloud/photos/5.png 'amma parallel proger')
   
   Виден прирост в скорости при увеличении кол-ва задействованных процессов.  
   Ещё можно посмотреть, как загружается клауд:
   
   ![alt text](https://github.com/andynik/knu_labs/blob/master/term_7/cloud/photos/6.png 'клауд потеет')
   
   И отметить, что подробная конфигурация гугловсих машин, увы, скрыта:
   
   ![alt text](https://github.com/andynik/knu_labs/blob/master/term_7/cloud/photos/7.png)

N. Ах, да! И не забудьте выключить его нахрен. А то придётся заводить новый ак с 300$.
   
   ![alt text](https://github.com/andynik/knu_labs/blob/master/term_7/cloud/photos/8.jpg 'теперь можно пойти спокойно пожрать')

# Примечания

Найти Cloud SDK можно здесь. На винде дальнейшая установка стандартная. Для яблочников с macOS установка описана ниже.

# _Как установить Cloud SDK на MacOS_

(soon)
