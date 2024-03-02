import modules.ui.ui as startup_ui
import modules.controllers.facade as facade
from modules.controllers.view_data import ViewData


# ZKILL_BR_LINK = 'https://zkillboard.com/related/31001761/202012040000'


def main() -> None:
    view_data = startup_ui.start_ui()

    print(view_data.wreck_list_a)
    print(view_data.wreck_list_b)
    print(view_data.texture_type)
    print(view_data.scale_multiplier)
    print(view_data.br_link)

    view_data.sanitise_input()

    facade.run_main_program(view_data.wreck_list_a,
                            view_data.wreck_list_b,
                            view_data.texture_type,
                            view_data.scale_multiplier)


if __name__ == '__main__':
    main()
