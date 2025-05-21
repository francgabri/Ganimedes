import flet as ft
import csv


def main(page: ft.Page):
    page.title = "GANIMEDES"
    page.bgcolor = ft.colors.BLUE_GREY_800
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    titulo = ft.Text("GANIMEDES",size =24,color=ft.colors.WHITE)
    usuario = ft.TextField(label="usuario",autofocus=True)
    contraseña = ft.TextField(label="contraseña",password=True)  
    mensaje = ft.Text()

    #contenido para el tab de tareas
    
    # Leer tareas desde un archivo
    def leer_datos():
        tareas = []
        try:
            with open("tareas.csv", mode="r") as archivo:
                reader = csv.reader(archivo)
                for fila in reader:
                    # Asumir que la columna de estado es un string "True" o "False"
                    fila[1] = fila[1] == "True"  # Convertirlo a bool
                    tareas.append(fila)
        except FileNotFoundError:
            print("El archivo no existe, se creará uno nuevo.")
        return tareas
    # Guardar tareas en un archivo
    def escribir_datos(tareas):
        with open("tareas.csv", mode="w", newline='') as archivo:
            writer = csv.writer(archivo)
            writer.writerows(tareas)

    tareas = leer_datos()
    texto_input = ft.TextField(hint_text="escribe una nueva tarea")
     
    def agregar_tarea(e):
        if texto_input.value:  # Verifica que el campo no esté vacío
            contenido = texto_input.value
            estado = False
            tarea = [contenido, estado]
            tareas.append(tarea)
            escribir_datos(tareas)
            texto_input.value = ""  # Limpia el campo de texto
            actualizar_lista() 

    def actualizar_lista():
        lista_tareas.controls.clear()  # Limpia la lista actual
        for tarea in tareas:
            # Creamos un checkbox que tiene un estado vinculado con la tarea
            checkbox = ft.Checkbox(value=tarea[1], on_change=lambda e, tarea=tarea: cambiar_estado(e, tarea))
            lista_tareas.controls.append(
                ft.ListTile(
                    title=ft.Text(tarea[0]),
                    leading=checkbox,
                    bgcolor=ft.colors.BLUE_GREY_800
                )
            )
        page.update()

    def cambiar_estado(e, tarea):
        tarea[1] = e.control.value  # Actualiza el estado de la tarea en la lista

    def eliminar_tareas_seleccionadas(e):  
        # Filtra las tareas seleccionadas (marcadas)
        tareas_a_eliminar = [tarea for tarea in tareas if tarea[1] == True]
        for tarea in tareas_a_eliminar:
            tareas.remove(tarea)  # Elimina las tareas seleccionadas
        escribir_datos(tareas)  # Guarda los cambios
        actualizar_lista()  # Actualiza la lista después de eliminar las tareas

        
   
    boton_agregar = ft.FilledButton(text="agregar tarea",on_click=agregar_tarea)
    boton_eliminar = ft.FilledButton(text="Eliminar tareas seleccionadas", on_click=eliminar_tareas_seleccionadas)
    lista_tareas = ft.ListView(expand=1,spacing=3)
    
    contenido_tareas = ft.Column([titulo,texto_input,boton_agregar,boton_eliminar,lista_tareas])
    actualizar_lista()
    #contenido para el tab de notas6
    def load_notes():
        try:
            with open("notas.txt", "r") as archivo:
                # Leer las notas, una por línea
                return archivo.read().splitlines()
        except FileNotFoundError:
            return []  # Si el archivo no existe, devolver una lista vacía

    def save_notes():
        with open("notas.txt","w") as archivo:
            for note in grid.controls:
                archivo.write(note.content.controls[0].value + "\n")

    def create_note(text):
        # Create a text field for the note
        texto = ft.TextField(value=text, multiline=True, bgcolor=ft.Colors.BLUE_GREY_50)
        
        # Create the note container with a delete button
        note = ft.Container(
            content=ft.Column([
                texto, 
                ft.IconButton(icon=ft.icons.DELETE, on_click=lambda e: delete_note(note))
            ])
        )
        return note
    
    def delete_note(note):
        # Remove the note from the grid and update the page
        grid.controls.remove(note)
        save_notes()
        page.update()
    
    grid = ft.GridView(
        expand=True,
        max_extent=220,
        child_aspect_ratio=1,
        spacing=10,
        run_spacing=10,
    )
    
        # Function to add a new note
  
    def add_note():
        # Default text for the new note
        new_note_text = "Nueva Nota"
        
        # Append the new note to the grid
        grid.controls.append(create_note(new_note_text))
        save_notes()
        page.update()  # Refresh the page to display the new note

     # Button to add a new note
    
    boton_add = ft.FilledButton("Añadir Nota", on_click=lambda e: add_note())


    # Cargar las notas guardadas al iniciar la aplicación
    for note_text in load_notes():
        grid.controls.append(create_note(note_text))

    contenido_notas = ft.Column([grid,boton_add])
      
    # Guardar las notas cuando se cierra la página
    page.on_closing = save_notes


    #contenido para el tab de finanzas
    proximamente = ft.Text("proximamente")
    contenido_finanzas=ft.Column([proximamente])
    #contenido para el tab de calendario
    proximamente = ft.Text("proximamente")
    contenido_calendario=ft.Column([proximamente])


    tabs = ft.Tabs(
            selected_index=0,
            animation_duration=300,
            tabs=[
                ft.Tab(text ="tareas",icon = ft.icons.LIST_ALT,content=contenido_tareas),
                ft.Tab(text = "notas",icon = ft.icons.NOTE_ADD,content= contenido_notas),
                ft.Tab(text = "finanzas",icon = ft.icons.MONETIZATION_ON,content=contenido_finanzas),
                ft.Tab(text="calendario",icon=ft.icons.CALENDAR_MONTH,content=contenido_calendario),
                ],
            )
    def login_click(e):

        username = usuario.value
        password = contraseña.value
        
        if username == "franco" and password == "1234":
            page.controls.clear()
            page.add(tabs)
        else:
            mensaje.value = "usuario o contraseña incorrectos"
            page.update()
        
        page.update()

    login_button = ft.ElevatedButton("login",on_click=login_click)


    
   

    page.add(titulo,usuario,contraseña,mensaje,login_button)


ft.app(target=main)