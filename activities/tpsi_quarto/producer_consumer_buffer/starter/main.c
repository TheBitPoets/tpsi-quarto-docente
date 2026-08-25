#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>

#define CAPACITY 4

typedef struct {
    int data[CAPACITY];
    int head;
    int tail;
    int count;
    pthread_mutex_t mutex;
    pthread_cond_t not_empty;
    pthread_cond_t not_full;
} BoundedBuffer;

typedef struct {
    BoundedBuffer *buffer;
    int n;
} ProducerArgs;

typedef struct {
    BoundedBuffer *buffer;
    int n;
    long long sum;
    int consumed;
} ConsumerArgs;

static int buffer_init(BoundedBuffer *buffer) {
    buffer->head = 0;
    buffer->tail = 0;
    buffer->count = 0;

    if (pthread_mutex_init(&buffer->mutex, NULL) != 0) {
        return -1;
    }
    if (pthread_cond_init(&buffer->not_empty, NULL) != 0) {
        pthread_mutex_destroy(&buffer->mutex);
        return -1;
    }
    if (pthread_cond_init(&buffer->not_full, NULL) != 0) {
        pthread_cond_destroy(&buffer->not_empty);
        pthread_mutex_destroy(&buffer->mutex);
        return -1;
    }
    return 0;
}

static void buffer_destroy(BoundedBuffer *buffer) {
    pthread_cond_destroy(&buffer->not_full);
    pthread_cond_destroy(&buffer->not_empty);
    pthread_mutex_destroy(&buffer->mutex);
}

static int buffer_push(BoundedBuffer *buffer, int value) {
    (void)buffer;
    (void)value;
    /* TODO: lock -> while full wait -> insert -> signal not_empty -> unlock. */
    return -1;
}

static int buffer_pop(BoundedBuffer *buffer, int *value) {
    (void)buffer;
    (void)value;
    /* TODO: lock -> while empty wait -> extract -> signal not_full -> unlock. */
    return -1;
}

static void *producer_main(void *raw) {
    ProducerArgs *args = raw;
    (void)args;
    /* TODO: produci i valori da 1 a N usando buffer_push. */
    return NULL;
}

static void *consumer_main(void *raw) {
    ConsumerArgs *args = raw;
    args->sum = 0;
    args->consumed = 0;
    /* TODO: consuma N valori usando buffer_pop e aggiorna sum/consumed. */
    return NULL;
}

int main(void) {
    int n = 0;
    if (scanf("%d", &n) != 1 || n < 1 || n > 1000) {
        puts("Input non valido");
        return EXIT_FAILURE;
    }

    BoundedBuffer buffer;
    if (buffer_init(&buffer) != 0) {
        fputs("Errore sincronizzazione\n", stderr);
        return EXIT_FAILURE;
    }

    ProducerArgs producer_args = {.buffer = &buffer, .n = n};
    ConsumerArgs consumer_args = {
        .buffer = &buffer,
        .n = n,
        .sum = 0,
        .consumed = 0,
    };

    (void)producer_args;
    (void)consumer_args;
    /* TODO: crea i due thread, attendili con pthread_join e verifica gli errori. */

    buffer_destroy(&buffer);
    puts("TODO");
    return EXIT_SUCCESS;
}
