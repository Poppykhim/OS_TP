#include <windows.h>
#include <stdio.h>
#include <stdlib.h>

#define NUM_THREADS 10

DWORD Sum = 0;
CRITICAL_SECTION cs;  // For thread-safe access to Sum

/* The thread will execute in this function */
DWORD WINAPI Summation(LPVOID Param)
{
    DWORD Upper = *(DWORD*)Param;
    DWORD local_sum = 0;
    
    printf("Thread %lu started - calculating sum from 1 to %lu...\n", GetCurrentThreadId(), Upper);
    
    for (DWORD i = 1; i <= Upper; i++) {
        local_sum += i;
        Sleep(100); // Add delay in each iteration (100ms)
    }
    
    // Add to global sum safely
    EnterCriticalSection(&cs);
    Sum += local_sum;
    LeaveCriticalSection(&cs);
    
    printf("Thread %lu completed calculation. Local sum: %lu\n", GetCurrentThreadId(), local_sum);
    return 0;
}

int main(int argc, char *argv[])
{
    if (argc != 2) {
        printf("Usage: %s <number>\n", argv[0]);
        return 1;
    }

    HANDLE ThreadHandles[NUM_THREADS];
    DWORD ThreadIds[NUM_THREADS];
    DWORD Param = (DWORD)atoi(argv[1]);
    
    InitializeCriticalSection(&cs);

    printf("Main: Creating %d threads to calculate sum...\n", NUM_THREADS);
    Sleep(5000);
    // Create all threads
    for (int i = 0; i < NUM_THREADS; i++) {
        // Allocate memory for each thread's parameter
        DWORD* threadParam = (DWORD*)malloc(sizeof(DWORD));
        *threadParam = Param;
      
        ThreadHandles[i] = CreateThread(
            NULL,                   /* default security attributes */
            0,                      /* default stack size */
            Summation,              /* thread function */
            threadParam,            /* parameter to thread function */
            0,                      /* default creation flags */
            &ThreadIds[i]);         /* returns the thread identifier */

        if (ThreadHandles[i] == NULL) {
            fprintf(stderr, "Error creating thread %d: %d\n", i, GetLastError());
            // Clean up already created threads
            for (int j = 0; j < i; j++) {
                CloseHandle(ThreadHandles[j]);
            }
            DeleteCriticalSection(&cs);
            return 1;
        }
        
        printf("Main: Created thread %d with ID: %lu\n", i, ThreadIds[i]);
    }

    printf("Main: Waiting for all threads to complete...\n");

    /* Wait for all threads to finish */
    WaitForMultipleObjects(NUM_THREADS, ThreadHandles, TRUE, INFINITE);

    /* Close all thread handles and free memory */
    for (int i = 0; i < NUM_THREADS; i++) {
        CloseHandle(ThreadHandles[i]);
        // Note: We can't free the parameter memory here as threads may still be using it
        // In a real application, you'd need a better way to manage this
    }

    printf("\nMain: All threads completed.\n");
    printf("Main: Final sum = %lu\n", Sum);
    printf("Main: Press Enter to exit...\n");
    getchar(); // Keep console open longer

    DeleteCriticalSection(&cs);
    return 0;
}