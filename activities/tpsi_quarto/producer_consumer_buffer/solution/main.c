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
    if (pthread_mutex_lock(&buffer->mutex) != 0) {
        return -1;
    }

    while (buffer->count == CAPACITY) {
        if (pthread_cond_wait(&buffer->not_full, &buffer->mutex) != 0) {
            pthread_mutex_unlock(&buffer->mutex);
            return -1;
        }
    }

    buffer->data[buffer->tail] = value;
    buffer->tail = (buffer->tail + 1) % CAPACITY;
    buffer->count++;

    pthread_cond_signal(&buffer->not_empty);
    pthread_mutex_unlock(&buffer->mutex);
    return 0;
}

static int buffer_pop(BoundedBuffer *buffer, int *value) {
    if (pthread_mutex_lock(&buffer->mutex) != 0) {
        return -1;
    }

    while (buffer->count == 0) {
        if (pthread_cond_wait(&buffer->not_empty, &buffer->mutex) != 0) {
            pthread_mutex_unlock(&buffer->mutex);
            return -1;
        }
    }

    *value = buffer->data[buffer->head];
    buffer->head = (buffer->head + 1) % CAPACITY;
    buffer->count--;

    pthread_cond_signal(&buffer->not_full);
    pthread_mutex_unlock(&buffer->mutex);
    return 0;
}

static void *producer_main(void *raw) {
    ProducerArgs *args = raw;

    for (int value = 1; value <= args->n; ++value) {
        if (buffer_push(args->buffer, value) != 0) {
            return (void *)1;
        }
    }
    return NULL;
}

static void *consumer_main(void *raw) {
    ConsumerArgs *args = raw;
    args->sum = 0;
    args->consumed = 0;

    for (int i = 0; i < args->n; ++i) {
        int value = 0;
        if (buffer_pop(args->buffer, &value) != 0) {
            return (void *)1;
        }
        args->sum += value;
        args->consumed++;
    }
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
    pthread_t producer;
    pthread_t consumer;

    if (pthread_create(&producer, NULL, producer_main, &producer_args) != 0) {
        buffer_destroy(&buffer);
        return EXIT_FAILURE;
    }
    if (pthread_create(&consumer, NULL, consumer_main, &consumer_args) != 0) {
        pthread_cancel(producer);
        pthread_join(producer, NULL);
        buffer_destroy(&buffer);
        return EXIT_FAILURE;
    }

    void *producer_status = NULL;
    void *consumer_status = NULL;
    int join_producer = pthread_join(producer, &producer_status);
    int join_consumer = pthread_join(consumer, &consumer_status);
    buffer_destroy(&buffer);

    if (join_producer != 0 || join_consumer != 0 ||
        producer_status != NULL || consumer_status != NULL) {
        return EXIT_FAILURE;
    }

    printf("Somma: %lld\n", consumer_args.sum);
    printf("Prodotti: %d\n", n);
    printf("Consumati: %d\n", consumer_args.consumed);
    return EXIT_SUCCESS;
}
