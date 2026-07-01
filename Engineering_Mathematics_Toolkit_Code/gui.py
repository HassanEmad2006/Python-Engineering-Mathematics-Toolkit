from __future__ import annotations

import math

import customtkinter as ctk
from library import Tangent_Line, Normal_line, area_between_2functions, definite_integral
from vector_library import (
    angle_between_vectors,
    angle_with_axis,
    cross_product,
    degree_angle_in_3d,
    dot,
    magnitute_of_cross,
    magnitude,
    vector_coordinates,
)
from newton_method import find_roots
from sympy import sympify


ctk.set_appearance_mode('dark')
ctk.set_default_color_theme('dark-blue')


def format_number(value) -> str:
    numeric = float(value)
    if abs(numeric - round(numeric)) < 1e-10:
        return str(int(round(numeric)))
    return f'{numeric:.10g}'


def parse_vector(text: str):
    cleaned = text.replace(',', ' ').split()
    if not cleaned:
        raise ValueError('Enter at least one component.')
    return [float(sympify(item).evalf()) for item in cleaned]


class EngineeringCalculatorApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title('Engineering Calculator')
        self.geometry('980x760')
        self.minsize(900, 680)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        header = ctk.CTkFrame(self, corner_radius=20)
        header.grid(row=0, column=0, padx=24, pady=(24, 12), sticky='nsew')
        header.grid_columnconfigure(0, weight=1)

        title = ctk.CTkLabel(
            header,
            text='Engineering Calculator',
            font=ctk.CTkFont(size=30, weight='bold'),
        )
        title.grid(row=0, column=0, padx=24, pady=(20, 4), sticky='w')

        subtitle = ctk.CTkLabel(
            header,
            text='Vector tools, calculus utilities, and Newton\'s method in one place.',
            text_color='#9fb3c8',
        )
        subtitle.grid(row=1, column=0, padx=24, pady=(0, 20), sticky='w')

        self.tabs = ctk.CTkTabview(self, corner_radius=18)
        self.tabs.grid(row=1, column=0, padx=24, pady=(0, 24), sticky='nsew')
        self.tabs.add('Vectors')
        self.tabs.add('Calculus')
        self.tabs.add('Newton')

        self._build_vector_tab(self.tabs.tab('Vectors'))
        self._build_calculus_tab(self.tabs.tab('Calculus'))
        self._build_newton_tab(self.tabs.tab('Newton'))

    def _configure_section(self, parent):
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_columnconfigure(1, weight=1)
        parent.grid_columnconfigure(2, weight=1)

    def _entry_row(self, parent, row, label_text, placeholder, column=0, columnspan=1):
        label = ctk.CTkLabel(parent, text=label_text)
        label.grid(row=row, column=column, padx=12, pady=(12, 4), sticky='w')
        entry = ctk.CTkEntry(parent, placeholder_text=placeholder, height=36)
        entry.grid(row=row + 1, column=column, padx=12, pady=(0, 6), sticky='ew', columnspan=columnspan)
        return entry

    def _build_vector_tab(self, tab):
        self._configure_section(tab)

        intro = ctk.CTkLabel(tab, text='Enter vectors as space or comma separated numbers, such as 3 4 or 1 2 3.')
        intro.grid(row=0, column=0, padx=16, pady=(16, 8), columnspan=3, sticky='w')

        self.vector1_entry = self._entry_row(tab, 1, 'Vector 1', '3 4')
        self.vector2_entry = self._entry_row(tab, 1, 'Vector 2', '1 2 3', column=1)

        self.vector_operation = ctk.StringVar(value='Coordinates')
        self.vector_operation_menu = ctk.CTkOptionMenu(
            tab,
            values=[
                'Coordinates',
                'Magnitude',
                'Angle with Axis',
                'Dot Product',
                'Cross Product',
                'Magnitude of Cross',
                'Angle Between Vectors',
            ],
            variable=self.vector_operation,
        )
        self.vector_operation_menu.grid(row=3, column=0, padx=12, pady=(16, 8), sticky='ew')

        self.vector_target = ctk.StringVar(value='Vector 1')
        self.vector_target_menu = ctk.CTkOptionMenu(
            tab,
            values=['Vector 1', 'Vector 2'],
            variable=self.vector_target,
        )
        self.vector_target_menu.grid(row=3, column=1, padx=12, pady=(16, 8), sticky='ew')

        self.angle_unit = ctk.StringVar(value='Radians')
        self.angle_unit_menu = ctk.CTkOptionMenu(
            tab,
            values=['Radians', 'Degrees'],
            variable=self.angle_unit,
        )
        self.angle_unit_menu.grid(row=3, column=2, padx=12, pady=(16, 8), sticky='ew')

        run_button = ctk.CTkButton(tab, text='Calculate', command=self._run_vector_calculation)
        run_button.grid(row=5, column=0, padx=12, pady=(8, 12), sticky='ew')

        clear_button = ctk.CTkButton(tab, text='Clear Output', command=lambda: self._set_textbox(self.vector_output, ''))
        clear_button.grid(row=5, column=1, padx=12, pady=(8, 12), sticky='ew')

        self.vector_output = ctk.CTkTextbox(tab, height=220, corner_radius=16)
        self.vector_output.grid(row=6, column=0, padx=12, pady=(8, 16), columnspan=3, sticky='nsew')
        self.vector_output.configure(state='disabled')

    def _build_calculus_tab(self, tab):
        self._configure_section(tab)

        intro = ctk.CTkLabel(tab, text='Use standard math syntax, like x**2 + 3*x or sin(x).')
        intro.grid(row=0, column=0, padx=16, pady=(16, 8), columnspan=3, sticky='w')

        self.calculus_expression1 = self._entry_row(tab, 1, 'Function 1', 'x**2 + 3*x')
        self.calculus_expression2 = self._entry_row(tab, 1, 'Function 2', 'sin(x)', column=1)
        self.calculus_variable = self._entry_row(tab, 3, 'Variable', 'x')
        self.calculus_point = self._entry_row(tab, 3, 'Point', '1', column=1)
        self.calculus_lower = self._entry_row(tab, 5, 'Lower Bound', '0')
        self.calculus_upper = self._entry_row(tab, 5, 'Upper Bound', '2', column=1)

        self.calculus_operation = ctk.StringVar(value='Definite Integral')
        self.calculus_operation_menu = ctk.CTkOptionMenu(
            tab,
            values=[
                'Definite Integral',
                'Area Between Two Functions',
                'Tangent Line',
                'Normal Line',
            ],
            variable=self.calculus_operation,
        )
        self.calculus_operation_menu.grid(row=7, column=0, padx=12, pady=(16, 8), sticky='ew')

        run_button = ctk.CTkButton(tab, text='Calculate', command=self._run_calculus_calculation)
        run_button.grid(row=7, column=1, padx=12, pady=(16, 8), sticky='ew')

        self.calculus_output = ctk.CTkTextbox(tab, height=240, corner_radius=16)
        self.calculus_output.grid(row=8, column=0, padx=12, pady=(8, 16), columnspan=3, sticky='nsew')
        self.calculus_output.configure(state='disabled')

    def _build_newton_tab(self, tab):
        self._configure_section(tab)

        intro = ctk.CTkLabel(
            tab,
            text='Enter an equation like x**3 - 2*x - 5 or x**3 = 2*x + 5, then supply starting guesses.',
        )
        intro.grid(row=0, column=0, padx=16, pady=(16, 8), columnspan=3, sticky='w')

        self.newton_equation = self._entry_row(tab, 1, 'Equation', 'x**3 - 2*x - 5')
        self.newton_variable = self._entry_row(tab, 1, 'Variable', 'x', column=1)
        self.newton_guesses = self._entry_row(tab, 3, 'Starting Guesses', '-5, -2, 0, 2, 5')
        self.newton_tolerance = self._entry_row(tab, 3, 'Tolerance', '1e-7', column=1)
        self.newton_iterations = self._entry_row(tab, 5, 'Max Iterations', '50')

        run_button = ctk.CTkButton(tab, text='Find Roots', command=self._run_newton_calculation)
        run_button.grid(row=7, column=0, padx=12, pady=(16, 8), sticky='ew')

        self.newton_output = ctk.CTkTextbox(tab, height=260, corner_radius=16)
        self.newton_output.grid(row=8, column=0, padx=12, pady=(8, 16), columnspan=3, sticky='nsew')
        self.newton_output.configure(state='disabled')

    def _set_textbox(self, textbox, text):
        textbox.configure(state='normal')
        textbox.delete('1.0', 'end')
        textbox.insert('end', text)
        textbox.configure(state='disabled')

    def _format_angle(self, value):
        if self.angle_unit.get() == 'Degrees':
            return f'{math.degrees(value):.10g}°'
        return f'{value:.10g} rad'

    def _run_vector_calculation(self):
        try:
            vector1 = parse_vector(self.vector1_entry.get())
            vector2 = parse_vector(self.vector2_entry.get())
            operation = self.vector_operation.get()

            if operation == 'Coordinates':
                result = f'Vector 1: {vector_coordinates(vector1)}\nVector 2: {vector_coordinates(vector2)}'
            elif operation == 'Magnitude':
                target = vector1 if self.vector_target.get() == 'Vector 1' else vector2
                result = f'{self.vector_target.get()} magnitude: {format_number(magnitude(target))}'
            elif operation == 'Angle with Axis':
                target = vector1 if self.vector_target.get() == 'Vector 1' else vector2
                angle_result = angle_with_axis(target)
                if isinstance(angle_result, tuple):
                    result = (
                        f'{self.vector_target.get()} angles:\n'
                        f'X-axis: {self._format_angle(angle_result[0])}\n'
                        f'Y-axis: {self._format_angle(angle_result[1])}\n'
                        f'Z-axis: {self._format_angle(angle_result[2])}'
                    )
                else:
                    result = f'{self.vector_target.get()} angle: {self._format_angle(angle_result)}'
            elif operation == 'Dot Product':
                result = f'Dot product: {format_number(dot(vector1, vector2))}'
            elif operation == 'Cross Product':
                cross_value = cross_product(vector1, vector2)
                if isinstance(cross_value, list):
                    result = f'Cross product: {vector_coordinates(cross_value)}'
                else:
                    result = f'Cross product: {format_number(cross_value)}k'
            elif operation == 'Magnitude of Cross':
                result = f'Magnitude of cross product: {format_number(magnitute_of_cross(vector1, vector2))}'
            elif operation == 'Angle Between Vectors':
                result = f'Angle between vectors: {self._format_angle(angle_between_vectors(vector1, vector2))}'
            else:
                result = 'Select an operation.'

            self._set_textbox(self.vector_output, result)
        except Exception as error:
            self._set_textbox(self.vector_output, f'Error: {error}')

    def _run_calculus_calculation(self):
        try:
            operation = self.calculus_operation.get()
            variable = self.calculus_variable.get().strip() or 'x'
            function1 = self.calculus_expression1.get().strip()
            function2 = self.calculus_expression2.get().strip()
            point = self.calculus_point.get().strip()
            lower = self.calculus_lower.get().strip()
            upper = self.calculus_upper.get().strip()

            if operation == 'Definite Integral':
                result = definite_integral(function1, lower, upper, variable)
                output = f'Integral of {function1} from {lower} to {upper}: {result}'
            elif operation == 'Area Between Two Functions':
                result = area_between_2functions(function1, function2, lower, upper, variable)
                output = f'Area between {function1} and {function2} from {lower} to {upper}: {result}'
            elif operation == 'Tangent Line':
                output = Tangent_Line(function1, point, variable)
            elif operation == 'Normal Line':
                output = Normal_line(function1, point, variable)
            else:
                output = 'Select an operation.'

            self._set_textbox(self.calculus_output, output)
        except Exception as error:
            self._set_textbox(self.calculus_output, f'Error: {error}')

    def _run_newton_calculation(self):
        try:
            equation = self.newton_equation.get().strip()
            variable = self.newton_variable.get().strip() or 'x'
            guesses_text = self.newton_guesses.get().strip()
            tolerance = float(sympify(self.newton_tolerance.get().strip()).evalf())
            max_iterations = int(float(sympify(self.newton_iterations.get().strip()).evalf()))
            guesses = [float(sympify(item).evalf()) for item in guesses_text.replace(';', ',').split(',') if item.strip()]

            roots = find_roots(
                equation,
                guesses=guesses,
                variable=variable,
                tolerance=tolerance,
                max_iterations=max_iterations,
            )

            if not roots:
                output = 'No roots converged. Try different starting guesses.'
            else:
                lines = ['Newton roots:']
                for root, guess, iterations in roots:
                    lines.append(
                        f'guess {format_number(guess)} -> root {format_number(root)} '
                        f'({iterations} iterations)'
                    )
                output = '\n'.join(lines)

            self._set_textbox(self.newton_output, output)
        except Exception as error:
            self._set_textbox(self.newton_output, f'Error: {error}')


def main():
    app = EngineeringCalculatorApp()
    app.mainloop()


if __name__ == '__main__':
    main()
