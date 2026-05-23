"""
Гіпотеза Колатца — паралельні обчислення
=========================================
Для кожного числа від 1 до 10 000 000 обчислюється кількість кроків
для виродження в 1 (послідовність Колатца).
Використовується ThreadPool для паралельного виконання.
"""

import time
from multiprocessing.pool import ThreadPool
import os

# ── Параметри ──────────────────────────────────────────────────────────────
N           = 10_000_000           # верхня межа чисел
NUM_THREADS = os.cpu_count() or 4  # кількість потоків = кількість ядер CPU
# Можна задати вручну, наприклад: NUM_THREADS = 8
# ───────────────────────────────────────────────────────────────────────────


def collatz_steps(n: int) -> int:
    """Повертає кількість кроків для виродження числа n у 1."""
    steps = 0
    while n != 1:
        if n % 2 == 0:
            n //= 2
        else:
            n = 3 * n + 1
        steps += 1
    return steps


def compute_chunk(args):
    """
    Обчислює кількість кроків для діапазону чисел [start, end).
    Повертає список кроків.
    """
    start, end = args
    return [collatz_steps(num) for num in range(start, end)]


def main():
    print(f"╔══════════════════════════════════════════════╗")
    print(f"║   Гіпотеза Колатца — паралельні обчислення   ║")
    print(f"╚══════════════════════════════════════════════╝")
    print(f"  Числа  : 1 … {N:,}")
    print(f"  Потоки : {NUM_THREADS}")
    print()

    # Розбиваємо числа від 1 до N на рівні частини для потоків
    chunk_size = N // NUM_THREADS
    chunks = []
    for i in range(NUM_THREADS):
        start = i * chunk_size + 1
        end   = (i + 1) * chunk_size + 1 if i < NUM_THREADS - 1 else N + 1
        chunks.append((start, end))

    print("  Запуск обчислень...")
    t_start = time.perf_counter()

    # ThreadPool розподіляє chunk-и між потоками
    # imap_unordered повертає результати у міру завершення — потоки не простоюють
    all_steps = []
    with ThreadPool(processes=NUM_THREADS) as pool:
        for partial in pool.imap_unordered(compute_chunk, chunks):
            all_steps.extend(partial)

    t_end   = time.perf_counter()
    elapsed = t_end - t_start

    # ── Статистика ────────────────────────────────────────────────────────
    total_steps = sum(all_steps)
    avg_steps   = total_steps / N
    max_steps   = max(all_steps)
    max_number  = all_steps.index(max_steps) + 1  # індекс + 1, бо починаємо з 1

    print()
    print(f"  ✔ Обчислення завершено!")
    print(f"  ─────────────────────────────────────────────")
    print(f"  Загальний час        : {elapsed:.4f} с")
    print(f"  Середня к-сть кроків : {avg_steps:.4f}")
    print(f"  Макс. кроків         : {max_steps}  (число {max_number:,})")
    print(f"  Мін. кроків          : {min(all_steps)}  (число 1)")
    print(f"  ─────────────────────────────────────────────")
    print()

    # Приклади для перших 10 чисел
    print("  Перші 10 чисел — кроки до 1:")
    for i in range(10):
        print(f"    {i+1:>3} → {all_steps[i]} кроків")


if __name__ == "__main__":
    main()
