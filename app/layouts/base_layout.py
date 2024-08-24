import solara
import solara.lab as lab


@solara.component
def base_layout(children: list):
    with solara.AppLayout() as layout:
        with solara.AppBar() as appbar:
            lab.ThemeToggle()
        
        with solara.Sidebar() as sidebar:
            ...

        with solara.Div() as content:
            content.add_children(children)
    
    return layout