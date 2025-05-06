import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, CheckButtons
from scipy.signal import butter, filtfilt

def generate_noise(noise_mean, noise_cov, t):
    return np.random.normal(noise_mean, np.sqrt(noise_cov), len(t))

def harmonic(amplitude, frequency, phase):
    return amplitude * np.sin(2 * np.pi * frequency * t + phase)

def harmonic_with_noise(amplitude, frequency, phase, noise):
    y = harmonic(amplitude, frequency, phase)
    return y + noise

def butter_filter(signal, cutoff_freq, fs):
    b, a = butter(N=4, Wn=cutoff_freq / (0.5 * fs), btype='low')
    return filtfilt(b, a, signal)

# Оновлення параметрів
def update():
    show_noise = cb_noise.get_status()[0]
    show_filtered = cb_filter.get_status()[0]

    y_no_noise = harmonic(s_amp.val, s_freq.val, s_phase.val)
    line_no_noise.set_ydata(y_no_noise)

    y_with_noise = harmonic_with_noise(s_amp.val, s_freq.val, s_phase.val, noise)
    line_with_noise.set_ydata(y_with_noise)
    line_with_noise.set_visible(show_noise)

    y_filtered = butter_filter(y_with_noise, s_cutoff.val, s_fs.val)
    filtered_line.set_ydata(y_filtered)
    filtered_line.set_visible(show_filtered)

    fig.canvas.draw_idle()

# Оновлення шуму при зміні параметрів шуму
def update_noise():
    global noise
    noise = generate_noise(s_nmean.val, s_ncov.val, t)
    update()

def reset(event):
    for slider in sliders:
        slider.reset()
    if cb_noise.get_status()[0]:  # якщо увімкнений, вимкнути
        cb_noise.set_active(0)
    if cb_filter.get_status()[0]:  # якщо увімкнений, вимкнути
        cb_filter.set_active(0)  
    update()

# Значення параметрів при ініціалізації
init_amplitude = 1.0
init_frequency = 1.0
init_phase = 0.0
init_noise_mean = 0.0
init_noise_cov = 0.1
init_cutoff = 2.0
init_fs = 100

# Часовий діапазон
t = np.linspace(0, 10, 1000)
noise = generate_noise(init_noise_mean, init_noise_cov, t)

# Криві
y_no_noise = harmonic(init_amplitude, init_frequency, init_phase)
y_with_noise = harmonic_with_noise(init_amplitude, init_frequency, init_phase, noise)
y_filtered = butter_filter(y_with_noise, init_cutoff, init_fs)

# Графік
fig, ax = plt.subplots(figsize=(12, 6))
plt.subplots_adjust(left=0.2, bottom=0.50)
ax.set_ylim(-2, 2)
line_with_noise, = ax.plot(t, y_with_noise, color='orange')  # Крива з шумом
line_no_noise, = ax.plot(t, y_no_noise)  # Крива без шуму
filtered_line, = ax.plot(t, y_filtered, color='red') # Крива з фільтром
ax.set_title("Функція гармоніки з накладеним шумом і фільтром")
ax.legend(["Шум", "Гармонічна крива", "Фільтр"], loc='upper right')
line_with_noise.set_visible(False)
filtered_line.set_visible(False)

# Слайдери
s_amp = Slider(plt.axes([0.2, 0.40, 0.65, 0.03]), 'Амплітуда', 0.0, 2.0, valinit=init_amplitude)
s_freq = Slider(plt.axes([0.2, 0.35, 0.65, 0.03]), 'Частота', 0.0, 5.0, valinit=init_frequency)
s_phase = Slider(plt.axes([0.2, 0.3, 0.65, 0.03]), 'Фаза', 0.0, 2 * np.pi, valinit=init_phase)
s_nmean = Slider(plt.axes([0.2, 0.25, 0.65, 0.03]), 'Середнє Шуму', -1.0, 1.0, valinit=init_noise_mean)
s_ncov = Slider(plt.axes([0.2, 0.2, 0.65, 0.03]), 'Дисперсія Шуму', 0.0, 1.0, valinit=init_noise_cov)
s_cutoff = Slider(plt.axes([0.2, 0.15, 0.65, 0.03]), 'Частота зрізу', 0.1, 10.0, valinit=init_cutoff)
s_fs = Slider(plt.axes([0.2, 0.1, 0.65, 0.03]), 'Частота дискретизації', 25.0, 200.0, valinit=init_fs)

sliders = [s_amp, s_freq, s_phase, s_nmean, s_ncov, s_cutoff, s_fs]  # масив слайдерів

# Чекбокс шуму/фільтру
cb_noise = CheckButtons(plt.axes([0.15, 0.03, 0.15, 0.04]), ['Показати Шум'], [False])
cb_filter = CheckButtons(plt.axes([0.45, 0.03, 0.2, 0.04]), ['Показати Фільтр'], [False])

# Кнопка Reset
button = Button(plt.axes([0.8, 0.03, 0.1, 0.04]), 'Скинути')
button.on_clicked(reset)

# Оновлення при взаємодії
for slider in [s_amp, s_freq, s_phase, s_cutoff, s_fs]:
    slider.on_changed(lambda val: update())
s_nmean.on_changed(lambda val: update_noise())
s_ncov.on_changed(lambda val: update_noise())
cb_noise.on_clicked(lambda val: update())
cb_filter.on_clicked(lambda val: update())

plt.show()