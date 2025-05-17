import tkinter as tk
from tkinter import messagebox
import time
import threading
import winsound  # Solo en Windows

class TemporizadorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Temporizador Postural")

        self.en_ejecucion = False
        self.detener = False
        self.pausado = False
        self.saltar = False
        self.bloque = 0
        self.estado_index = 0
        self.estados = ["Sentarse", "Caminar", "En pie"]

        self.tiempos = {
            "Sentarse": 30,
            "Caminar": 20,
            "En pie": 10
        }

        self.kilometros_totales = 0
        self.calorias_totales = 0
        self.pasos_totales = 0

        tk.Label(root, text="Duración por bloque (minutos):", font=("Helvetica", 12)).pack(pady=(10, 0))

        self.inputs = {}
        for estado in self.estados:
            frame = tk.Frame(root)
            frame.pack(pady=2)
            tk.Label(frame, text=f"{estado}:", width=15, anchor="w").pack(side="left")
            entry = tk.Entry(frame, width=5)
            entry.insert(0, str(self.tiempos[estado]))
            entry.pack(side="left")
            self.inputs[estado] = entry

        tk.Label(root, text="Velocidad al caminar (km/h):", font=("Helvetica", 12)).pack()
        self.input_velocidad = tk.Entry(root, width=5)
        self.input_velocidad.insert(0, "1.5")
        self.input_velocidad.pack(pady=(0, 10))

        self.label = tk.Label(root, text="Haz clic en 'Iniciar rutina'", font=("Helvetica", 14))
        self.label.pack(pady=10)

        self.label_estado = tk.Label(root, text="", font=("Helvetica", 12))
        self.label_estado.pack()

        self.label_bloques = tk.Label(root, text="Bloques realizados: 0", font=("Helvetica", 11))
        self.label_bloques.pack(pady=(5, 5))

        self.boton_iniciar = tk.Button(root, text="Iniciar rutina", command=self.iniciar_jornada)
        self.boton_iniciar.pack(pady=5)

        self.boton_pausar = tk.Button(root, text="Pausar", command=self.pausar_jornada, state="disabled")
        self.boton_pausar.pack()

        self.boton_continuar = tk.Button(root, text="Continuar", command=self.continuar_jornada, state="disabled")
        self.boton_continuar.pack()

        self.boton_saltar = tk.Button(root, text="Saltar bloque", command=self.saltar_bloque, state="disabled")
        self.boton_saltar.pack()

        self.boton_detener = tk.Button(root, text="Detener rutina", command=self.detener_jornada, state="disabled")
        self.boton_detener.pack(pady=(5, 10))

        self.label_resumen = tk.Label(
            root,
            text="Aquí se mostrarán tus resultados al terminar la rutina.",
            font=("Helvetica", 11),
            justify="left",
            fg="gray"
        )
        self.label_resumen.pack(pady=(10, 5))

    def iniciar_jornada(self):
        try:
            for estado in self.estados:
                minutos = int(self.inputs[estado].get())
                if minutos <= 0:
                    raise ValueError
                self.tiempos[estado] = minutos

            self.velocidad_kmh = float(self.input_velocidad.get())
            if self.velocidad_kmh <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Introduce valores válidos mayores que 0.")
            return

        self.kilometros_totales = 0
        self.calorias_totales = 0
        self.pasos_totales = 0
        self.label_resumen.config(
            text="Aquí se mostrarán tus resultados al terminar la rutina.",
            fg="gray"
        )
        self.label_bloques.config(text="Bloques realizados: 0")
        self.en_ejecucion = True
        self.detener = False
        self.pausado = False
        self.saltar = False
        self.bloque = 0
        self.estado_index = 0

        self.boton_detener.config(state="normal")
        self.boton_pausar.config(state="normal")
        self.boton_saltar.config(state="normal")
        self.boton_continuar.config(state="disabled")

        t = threading.Thread(target=self.ejecutar_temporizador)
        t.start()

    def pausar_jornada(self):
        self.pausado = True
        self.boton_pausar.config(state="disabled")
        self.boton_continuar.config(state="normal")
        self.label.config(text="⏸️ Rutina en pausa")

    def continuar_jornada(self):
        self.pausado = False
        self.boton_pausar.config(state="normal")
        self.boton_continuar.config(state="disabled")

    def saltar_bloque(self):
        self.saltar = True

    def detener_jornada(self):
        self.detener = True
        self.label.config(text="⛔ Rutina detenida por el usuario.")
        self.label_estado.config(text="")
        self.boton_detener.config(state="disabled")
        self.boton_pausar.config(state="disabled")
        self.boton_continuar.config(state="disabled")
        self.boton_saltar.config(state="disabled")

        resumen = f"📊 Resumen de la rutina:\n" \
                  f"- Bloques completados: {self.bloque}\n" \
                  f"- Distancia total caminada: {self.kilometros_totales:.2f} km\n" \
                  f"- Pasos estimados: {self.pasos_totales}\n" \
                  f"- Calorías quemadas: {self.calorias_totales}"

        self.label_resumen.config(text=resumen, fg="black")
        messagebox.showinfo("Resumen de la rutina", resumen)

        

    def ejecutar_temporizador(self):
        while not self.detener:
            estado_actual = self.estados[self.estado_index]
            duracion_min = self.tiempos[estado_actual]

            emoji = {
                "Sentarse": "🪑",
                "Caminar": "👟",
                "En pie": "🦶"
            }
            colores = {
                "Sentarse": "#d0e6f7",
                "Caminar": "#d4edda",
                "En pie": "#fff3cd"
            }

            color_actual = colores.get(estado_actual, "white")
            self.label.config(bg=color_actual)
            self.label_estado.config(bg=color_actual)
            self.root.config(bg=color_actual)
            self.label_estado.config(text=f"{emoji.get(estado_actual, '')}  {estado_actual}")
            try:
                for widget in self.root.winfo_children():
                    if isinstance(widget, tk.Frame):
                        widget.configure(bg=color_actual)
            except:
                pass

            self.mostrar_alerta(estado_actual)

            if estado_actual == "Caminar":
                km = self.velocidad_kmh * (duracion_min / 60)
                pasos = int(km * 1400)
                calorias = int(km * 50)

                self.kilometros_totales += km
                self.pasos_totales += pasos
                self.calorias_totales += calorias

            for i in range(duracion_min * 60, 0, -1):
                if self.detener or self.saltar:
                    self.saltar = False
                    break
                while self.pausado and not self.detener:
                    time.sleep(1)
                minutos_restantes = i // 60
                self.label.config(text=f"{estado_actual} ({minutos_restantes} min restantes)")

                if estado_actual == "Caminar":
                    self.label_estado.config(
                        text=f"👟 Caminar\nDistancia: {self.kilometros_totales:.2f} km\n"
                             f"Pasos: {self.pasos_totales}\nCalorías: {self.calorias_totales}"
                    )
                time.sleep(1)

            self.estado_index = (self.estado_index + 1) % len(self.estados)
            self.bloque += 1
            self.label_bloques.config(text=f"Bloques realizados: {self.bloque}")

        self.label.config(text="⛔ Rutina finalizada")
        self.label_estado.config(text="")

    def mostrar_alerta(self, estado):
        try:
            winsound.Beep(1000, 700)
        except:
            pass
        messagebox.showinfo("Cambio de estado", f"Es hora de: {estado}")

root = tk.Tk()
app = TemporizadorApp(root)
root.mainloop()
