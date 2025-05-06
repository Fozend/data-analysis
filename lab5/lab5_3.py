import numpy as np
from bokeh.plotting import figure, curdoc
from bokeh.layouts import column, row
from bokeh.models import Slider, CheckboxGroup, Button, ColumnDataSource, Select

def generate_noise(mean, cov, t):
    return np.random.normal(mean, np.sqrt(cov), len(t))

def harmonic(amplitude, frequency, phase, t):
    return amplitude * np.sin(2 * np.pi * frequency * t + phase)

def harmonic_with_noise(amplitude, frequency, phase, noise, t):
    return harmonic(amplitude, frequency, phase, t) + noise

def moving_average(signal, window_size):
    filtered = np.zeros_like(signal) # створюється масив нулів розміру масиву signal
    for i in range(len(signal)):
        start = max(0, i - window_size // 2)
        end = min(len(signal), i + window_size // 2 + 1)
        filtered[i] = np.mean(signal[start:end])
    return filtered


def butter_lowpass_filter(signal, cutoff, fs, order=4):
    N = len(signal)
    # FFT - швидке перетворення Фур'є

    # обчислюємо частотну сітку для FFT
    freqs = np.fft.fftfreq(N, d=1/fs) # d=1/fs: крок дискретизації за часом, вихідний freqs - масив частот від -fs/2 до fs/2

    # перетворення Фур'є сигналу (переходить у частотну область)
    F = np.fft.fft(signal) # F - комплексні коефіцієнти, що показують амплітуди та фази кожної гармоніки
    H = np.zeros(N) # масив розміру N

    # формула амплітудної характеристики фільтра Баттерворта H(f) = 1 / 1 + (f/fc)^(2*n)
    for i in range(N):
        D = abs(freqs[i])
        H[i] = 1 / (1 + (D / cutoff)**(2 * order))

    G = F * H # Множимо спектр сигналу F на частотну характеристику H — це еквівалент фільтрації у частотній області
    filtered = np.fft.ifft(G) # Зворотне FFT — повертає сигнал назад у часову область
    return np.real(filtered)

def apply_filter(y_clean, y_noisy):
    method = filter_select.value
    if method == "Середнє ковзне":
        return moving_average(y_noisy, window_slider.value)
    elif method == "Низькочастотний Butter":
        return butter_lowpass_filter(y_noisy, cutoff_slider.value, fs_slider.value)
    
def update_signal(attr, old, new):
    y_clean = harmonic(amp_slider.value, freq_slider.value, phase_slider.value, t)
    y_noisy = harmonic_with_noise(amp_slider.value, freq_slider.value, phase_slider.value, noise, t)
    y_filtered = apply_filter(y_clean, y_noisy)
    source.data = dict(x=t, y_clean=y_clean, y_noisy=y_noisy, y_filtered=y_filtered)
    update_visibility()

def update_noise(attr, old, new):
    global noise
    noise = generate_noise(nmean_slider.value, ncov_slider.value, t)
    update_signal(attr, old, new)

def update_visibility():
    line_noise.visible = 0 in check.active
    line_filt.visible = 1 in check.active
    line_noise2.visible = 0 in check.active
    line_filt2.visible = 1 in check.active

def reset():
    amp_slider.value = init_amplitude
    freq_slider.value = init_frequency
    phase_slider.value = init_phase
    nmean_slider.value = init_noise_mean
    ncov_slider.value = init_noise_cov
    fs_slider.value = init_fs
    window_slider.value = init_window
    check.active = []
    filter_select.value = "Середнє ковзне"

# Початкові значення
init_amplitude = 1.0
init_frequency = 1.0
init_phase = 0.0
init_noise_mean = 0.0
init_noise_cov = 0.1
init_fs = 100
init_window = 11
init_cutoff = 5

# Часовий діапазон
t = np.linspace(0, 10, 1000)
noise = generate_noise(init_noise_mean, init_noise_cov, t)

# Слайдери 
amp_slider = Slider(start=0.0, end=2.0, value=init_amplitude, step=0.1, title="Амплітуда")
freq_slider = Slider(start=0.0, end=5.0, value=init_frequency, step=0.1, title="Частота")
phase_slider = Slider(start=0.0, end=2 * np.pi, value=init_phase, step=0.1, title="Фаза")
nmean_slider = Slider(start=-1.0, end=1.0, value=init_noise_mean, step=0.1, title="Середнє шуму")
ncov_slider = Slider(start=0.0, end=1.0, value=init_noise_cov, step=0.05, title="Дисперсія шуму")
window_slider = Slider(start=5, end=20, value=init_window, step=1, title="Розмір вікна")
fs_slider = Slider(start=25, end=200, value=init_fs, step=25, title="Частота дискретизації")
cutoff_slider = Slider(start=0.1, end=10, value=init_cutoff, step=0.1, title="Частота зрізу")

# Вибір фільтра
filter_select = Select(value="Середнє ковзне", options=["Середнє ковзне", "Низькочастотний Butter"])
filter_select.on_change('value', update_signal)

# Криві
y_noisy = harmonic_with_noise(init_amplitude, init_frequency, init_phase, noise, t)
y_clean = harmonic(init_amplitude, init_frequency, init_phase, t)
y_filtered = apply_filter(y_clean, y_noisy)
source = ColumnDataSource(data=dict(x=t, y_noisy=y_noisy, y_clean=y_clean, y_filtered=y_filtered))

# Графіки
plot = figure(height=400, width=600, title="Гармоніка з шумом і фільтром", x_axis_label='Час', y_axis_label='Амплітуда')
line_noise = plot.line('x', 'y_noisy', source=source, line_width=2, color='orange', legend_label="З шумом")
line_noise.visible = False
line_clean = plot.line('x', 'y_clean', source=source, line_width=2, color='blue', legend_label="Чиста гармоніка")
line_filt = plot.line('x', 'y_filtered', source=source, line_width=2, color='red', legend_label="Відфільтрований шум")
line_filt.visible = False

plot2 = figure(height=400, width=600, title="Шум і фільтр", x_axis_label='Час', y_axis_label='Амплітуда')
line_noise2 = plot2.line('x', 'y_noisy', source=source, line_width=2, color='orange', legend_label="З шумом")
line_noise2.visible = False
line_filt2 = plot2.line('x', 'y_filtered', source=source, line_width=2, color='red', legend_label="Відфільтрований шум")
line_filt2.visible = False

# Чекбокс шуму/фільтру
check = CheckboxGroup(labels=["Показати шум", "Показати фільтр"], active=[])

# Кнопка Reset
reset_button = Button(label="Скинути", button_type="success")
reset_button.on_click(reset)

# Оновлення при взаємодії
for par in [amp_slider, freq_slider, phase_slider, fs_slider, cutoff_slider, window_slider, filter_select]:
    par.on_change('value', update_signal)

for noise_par in [nmean_slider, ncov_slider]:
    noise_par.on_change('value', update_noise)

check.on_change('active', lambda attr, old, new: update_visibility())

layout = column(
    row(plot, plot2),
    row(amp_slider, freq_slider, phase_slider),
    row(nmean_slider, ncov_slider),
    row(window_slider, fs_slider, cutoff_slider),
    row(check, filter_select, reset_button)
)

curdoc().add_root(layout)
curdoc().title = "Інтерактивна гармоніка"