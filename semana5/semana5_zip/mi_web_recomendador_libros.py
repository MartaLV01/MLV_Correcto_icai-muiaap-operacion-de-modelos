import streamlit as st

# Lista de libros
books = [
    {
        "title": "Dune",
        "author": "Frank Herbert",
        "genres": ["Ciencia ficción", "Aventura", "Política"], # una lista mejor que varias variables
        "length": "Largo",
        "type": "Saga"
    },
    {
        "title": "Orgullo y prejuicio",
        "author": "Jane Austen",
        "genres": ["Romance", "Clásico", "Humor"],
        "length": "Medio",
        "type": "Autoconclusivo"
    },
    {
        "title": "El principito",
        "author": "Antoine de Saint-Exupéry",
        "genres": ["Fantasía", "Fábula", "Filosofía"],
        "length": "Corto",
        "type": "Autoconclusivo"
    },
    {
        "title": "Harry Potter y la piedra filosofal",
        "author": "J.K. Rowling",
        "genres": ["Fantasía", "Aventura", "Misterio"],
        "length": "Largo",
        "type": "Saga"
    },
    {
        "title": "El hobbit",
        "author": "J.R.R. Tolkien",
        "genres": ["Fantasía", "Aventura"],
        "length": "Largo",
        "type": "Saga"
    },
    {
        "title": "Los juegos del hambre",
        "author": "Suzanne Collins",
        "genres": ["Ciencia ficción", "Distopía", "Acción", "Romance"],
        "length": "Medio",
        "type": "Saga"
    },
    {
        "title": "1984",
        "author": "George Orwell",
        "genres": ["Distopía", "Ciencia ficción", "Clásico", "Política"],
        "length": "Medio",
        "type": "Autoconclusivo"
    },
    {
        "title": "Rebelión en la granja",
        "author": "George Orwell",
        "genres": ["Clásico", "Distopía", "Sátira", "Política"],
        "length": "Corto",
        "type": "Autoconclusivo"
    },
    {
        "title": "Coraline",
        "author": "Neil Gaiman",
        "genres": ["Fantasía", "Terror", "Aventura"],
        "length": "Corto",
        "type": "Autoconclusivo"
    },
    {
        "title": "Asesinato en el Orient Express",
        "author": "Agatha Christie",
        "genres": ["Misterio", "Crimen", "Clásico"],
        "length": "Medio",
        "type": "Saga"
    },
    {
        "title": "La sombra del viento",
        "author": "Carlos Ruiz Zafón",
        "genres": ["Misterio", "Thriller", "Histórico", "Romance"],
        "length": "Largo",
        "type": "Saga"
    },
    {
        "title": "Cien años de soledad",
        "author": "Gabriel García Márquez",
        "genres": ["Realismo mágico", "Clásico", "Histórico", "Fantasía"],
        "length": "Largo",
        "type": "Autoconclusivo"
    }
]

genres = [
    "Fantasía",
    "Romance",
    "Misterio",
    "Ciencia ficción",
    "Aventura",
    "Clásico",
    "Terror",
    "Distopía",
    "Histórico",
    "Thriller",
    "Humor",
    "Filosofía",
    "Fábula",
    "Política",
    "Acción",
    "Crimen",
    "Sátira",
    "Realismo mágico"
]

tipo_coleccion = ["Cualquiera", "Saga", "Autoconclusivo"]
extension = ["Cualquiera", "Corto", "Medio", "Largo"]

st.set_page_config(page_title="Recomendador de libros")

st.title("📚 Recomendador de libros") # titulo de la pagina
st.write("Encuentra tu próxima lectura.") # informacion adicional


# crea formulario de nombre Book_form. Es para identificarlo por si hubiera varios formularios en la pagina ademas,
# sin el formulario, Streamlit ejecutaría de nuevo la aplicación cada vez que el usuario cambiase una selección.
# con st.form(), los cambios en los selectores se mantienen pendientes hasta que el usuario pulsa el botón de enviar (submitted).
with st.form("book_form"):

    # diversas casillas de seleccion
    # para el genero
    genre = st.selectbox(
        "¿Qué género te gusta?",
        genres
    )

    genre2 = st.selectbox(
        "Puedes elegir un segundo genero [opcional]",
        ["Ninguno"] + genres # de esta manera se añade "ninguno" tambien como opcion
    )

    # se normaliza, aunque se podria dejar como "Ninguno" si luego el genre != "" se cambia por "Ninguno"
    if genre2 == "Ninguno":
        genre2 = ""
    
    # para el tipo de coleccion
    book_type = st.selectbox(
        "¿Qué tipo de libro prefieres?",
        tipo_coleccion
    )

    # para la longitud del libro
    length = st.selectbox(
        "¿Qué extensión prefieres?",
        extension
    )

    # boton de ejecutar la recomendacion
    submitted = st.form_submit_button("Recomendar libro")

