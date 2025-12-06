import serial
import time
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import mark_inset
from matplotlib.animation import FuncAnimation

SERIAL_PORT = 'COM14'
BAUD_RATE = 115200
SAMPLE_SIZE = 1024
FS_MHZ = 27.0
BIT_DEPTH = 8

C_TISSUE = 1540.0
F_SENSOR = 2.5

period_us = 1.0 / FS_MHZ
time_axis = np.linspace(0, SAMPLE_SIZE * period_us, SAMPLE_SIZE)
dist_axis = (time_axis * 1e-6 * C_TISSUE) * 100
lambda_mm = (C_TISSUE / (F_SENSOR * 1e6)) * 1000
max_depth_cm = dist_axis[-1]

try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=2)
    ser.reset_input_buffer()
    print(f"System Ready: {SERIAL_PORT}")
except Exception as e:
    print(f"Error: {e}")
    exit()

plt.style.use('dark_background')
fig, ax = plt.subplots(figsize=(13, 7))
plt.subplots_adjust(right=0.70, top=0.85, bottom=0.15) 

fig.suptitle(f"PHOTOACOUSTIC DAQ | PROTOTYPE v1", fontsize=18, fontweight='bold', color='#4ade80')
ax.set_title(f"Sensor: {F_SENSOR} MHz | Sampling: {FS_MHZ} MSPS | Window: {max_depth_cm:.2f} cm", fontsize=10, color='gray')

ax.set_xlabel("Time of Flight ($\mu s$)", fontsize=12, color='#bdc3c7')
ax.set_ylabel("Amplitude (ADC LSB)", fontsize=12, color='#bdc3c7')
ax.set_ylim(-10, 300)
ax.set_xlim(0, max(time_axis))
ax.grid(True, which='both', linestyle='--', alpha=0.2)

ax_top = ax.secondary_xaxis('top')
def time_to_dist(t): return t * 1e-6 * C_TISSUE * 100
def dist_to_time(d): return d / (C_TISSUE * 100) * 1e6
ax_top.set_functions((time_to_dist, dist_to_time))
ax_top.set_xlabel('Depth in Tissue (cm)', fontsize=11, color='#f39c12')
ax_top.tick_params(axis='x', colors='#f39c12')

line_main, = ax.plot([], [], color='#00f2ff', linewidth=1.0, label='Raw RF Data')

axins = ax.inset_axes([0.55, 0.55, 0.40, 0.40])
axins.set_facecolor('#0f172a')
axins.grid(True, linestyle=':', color='gray', alpha=0.3)

line_zoom, = axins.plot([], [], color='#ff0055', linewidth=1.5, marker='o', markersize=3, label='ROI Detail')

zoom_start = 10.0
zoom_width = 2.0
axins.set_xlim(zoom_start, zoom_start + zoom_width)
axins.set_ylim(-5, 260)
axins.set_title(f"ROI Zoom ({zoom_start}-{zoom_start+zoom_width} $\mu s$)", fontsize=9, color='#ff0055')

mark_inset(ax, axins, loc1=2, loc2=4, fc="none", ec="0.5", linestyle="--")

col_x = 0.73

fig.text(col_x, 0.88, "PHYSICS METRICS", fontsize=12, fontweight='bold', color='white')
fig.text(col_x, 0.88-0.005, "______________", fontsize=12, fontweight='bold', color='#4ade80')

props = dict(boxstyle='round', facecolor='#1e293b', alpha=0.8)
info_text = (
    f"Sound Speed: {C_TISSUE:.0f} m/s\n"
    f"Transducer:  {F_SENSOR} MHz\n"
    f"Wavelength:  {lambda_mm:.3f} mm\n"
    f"Theo. Res.:  {lambda_mm/2:.3f} mm\n"
    f"Max Depth:   {max_depth_cm:.2f} cm\n"
    f"Time Win:    {time_axis[-1]:.1f} $\mu s$"
)
fig.text(col_x, 0.70, info_text, fontsize=10, family='monospace', color='#bdc3c7', bbox=props)

fig.text(col_x, 0.60, "REAL-TIME STATUS", fontsize=12, fontweight='bold', color='white')
fig.text(col_x, 0.60-0.005, "________________", fontsize=12, fontweight='bold', color='#4ade80')

t_fps = fig.text(col_x, 0.55, "FPS:     --", fontsize=11, family='monospace', color='white')
t_rate = fig.text(col_x, 0.52, "Through: -- kB/s", fontsize=11, family='monospace', color='white')
t_check = fig.text(col_x, 0.48, "Signal:  WAITING...", fontsize=10, fontweight='bold', color='gray')

last_time = time.time()

def update(frame):
    global last_time

    if ser.in_waiting >= SAMPLE_SIZE:
        try:
            raw = ser.read(SAMPLE_SIZE)
            data = np.array(list(raw))

            line_main.set_data(time_axis, data)
            line_zoom.set_data(time_axis, data)

            curr_time = time.time()
            dt = curr_time - last_time
            fps = 1.0 / dt if dt > 0 else 0
            kbps = (SAMPLE_SIZE * fps) / 1000.0
            last_time = curr_time

            diffs = np.diff(data)
            errors = np.sum((diffs != 1) & (diffs != -255))

            t_fps.set_text(f"FPS:     {fps:4.1f}")
            t_rate.set_text(f"Through: {kbps:4.1f} kB/s")
            if errors <= 10:
                t_check.set_text("Signal:  [OK] VALID")
                t_check.set_color('#4ade80')
            else:
                t_check.set_text("Signal:  [!] NOISY / LOSS")
                t_check.set_color('#ef4444')

            ser.reset_input_buffer()
        except:
            pass

    return line_main, line_zoom

ani = FuncAnimation(fig, update, interval=1, blit=False, cache_frame_data=False)
plt.show()
ser.close()
