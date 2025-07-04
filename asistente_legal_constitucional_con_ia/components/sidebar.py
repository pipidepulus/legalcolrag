"""Barra de navegación principal que incluye un panel contextual inteligente."""
import reflex as rx
import reflex_clerk_api as clerk
from .asistente_sidebar import asistente_sidebar
from ..states.app_state import AppState # <-- ¡IMPORTANTE AÑADIR ESTA LÍNEA!

class SidebarState(rx.State):
    """Estado para controlar la visibilidad de los componentes de la barra lateral."""
    @rx.var
    def is_on_asistente_page(self) -> bool:
        """Comprueba si la ruta actual es la página del asistente."""
        return self.router.page.path == "/asistente"

def sidebar(is_in_drawer: bool = False) -> rx.Component:
    """La barra de navegación principal de la aplicación."""
    link_click_handler = AppState.toggle_drawer if is_in_drawer else None
    return rx.vstack(
        # --- SECCIÓN SUPERIOR ---
        rx.vstack(
            rx.hstack(
                rx.image(src="/balanza.png", height="2em"),
                rx.heading("Asistente Legal", size="6", color="blue", weight="bold", ),
                width="100%",
            ),
            rx.divider(),
            rx.link("Inicio", href="/", style={"width": "100%", "color":"blue", "font-weight": "bold"}, on_click=link_click_handler),
            clerk.signed_in(
                rx.vstack(
                    rx.link("Asistente Constitucional", href="/asistente", width="100%", style={"color":"blue", "font-weight": "bold"}, on_click=link_click_handler),
                    rx.link("Explorar Proyectos de Ley", href="/proyectos", width="100%", style={"color":"blue", "font-weight": "bold"}, on_click=link_click_handler),
                    rx.link("Prompts", href="/prompts", width="100%", style={"color":"blue", "font-weight": "bold"}, on_click=link_click_handler),
                    spacing="5",
                    width="100%",
                    align_items="start",
                )
            ),
            spacing="5",
            width="100%",
            align_items="start",
        ),
        
        # --- PANEL CONTEXTUAL ---
        clerk.signed_in(
            rx.cond(
                SidebarState.is_on_asistente_page,
                asistente_sidebar(),
                rx.fragment(),
            )
        ),

        rx.spacer(),

        # --- SECCIÓN INFERIOR DE USUARIO ---
        rx.vstack(
            rx.divider(),
            
            # Si está logueado
            clerk.signed_in(
                clerk.user_button(after_sign_out_url="/")
            ),
            
            # Si está deslogueado
            clerk.signed_out(
                # HIJO 1: Botón
                clerk.sign_in_button(
                    rx.button(
                        "Iniciar Sesión",
                        width="100%",
                        style={
                            "font_weight": "bold",
                            "text_transform": "uppercase",
                            "color": "white",
                            "background_color": "blue",  # azul personalizado
                        },
                    )
                ),               
            ),
            
            width="100%",
            padding_bottom="1em",
        ),
        
        # --- ESTILOS DEL CONTENEDOR PRINCIPAL ---
        spacing="5",
        height="100%", # Ocupa toda la altura del contenedor padre (sea el box o el drawer)
        width="100%",  # Ocupa todo el ancho del contenedor padre
        align_items="stretch" # Para que los enlaces ocupen todo el ancho

        '''
        spacing="5",
        width="350px",
        min_width="350px",
        height="100vh",
        padding="1em",
        position="sticky",
        top="0",
        border_right="1px solid var(--gray-4)",
        flex_shrink="0",
        '''
    )