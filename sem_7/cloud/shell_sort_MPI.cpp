// this code provided by Leonid Gotsalyuk

#include <mpi.h>
#include <iostream>
#include <algorithm>
#include <time.h>
#include <ctime>

using namespace std;

int ProcNum;    // Number of available processes
int ProcRank;   // Rank of current process

void procInit(int* &arr, int &size)
{
    if (ProcRank == 0)
    {
        do
        {
            cout << "Enter size of array:" << endl;
            cin >> size;
        } while (size <= 0);
    }

    MPI_Bcast(&size, 1, MPI_INT, 0, MPI_COMM_WORLD);

    arr = new int[size];

    if (ProcRank == 0)
    {
        //srand(unsigned(time(0)));
        for (int i = 0; i < size; i++)
        {
            //arr[i] = rand();
            arr[i] = (size - i) * (size - i) + i * i - i;
        }
    }

    //  Broadcasting array to all processes.
    MPI_Bcast(arr, size, MPI_INT, 0, MPI_COMM_WORLD);
}

void printArray(int * arr, int size)
{
    if (ProcRank == 0)
    {
        for (int i = 0; i < size; i++)
            cout << arr[i] << ' ';
        cout << endl;
    }
}

void checkIfSorted(int * arr, int size)
{
    if (ProcRank == 0)
    {
        bool flag = true;
        for (int i = 0; i < size - 1; i++)
            if (arr[i] > arr[i + 1])
            {
                flag = false;
                break;
            }

        if (flag)
            cout << "Array is sorted" << endl;
        else
            cout << "Array is NOT sorted" << endl;
    }
}

void clearMemory(int * &arr)
{
    delete[] arr;
}

int func(int num)
{
    int temp = num % 2 == 0 ? num - 6789012 : num - 5678901;
    while (temp < num)
    {
        if (temp % 2 == 0)
            temp += 3;
        else
            temp += 5;
    }
    while (temp > num)
        temp -= 1;
    return temp;
}

void shell_sort(int * arr, int size, int * transfer)
{
    const int THREADS = 4;

    int find_k = 1;
    while (find_k < size)
        find_k *= THREADS;
    find_k /= THREADS;

    for (int k = find_k; k > 0; k /= THREADS)
    {
        for (int z = ProcRank; z < k; z += ProcNum)
        {
            for (int i = z + k; i < size; i += k)
            {
                for (int j = i; j >= k; j -= k)
                {
                    if (func(arr[j]) < func(arr[j - k]))
                        swap(arr[j], arr[j - k]);
                    else
                        break;
                }
            }
        }

        // Reassemble array
        if (ProcRank == 0)
        {
            for (int process = 1; process < ProcNum; process++)
            {
                MPI_Recv(transfer, size, MPI_INT, process, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
                for (int z = process; z < k; z += ProcNum)
                    for (int i = z; i < size; i += k)
                        arr[i] = transfer[i];
            }
        }
        else
        {
            MPI_Send(arr, size, MPI_INT, 0, 0, MPI_COMM_WORLD);
        }

        MPI_Bcast(arr, size, MPI_INT, 0, MPI_COMM_WORLD);
        //MPI_Barrier(MPI_COMM_WORLD);
    }
}

int main(int argc, char* argv[])
{
    int * data;
    int * temp = nullptr;
    int size;
    double start;
    double finish;
    double duration;

    MPI_Init(&argc, &argv);
    MPI_Comm_size(MPI_COMM_WORLD, &ProcNum);
    MPI_Comm_rank(MPI_COMM_WORLD, &ProcRank);

    procInit(data, size);

    if (ProcRank == 0)
        temp = new int[size];

    //printArray(data, size);

    start = MPI_Wtime();
    shell_sort(data, size, temp);
    finish = MPI_Wtime();

    duration = finish - startd
    if (ProcRank == 0)
        cout << "Executed in: " << duration << endl;

    //printArray(data, size);
    checkIfSorted(data, size);

    clearMemory(data);
    if (ProcRank == 0)
        clearMemory(temp);

    MPI_Barrier(MPI_COMM_WORLD);

    MPI_Finalize();

    //system("pause");
    return 0;
}
