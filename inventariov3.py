from tkinter import Entry, Label, Frame, Tk, Button, ttk, StringVar, IntVar
import json
import csv
import math

class SistemaLecheria(Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.inscritos = {}
        self.no_inscritos = {}
        self.sobres_disponibles = self.cargar_sobres_disponibles()

        try:
            with open("datos_lecheria.json", "r") as file:
                datos_guardados = json.load(file)
                self.inscritos = datos_guardados.get("inscritos", {})
                self.no_inscritos = datos_guardados.get("no_inscritos", {})
        except FileNotFoundError:
            pass

        self.frame1 = Frame(master)
        self.frame1.grid(columnspan=2, column=0, row=0)
        self.frame2 = Frame(master, bg='navy')
        self.frame2.grid(column=0, row=1)

        self.nombre = StringVar()
        self.estado_inscrito = IntVar()  # 1 si está inscrito, 0 si no está inscrito
        self.cantidad = StringVar()

        self.create_widgets()

    def cargar_sobres_disponibles(self):
        try:
            with open("datos_lecheria.json", "r") as file:
                datos_guardados = json.load(file)
                return datos_guardados.get("sobres_disponibles", 3000)
        except FileNotFoundError:
            return 3000

    def guardar_sobres_disponibles(self):
        try:
            with open("datos_lecheria.json", "r") as file:
                datos_exist = json.load(file)
                datos_exist["sobres_disponibles"] = self.sobres_disponibles
        except FileNotFoundError:
            datos_exist = {"sobres_disponibles": self.sobres_disponibles}

        with open("datos_lecheria.json", "w") as file:
            json.dump(datos_exist, file)

    def create_widgets(self):
        Label(self.frame1, text='R E G I S T R O \t D E \t D A T O S', bg='gray22', fg='white', font=('Orbitron', 15, 'bold')).grid(column=0, row=0)

        Label(self.frame2, text='Agregar Nuevos Datos', fg='white', bg='navy', font=('Rockwell', 12, 'bold')).grid(columnspan=2, column=0, row=0, pady=5)
        Label(self.frame2, text='Nombre', fg='white', bg='navy', font=('Rockwell', 13, 'bold')).grid(column=0, row=1, pady=15)
        Label(self.frame2, text='Estado', fg='white', bg='navy', font=('Rockwell', 13, 'bold')).grid(column=0, row=2, pady=15)
        Label(self.frame2, text='Cantidad', fg='white', bg='navy', font=('Rockwell', 13, 'bold')).grid(column=0, row=3, pady=15)

        Entry(self.frame2, textvariable=self.nombre, font=('Arial', 12)).grid(column=1, row=1)
        ttk.Checkbutton(self.frame2, text='Inscrito', variable=self.estado_inscrito, onvalue=1, offvalue=0).grid(column=1, row=2)
        Entry(self.frame2, textvariable=self.cantidad, font=('Arial', 12)).grid(column=1, row=3)

        Label(self.frame2, text='Sobres Disponibles:', fg='white', bg='navy', font=('Rockwell', 13, 'bold')).grid(column=0, row=6, pady=15, sticky='e')
        Label(self.frame2, text=f"{self.sobres_disponibles} Sobres / {self.calcular_cajas(self.sobres_disponibles)} Cajas", fg='white', bg='navy', font=('Rockwell', 13, 'bold')).grid(column=1, row=6, pady=15, sticky='w')

        Button(self.frame2, command=self.registrar_entrega, text='REGISTRAR', font=('Arial', 10, 'bold'), bg='magenta2').grid(column=0, row=4, pady=10)
        Button(self.frame2, command=self.limpiar_datos, text='LIMPIAR', font=('Arial', 10, 'bold'), bg='orange red').grid(column=1, row=4, pady=10)
        Button(self.frame2, command=self.mostrar_inscritos, text='Mostrar Inscritos', font=('Arial', 10, 'bold'), bg='light green').grid(column=0, row=5, pady=10, padx=(10))
        Button(self.frame2, command=self.mostrar_no_inscritos, text='Mostrar No Inscritos', font=('Arial', 10, 'bold'), bg='light coral').grid(column=1, row=5, pady=10, padx=(0, 10), sticky='e')

        self.create_tabla()

    def create_tabla(self):
        self.tabla_frame = Frame(self.master, bg='gray22')
        self.tabla_frame.grid(column=1, row=1, sticky='nsew', rowspan=18)
        self.master.grid_columnconfigure(1, weight=1)
        self.tabla = ttk.Treeview(self.tabla_frame, height=15)
        self.tabla.grid(column=0, row=0, pady=10, sticky='nsew')

        self.tabla.columnconfigure(0, weight=1, minsize=300)

        self.tabla['columns'] = ('Nombre', 'Estado', 'Cantidad', 'Total Inscritos', 'Total No Inscritos', 'Cajas')

        self.tabla.column('#0', minwidth=0, width=0, stretch=False)
        self.tabla.column('Nombre', minwidth=120, width=120, anchor='center')
        self.tabla.column('Estado', minwidth=120, width=120, anchor='center')
        self.tabla.column('Cantidad', minwidth=120, width=120, anchor='center')
        self.tabla.column('Total Inscritos', minwidth=150, width=150, anchor='center')
        self.tabla.column('Total No Inscritos', minwidth=150, width=150, anchor='center')
        self.tabla.column('Cajas', minwidth=120, width=120, anchor='center')

        self.tabla.heading('#0', text='', anchor='center')
        self.tabla.heading('Nombre', text='Nombre', anchor='center')
        self.tabla.heading('Estado', text='Estado', anchor='center')
        self.tabla.heading('Cantidad', text='Cantidad', anchor='center')
        self.tabla.heading('Total Inscritos', text='Total Inscritos', anchor='center')
        self.tabla.heading('Total No Inscritos', text='Total No Inscritos', anchor='center')
        self.tabla.heading('Cajas', text='Cajas', anchor='center')

        estilo = ttk.Style(self.tabla_frame)
        estilo.theme_use('clam')
        estilo.configure(".", font=('Helvetica', 10, 'bold'), foreground='red2')
        estilo.configure("Treeview", font=('Helvetica', 10, 'bold'), foreground='black', background='white')
        estilo.map('Treeview', background=[('selected', 'green2')], foreground=[('selected', 'black')])

    def registrar_entrega(self):
        nombre = self.nombre.get()
        estado = 'Inscrito' if self.estado_inscrito.get() == 1 else 'No Inscrito'
        cantidad = self.cantidad.get()

        if nombre and estado and cantidad != '' and int(cantidad) <= self.sobres_disponibles:
            self.actualizar_totales(nombre, estado, int(cantidad))
            self.tabla.insert('', 'end', values=(nombre, estado, cantidad))
            self.sobres_disponibles -= int(cantidad)
            self.guardar_sobres_disponibles()
            self.guardar_datos()
            self.guardar_datos_csv()
            self.limpiar_datos()
            self.actualizar_sobres_disponibles_label()

    def actualizar_sobres_disponibles_label(self):
        sobres_label = self.tabla_frame.grid_slaves(row=6, column=1)[0]
        sobres_label.configure(text=f"{self.sobres_disponibles} Sobres / {self.calcular_cajas(self.sobres_disponibles)} Cajas")

    def calcular_cajas(self, sobres):
        sobres_por_caja = 36
        return math.ceil(sobres / sobres_por_caja)

    def actualizar_totales(self, nombre, estado, cantidad):
        if estado == 'Inscrito':
            self.inscritos[nombre] = self.inscritos.get(nombre, 0) + cantidad
        else:
            self.no_inscritos[nombre] = self.no_inscritos.get(nombre, 0) + cantidad

        total_inscritos = sum(self.inscritos.values())
        total_no_inscritos = sum(self.no_inscritos.values())

        for item in self.tabla.get_children():
            values = self.tabla.item(item, 'values')
            if values[1] == 'Inscrito':
                self.tabla.set(item, 'Total Inscritos', total_inscritos)
            elif values[1] == 'No Inscrito':
                self.tabla.set(item, 'Total No Inscritos', total_no_inscritos)
            self.tabla.set(item, 'Cajas', self.calcular_cajas(total_inscritos + total_no_inscritos))

    def limpiar_datos(self):
        self.nombre.set('')
        self.estado_inscrito.set(0)
        self.cantidad.set('')

    def guardar_datos(self):
        try:
            with open("datos_lecheria.json", "r") as file:
                datos_exist = json.load(file)
                datos_exist["inscritos"] = self.inscritos
                datos_exist["no_inscritos"] = self.no_inscritos
        except FileNotFoundError:
            datos_exist = {"inscritos": self.inscritos, "no_inscritos": self.no_inscritos}

        with open("datos_lecheria.json", "w") as file:
            json.dump(datos_exist, file)

    def guardar_datos_csv(self):
        with open("datos_lecheria.csv", mode="w", newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Nombre", "Estado", "Cantidad"])
            for nombre, cantidad in self.inscritos.items():
                writer.writerow([nombre, "Inscrito", cantidad])
            for nombre, cantidad in self.no_inscritos.items():
                writer.writerow([nombre, "No Inscrito", cantidad])

    def mostrar_inscritos(self):
        self.tabla.delete(*self.tabla.get_children())
        for nombre, cantidad in self.inscritos.items():
            total_inscritos = sum(self.inscritos.values())
            self.tabla.insert('', 'end', values=(nombre, 'Inscrito', cantidad, total_inscritos, 0, self.calcular_cajas(total_inscritos)))

    def mostrar_no_inscritos(self):
        self.tabla.delete(*self.tabla.get_children())
        for nombre, cantidad in self.no_inscritos.items():
            total_no_inscritos = sum(self.no_inscritos.values())
            self.tabla.insert('', 'end', values=(nombre, 'No Inscrito', cantidad, 0, total_no_inscritos, self.calcular_cajas(total_no_inscritos)))

def main():
    ventana = Tk()
    ventana.wm_title("Control de Lechería")
    ventana.config(bg='gray22')
    ventana.geometry('1010x400')
    #ventana.resizable(0, 0)
    app = SistemaLecheria(ventana)
    app.mainloop()

if __name__ == "__main__":
    main()
