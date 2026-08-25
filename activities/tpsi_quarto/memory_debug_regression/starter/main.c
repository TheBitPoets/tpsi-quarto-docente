#include <stdio.h>
#include <stdlib.h>

static void fill_samples(int *samples, int n) {
    /* BUG intenzionale: individua la causa con test e sanitizer. */
    for (int i = 0; i <= n; ++i) {
        samples[i] = i + 1;
    }
}

static void summarize(const int *samples, int n, long long *sum, int *min, int *max) {
    *sum = samples[0];
    *min = samples[0];
    *max = samples[0];

    /* BUG intenzionale: un caso di confine non viene incluso. */
    for (int i = 1; i < n - 1; ++i) {
        if (samples[i] < *min) {
            *min = samples[i];
        }
        if (samples[i] > *max) {
            *max = samples[i];
        }
        *sum += samples[i];
    }
}

int main(void) {
    int n = 0;
    if (scanf("%d", &n) != 1 || n < 1 || n > 1000) {
        puts("Input non valido");
        return EXIT_FAILURE;
    }

    int *samples = malloc((size_t)n * sizeof *samples);
    if (samples == NULL) {
        fputs("Memoria non disponibile\n", stderr);
        return EXIT_FAILURE;
    }

    fill_samples(samples, n);

    long long sum = 0;
    int min = 0;
    int max = 0;
    summarize(samples, n, &sum, &min, &max);

    free(samples);

    printf("Somma: %lld\n", sum);
    printf("Min: %d\n", min);
    printf("Max: %d\n", max);
    return EXIT_SUCCESS;
}
