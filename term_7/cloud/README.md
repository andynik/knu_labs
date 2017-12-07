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

   a. Нажимаем на стрелочку справа от SSH, где выбираем
   
      ![alt text](https://github.com/andynik/knu_labs/blob/master/term_7/cloud/photos/3.png)
   
   b. В появившемся окне копируем команду типа такой:
   
      `gcloud compute --project "optimum-reactor-187009" ssh --zone "us central1-a" "ubuntu-xenial-8"`
      
   c. Запускаем на своём компе Google Cloud SDK Shell (см. Примечания) и выполняем её там. Откроется консоль виртуалки.
   
      ![alt text](https://github.com/andynik/knu_labs/blob/master/term_7/cloud/photos/4.png 'PuTTY')
      
      
