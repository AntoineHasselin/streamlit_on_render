
class CustomComponents:
    from typing import Union


    def __init__(self):
        self.color = 'white'

    @staticmethod
    def create_background(color: str = None, height: str = None, width: str = None):
        import streamlit as st
        background_build = f"" \
                           f""" 
            <style>
                background: {color};
                height: {height},
                width: {width},
            </style>
        """ \
                           f""
        return st.markdown(background_build, unsafe_allow_html=True)

    @staticmethod
    def hide_generator_streamlit():
        from streamlit import markdown
        hide_streamlit_style = """
                        <style>
                        #MainMenu {visibility: hidden;}
                        footer {visibility: hidden;}
                        
                        
                        
                        header {visibility: hidden;}
                        </style>
                        """
        return markdown(hide_streamlit_style, unsafe_allow_html=True)

    @staticmethod
    def style_button_row(clicked_button_ix, n_buttons):
        import streamlit as st

        def get_button_indices(button_ix):
            return {
                'nth_child': button_ix,
                'nth_last_child': n_buttons - button_ix + 1
            }

        clicked_style = """
        div[data-testid*="stHorizontalBlock"] > div:nth-child(%(nth_child)s):nth-last-child(%(nth_last_child)s) button {
            border-color: rgb(255, 75, 75);
            color: rgb(255, 75, 75);
            box-shadow: rgba(255, 75, 75, 0.5) 0px 0px 0px 0.2rem;
            outline: currentcolor none medium;
            height: 10px;
        }
        """
        unclicked_style = """
        div[data-testid*="stHorizontalBlock"] > div:nth-child(%(nth_child)s):nth-last-child(%(nth_last_child)s) button {
            pointer-events: none;
            cursor: not-allowed;
            opacity: 0.65;
            filter: alpha(opacity=65);
            -webkit-box-shadow: none;
            box-shadow: none;
            height: 10px;
        }
        """
        style = ""
        for ix in range(n_buttons):
            ix += 1
            if ix == clicked_button_ix:
                style += clicked_style % get_button_indices(ix)
            else:
                style += unclicked_style % get_button_indices(ix)
        st.markdown(f"<style>{style}</style>", unsafe_allow_html=True)

    @staticmethod
    def sidebar_color(color: str = "#dfebf7"):
        import streamlit as st
        mark_color = "<style>.css-163ttbj {background-color: " + color + ";} </style>"
        return st.markdown(mark_color, unsafe_allow_html=True)

    @staticmethod
    def css_color(css_code: str, color: str = "red", radius: str = '0px', padding: str = '0px'):
        import streamlit as st
        mark_color = f"<style>{css_code}" + "{background-color:" + color + "; border-radius:" + radius + "; padding:" + padding + ";</style>"
        return st.markdown(mark_color, unsafe_allow_html=True)

    @staticmethod
    def style_markdown(
            text: Union[str, int, float] = 'default',
            balise: str = 'title',
            bgcolor: str = 'red',
            radius: str = '0px',
            padding: str = '0px',
            fontcolor: str = 'black'):

        import streamlit as st

        dict_conform_balise = {
            'title': 'h1',
            'header': 'h2',
            'subheader': 'h3',
            'text': 'h4',
        }

        balise_mark = "<" + dict_conform_balise[balise] + " style= background-color:" + bgcolor + ";border-radius:" + radius + ";padding:" + padding + ";color:" + fontcolor + ">" + str(text) + "</" + dict_conform_balise[balise] + ">"
        return st.markdown(balise_mark, unsafe_allow_html=True)

    @staticmethod
    def style_tabs():
        import streamlit as st
        font_css = """
            <style>
            button[data-baseweb="tab"] > div[data-testid="stMarkdownContainer"] > p {
              font-size: 24px;
              padding: 20px;
            }
            </style>
            """

        return st.markdown(font_css, unsafe_allow_html=True)