import tkinter as tk
import numpy as np
import sounddevice as sd

class Speaker:
    def __init__(self):
        self.state = "off"
        self.volume = 5.0
        self.increment = 1.0
        self.beep_tones = {}
        self.sample_rate = 44100/8 # Set a standard sample rate for sound playback
        self.create_beep_tones()

        self.window = tk.Tk()
        self.window.title("Speaker Control")

        self.create_buttons()

        self.window.mainloop()

    def create_buttons(self):
        self.plus_button = tk.Button(self.window, text="Plus", command=lambda: self.adjust_volume(1))
        self.plus_button.pack(pady=10)

        self.minus_button = tk.Button(self.window, text="Minus", command=lambda: self.adjust_volume(-1))
        self.minus_button.pack(pady=10)

        self.on_off_button = tk.Button(self.window, text="On/Off", command=self.switch_on_off)
        self.on_off_button.pack(pady=10)

    def switch_on_off(self):
        if self.state == 'on':
            self.play_beep('descending_beep', self.volume)
            print('Device switched off')
            self.state = 'off'
        else:
            self.state = 'on'
            self.volume = 5
            self.play_beep('ascending_beep', self.volume)
            print('Device switched on')

    def adjust_volume(self, button_press):
        if self.state == 'on':
            if button_press == -1:
                if self.volume > 0:
                    self.volume -= self.increment
                    print(self.volume)
                else:
                    print('Minimum volume reached.')
                    self.play_beep('beep_tone_2', 1.0)
                    
            elif button_press == 1:
                if self.volume < 10:
                    self.volume += self.increment
                    print(self.volume)
                else:
                    print('Maximum volume reached.')
                    self.play_beep('beep_tone_1', 5.0)
                    
            self.create_beep_tones()

    def create_beep_tones(self):
        t = np.linspace(0, 1, int(self.sample_rate * 0.5), endpoint=False)  # 0.5 second beep
        self.beep_tones['beep_tone_1'] = np.sin(2 * np.pi * 440 * t) + np.sin(2 * np.pi * 557/2 * t) \
                                            + np.sin(2 * np.pi * 329 * t) 
        self.beep_tones['beep_tone_2'] = np.sin(2 * np.pi * 440/2 * t) + np.sin(2 * np.pi * 557/4 * t) \
                                            + np.sin(2 * np.pi * 369 * t) 
        self.beep_tones['ascending_beep'] = np.sin(2/5 * np.pi * np.linspace(400, 1100, len(t)) * t) \
                                            + np.sin(2/5 * np.pi * np.linspace(390, 1000, len(t)) * t) * 2
        self.beep_tones['descending_beep'] = np.sin(2/5 * np.pi * np.linspace(1000, 390, len(t)) * t) \
                                             + np.sin(2/4 * np.pi * np.linspace(990, 400, len(t)) * t) * 2

    def play_beep(self, beep_tone, volume):
        volume_scale = volume/10
        if beep_tone in self.beep_tones:
            sd.play(self.beep_tones[beep_tone] * volume_scale, samplerate=self.sample_rate)

# Create a speaker instance to run the GUI and play sounds
speaker = Speaker()