# acciones a realizar cuando el user pulsa el boton
if submitted:

    # se esta usando compresion de listas en vez de los bucles for con ifs
    # recommendations = []
    # for book in books:
    #    if genre in book["genres"]:
    #       recommendations.append(book)

    # recommendations_one -> Coincide con al menos un genero
    # recommendations_both -> Coincide con ambos generos

    # se busca por el genero.
    recommendations_one = [
        book for book in books
        if genre in book["genres"] or genre2 in book["genres"]
    ]

    recommendations_both = [
        book for book in books
        if genre in book["genres"] and genre2 in book["genres"]
    ]

    # no importa el orden en que se mire la coleccion y la longitud, ya que en ambos casos la lista que se reocorre
    # es la de recommendations_one/_both, y se actualiza esa misma lista.

    # si se elige el tipo de coleccion, se busca coincidencias entre aquellos libros que contienen el genero elegido
    # se actualiza la lista dejando solo aquellos que cumplan que la coleccion sea la elegida por el usuario
    if book_type != "Cualquiera":
        recommendations_one = [
            book for book in recommendations_one
            if book["type"] == book_type
        ]

    if book_type != "Cualquiera":
        recommendations_both = [
            book for book in recommendations_both
            if book["type"] == book_type
        ]

    # si se elige longitud del libro, se busca coincidencias entre aquellos libros que contienen la longitud elegida
    # se actualiza la lista dejando solo aquellos que cumplan que la coleccion sea la elegida por el usuario
    if length != "Cualquiera":
        recommendations_one = [
            book for book in recommendations_one
            if book["length"] == length
        ]

    if length != "Cualquiera":
        recommendations_both = [
            book for book in recommendations_both
            if book["length"] == length
        ]

    # si recommendations_one no es una lista vacia
    if recommendations_one:

        # con succes se resalta el mensaje en verde
        # se pone un mensaje con el numero de recomendaciones encontradas

        # para poeder tener el mensaje con una correcta sintaxis
        if len(recommendations_one) == 1:
            st.success("¡Tenemos 1 recomendación para ti!")
        else:
            st.success(f"¡Tenemos {len(recommendations_one)} recomendaciones para ti!")
        
        st.markdown("**Coincide con al menos uno de los dos géneros**") # lo poen en negrita

        i=1 # indicara la posicion del libro en la lista
        for book in recommendations_one: # se recorre la lista de recomendaciones
            st.subheader(f"{i}. {book["title"]}") # es un suubtitulo.
            st.write(f"Autor: {book['author']}")
            st.write(f"Géneros: {', '.join(book['genres'])}")
            st.write(f"Extensión: {book['length']}")
            st.write(f"Tipo: {book['type']}")
            st.divider() # añade una linea divisoria entre los libros
            i=i+1

    else:
        st.warning("No hemos encontrado libros con al menos uno de los géneros y que cumplan esas características.")

    if genre2 != "": # si ha elegido un segundo genero
        if recommendations_both:

            # con succes se resalta el mensaje en verde
            # se pone un mensaje con el numero de recomendaciones encontradas

            # para poeder tener el mensaje con una correcta sintaxis
            if len(recommendations_both) == 1:
                st.success("¡Tenemos 1 recomendación para ti!")
            else:
                st.success(f"¡Tenemos {len(recommendations_both)} recomendaciones para ti!")

            st.markdown("**Coincide con los dos géneros**")

            i=1 # indicara la posicion del libro en la lista
            for book in recommendations_both: # se recorre la lista de recomendaciones
                st.subheader(f"{i}. {book["title"]}") # es un suubtitulo.
                st.write(f"Autor: {book['author']}")
                st.write(f"Géneros: {', '.join(book['genres'])}")
                st.write(f"Extensión: {book['length']}")
                st.write(f"Tipo: {book['type']}")
                st.divider() # añade una linea divisoria entre los libros
                i=i+1
        else:
            st.warning("No hemos encontrado libros que tengan ambos generos y cumplan esas caracteristicas.")

